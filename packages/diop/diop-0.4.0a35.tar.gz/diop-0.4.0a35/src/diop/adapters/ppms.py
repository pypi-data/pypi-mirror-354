"""Module providing the BookingSystem interface for Stratocore's PPMS."""

from logging import INFO

from datetime import datetime, date, time

from django.conf import settings
from django.utils.timezone import make_aware, make_naive

from loguru import logger as log
from logging_interceptor import setup_loguru_interceptor
from pyppms import ppms

from ..models import User, PpmsBooking, Reservation, DeliveryGroup, Issue


class BookingSystem:
    """Fetch and process information from PPMS and update the DIOP database.

    Attributes
    ----------
    interceptor_level : int
        The logging level to pass to the `setup_loguru_interceptor` call.
    cf_ref : int
        The PPMS core facility reference.
    """

    def __init__(self, interceptor_level=INFO):
        self.interceptor_level = interceptor_level
        log.debug("Instantiating a BookingSystem for 'PPMS'...")
        self.cf_ref = settings.PYPPMS_CORE_REF

        self._conn = None
        self._supersystems = None
        self._supersystems_ids = []

    @property
    def conn(self):
        """Return the PPMS connection, or create it if not yet connected.

        Returns
        -------
        pyppms.ppms.PpmsConnection
        """
        if self._conn is not None:
            return self._conn

        setup_loguru_interceptor(level=self.interceptor_level)
        cache_path = settings.PYPPMS_CACHE
        log.debug(f"Using [{cache_path}] as PyPPMS cache path.")
        api_url = settings.PYPPMS_URI
        api_key = settings.PYPPMS_API_KEY
        self._conn = ppms.PpmsConnection(
            api_url, api_key, cache=cache_path, cache_users_only=True
        )
        log.debug(f"Connected to PPMS at [{api_url}].")
        return self._conn

    @property
    def supersystems(self):
        """A dict mapping names to IDs of "supersystems" from PPMS.

        A "supersystem" is a virtual / meta group of systems comprised of two or
        more actual PPMS systems. Currently PPMS doesn't have a concept of
        booking just *any* slot in no-matter-what-exact-system, but we need this
        to reflect the random assignment of machines (i.e. there is no fixed
        mapping from a PPMS-system to a DIOP-machine).

        The method will query PPMS for all systems matching the "room" /
        "loca(lisa)tion" value defined in the `PumapiSystemsLocation`
        configuration setting and group them by the values specified in
        `PumapiSystemGroups`. That setting may contain multiple group names
        separated by a comma, each of them will result in a separate entry in
        the returned dict (unless empty).

        Returns
        -------
        dict
            A dict with the group name (the "supersystem" label) as the key and
            a list with the corresponding PPMS system IDs as value. Supersystems
            that do not have any related systems in PPMS will be skipped.

        Example
        -------
        >>> ppms = BookingSystem()
        >>> ppms.supersystems
        {
            "WestWingBookableSuperSystem": [37, 38, 39, 44],
            "HighlandsMetaSystem": [73, 74, 77, 78],
        }
        """
        if self._supersystems is not None:
            return self._supersystems

        self._supersystems = {}
        location_filter = settings.PYPPMS_LOC_FILTER
        name_groups = settings.PYPPMS_NAME_GROUPS
        log.trace(f"Using 'Room=[{location_filter}]' to identify systems in PPMS...")

        for name_group in name_groups:
            group_ids = self.conn.get_systems_matching(
                localisation=location_filter, name_contains=[name_group]
            )
            if not group_ids:
                log.warning(f"No systems matching name [{name_group}] found!")
                continue

            log.trace(f"System IDs matching name [{name_group}]: {group_ids}")
            self._supersystems[name_group] = group_ids

        return self._supersystems

    @property
    def supersystems_ids(self):
        """A list of all PPMS system IDs belonging to any super-system."""
        if self._supersystems_ids:
            return self._supersystems_ids

        for ids in self.supersystems.values():
            self._supersystems_ids += ids

        return self._supersystems_ids

    def _merge_reservations_all(self, username: str, category: str):
        """Merge adjacent reservations and update corresponding bookings.

        Parameters
        ----------
        username : str
            The username to look for reservations / bookings.
        category : str
            The delivery group related to the reservations.

        Returns
        -------
        int
            The count of merged reservations.
        """
        merged = self._merge_reservations_all_rec(username, category)
        if merged > 0:
            log.success(f"🗜 🗓🗓✅ Merged (and removed) {merged} reservations.")
        else:
            log.debug("🗓 🔍 No adjacent reservations found, nothing merged.")

        return merged

    def _merge_reservations_all_rec(self, username: str, category: str):
        merged = 0
        all_res = Reservation.objects.filter(user=username, deliverygroup=category)
        if len(all_res) < 2:
            return 0

        log.debug(f"🗓🗓🔍 Checking {len(all_res)} reservations of {username}...")
        for res in all_res:
            try:
                adjacent = Reservation.objects.get(
                    user=username,
                    deliverygroup=category,
                    t_start=res.t_end,
                )
                merged += self._merge_reservations(res, adjacent)
                log.debug("🗜 🗓🗓 ➿ Merged reservations, recursion necessary...")
                merged += self._merge_reservations_all_rec(username, category)
                break
            except Reservation.DoesNotExist:
                log.debug(f"🗓 🔍 No adjacent reservation for ({res.id}) found.")

        return merged

    def _merge_reservations(self, res_1: Reservation, res_2: Reservation):
        """Merge two adjacent reservations.

        Check if the end time of the first given reservation is matching the
        start time of the second one and, if yes, merge the second reservation
        into the first one (the second one will be removed).

        Parameters
        ----------
        res_1 : Reservation
            The first reservation to be merged. In case the merge is happening,
            this reservation will be extended and kept in the database.
        res_2 : Reservation
            The second reservation to be merged. In case the merge is happening,
            this reservation will be discarded after extending the first one.

        Returns
        -------
        int
            1 in case the reservations got merged, 0 otherwise.
        """
        if res_1.t_end != res_2.t_start:
            log.warning(
                f"💣🔥 Not merging non-adjacent reservations: [{res_1}] vs. [{res_2}]"
            )
            return 0

        log.info(f"🗓 🧲🗓 Merging adjacent reservations: [{res_1}] + [{res_2}]")
        res_1.t_end = res_2.t_end
        res_1.save()
        for booking in PpmsBooking.objects.filter(reservation=res_2):
            booking.reservation = res_1
            booking.save()
        log.debug(f"🗓🚮 Deleting merged reservation ({res_2.id})...")
        res_2.delete()
        log.success(f"🗓 🧲🗓✅ Done merging adjacent reservations: {res_1}")

        return 1

    def _populate_name_mapping(self):
        """Fetch users from the DIOP-DB and populate the PyPPMS name mapping."""
        log.trace("Populating the pyppms name mapping dict...")
        users = User.objects.filter(enabled=True, accessgroup_member=True)
        for user in users:
            # use the standard `fullname` attribute as a fallback:
            key = user.fullname

            # in case the DB has the `ppms_fullname` filled, it has priority:
            if user.ppms_fullname:
                key = user.ppms_fullname
                log.trace(f"Using `ppms_fullname` attribute: {key}")

            self.conn.fullname_mapping[key] = user.username
        # log.trace(self.conn.fullname_mapping)

    def _process_booking_updates(self):
        """Process changes to bookings after pulling from PPMS."""
        self._process_deleted_bookings_all()
        self._process_new_bookings_all()
        new = PpmsBooking.objects.filter(sync_state="N").count()
        if new:
            msg = f"Still {new} bookings in state 'New' after processing!"
            log.warning(f"💫🎫💥 {msg}")
            issue = Issue(description=msg, severity=2)
            issue.save()

    def _split_reservation(self, booking):
        res = booking.reservation
        log.info(f"🗓🪓 Splitting reservation {res} on booking {booking}...")
        split_start = booking.t_start
        split_end = booking.t_end
        res_new = Reservation(
            user=res.user,
            deliverygroup=res.deliverygroup,
            t_start=split_end,
            t_end=res.t_end,
        )
        res_new.save()

        res.t_end = split_start
        res.save()
        log.success(f"✨🗓🗓 New reservations: {res} 🚧 {res_new}")

        updated = 0
        for linked in PpmsBooking.objects.filter(reservation=res):
            if linked.t_start < res_new.t_start:
                log.debug(f"Not updating, belongs to old res: {linked}")
                continue
            log.info(f"🎫🔗🗓  Updating link of [{linked}] to [{res_new.id}]...")
            linked.reservation = res_new
            linked.save()
            updated += 1
        log.info(f"🎫🔗🗓✅ Updated {updated} links to reservation [{res_new.id}].")

        log.success(
            f"🗓🪓✅ Done splitting reservation {res}, additional "
            f"reservation {res_new}"
        )

    def _process_deleted_bookings(self, system_ids, username):
        """Process bookings from a given user that are marked as `deleted`.

        First, all bookings having their `sync_state` field set to `deleted` and
        that are matching the given user and the list of PPMS system IDs will be
        fetched from the DB.

        Then they will be checked if they are linked to a reservation (meaning
        they belong to a user account known to the DIOP-DB *and* have been
        processed before).

        In case a booking is not linked to a reservation, it will be deleted
        from the bookings table (NOT from PPMS!).

        Otherwise, the booking will be checked if it covers the entire
        reservation (reservation will be deleted), if it matches the start or
        the end (reservation will be shortened), or if it's fully enclosed by
        the reservation (requiring the reservation to be split).

        Parameters
        ----------
        system_ids : list(str)
            A list of PPMS system IDs to fetch the bookings for.
        username : str
            The PPMS username to check bookings for.

        Returns
        -------
        int
            The number of deleted bookings that has been processed.
        """
        deleted = PpmsBooking.objects.filter(
            username=username, sync_state="D", system_id__in=system_ids
        )
        if len(deleted) == 0:
            log.debug("⏹🚮🎫 All deleted bookings have been processed!")
            return 0

        num = len(deleted)
        log.info(f"▶🚮🎫 Processing {num} DELETED bookings of 🙋 [{username}]...")
        booking = deleted[0]
        if booking.reservation is None:
            log.info(f"Booking 🎫 is unlinked, deleting it: {booking}")

        else:
            log.debug(f"🚮🎫 Processing deleted booking: {booking}")

            # TODO: review the entire "else" block to make sure we haven't forgotten
            # conditions / edge cases
            res = booking.reservation
            log.debug(f"Linked 🎫🔗🗓  reservation: {res}")
            if booking.t_start == res.t_start and booking.t_end == res.t_end:
                log.info("🗓🚮 Start AND end matching, DELETING reservation...")
                res.delete()
            elif booking.t_end == res.t_end:
                log.info("🗓⏮ End matching, SHORTENING reservation...")
                res.t_end = booking.t_start
                res.save()
            elif booking.t_start == res.t_start:
                log.info("🗓⏭ Start matching, SHIFTING reservation START...")
                res.t_start = booking.t_end
                res.save()
            else:
                self._split_reservation(booking)

        log.success(
            f"🚮🎫✅ Processed booking ({booking.id}), removing it from the DB..."
        )
        # FIXME: this will fail if the booking has been deleted through a FK
        # relation automatically (reservation has been deleted)!
        booking.delete()

        return self._process_deleted_bookings(system_ids, username) + 1

    def _process_deleted_bookings_all(self):
        """Process all bookings having `sync_state` set to `deleted`.

        The method iterates over all users having any booking where `sync_state`
        is set to `deleted` and calls the corresponding method to process those
        bookings for each PPMS supersystem group.

        Returns
        -------
        int
            The total count of processed deleted bookings.
        """
        log.trace("▶🚮🎫Processing 'deleted' bookings...")
        usernames = (
            PpmsBooking.objects.filter(sync_state="D")
            .values_list("username", flat=True)
            .distinct()
        )
        total = 0
        for category, system_ids in self.supersystems.items():
            log.debug(f"Category: {category}")
            cat_total = 0
            for username in usernames:
                num = self._process_deleted_bookings(system_ids, username)
                log.debug(f"⏹🚮🎫 Processed {num} DELETED bookings of {username}...")
                cat_total += num

            if cat_total == 0:
                continue

            total += cat_total
            log.info(
                f"🔄🚮🎫✅ Processed {cat_total} booking updates in state 'deleted' "
                f"for [{category}], IDs {system_ids}."
            )

        return total

    def _process_new_bookings(self, category, system_ids, username):
        """Process `new` bookings of a given user and PPMS supersystem.

        First, the function makes sure the given user doesn't have any bookings
        marked as `deleted`, otherwise processing will be stopped as those ones
        *must* be treated before.

        Then all PPMS-bookings of the user marked as `new` are retrieved which
        are matching the PPMS system IDs making up the "supersystem".

        Next, each of those bookings is compared against *all* reservations to
        decide if the new booking is extending that reservation (shifting the
        reservation's start or end time) or if it's actually overlapping
        (meaning a violation of the no-double-bookings rule).

        In case none of the previous conditions is matching, the booking is
        actually a truly new one that will be used to create a new reservation.

        Eventually (after processing all new bookings), the reservations are
        checked and merged if the updates resulted in adjacent reservations.

        Parameters
        ----------
        category : str
            The name of a category (=delivery group).
        system_ids : list(int)
            The PPMS system IDs making up this category ("supersystem").
        username : str
            The username owning the bookings.
        """
        user = User.objects.get(username=username)

        deleted = PpmsBooking.objects.filter(
            username=username, sync_state="D", system_id__in=system_ids
        ).count()
        if deleted > 0:
            desc = (
                f"User [{username}] is having {deleted} pending bookings in "
                "state 'DELETED', cannot process this user's new bookings!"
            )
            log.error(desc)
            issue = Issue(user=user, description=desc, severity=3)
            issue.save()
            return

        bookings_new = PpmsBooking.objects.filter(
            username=username, sync_state="N", system_id__in=system_ids
        )
        log.debug(f"💫🎫 Processing NEW bookings of 🙋 [{username}]...")

        end = start = double = new = 0
        for booking in bookings_new:
            is_new_reservation = True

            # compare new booking against all existing reservations:
            existing_reservations = Reservation.objects.filter(
                user=username, deliverygroup=category
            )
            for res in existing_reservations:
                # check if booking start matches the end of the reservation:
                if booking.t_start == res.t_end:
                    res.t_end = booking.t_end
                    res.save()
                    log.success(f"🗓⏭  New reservation end: {res}")
                    booking.reservation = res
                    booking.sync_state = "K"
                    booking.save()
                    is_new_reservation = False
                    end += 1
                    break

                # check if booking end matches the start of the reservation:
                if booking.t_end == res.t_start:
                    res.t_start = booking.t_start
                    res.save()
                    log.success(f"🗓⏮  New reservation start: {res}")
                    booking.reservation = res
                    booking.sync_state = "K"
                    booking.save()
                    is_new_reservation = False
                    start += 1
                    break

                # check if booking overlaps with reservation (double-booking):
                if booking.t_start in res.t_range or booking.t_end in res.t_range:
                    log.warning(
                        f"🎫💥 booking [{booking}] overlaps with 🗓  reservation "
                        f"[{res}], NEW booking will be DISCARDED!"
                    )
                    is_new_reservation = False
                    # FIXME: what other actions are needed on double bookings?
                    # - remove entire reservation (if possible)
                    # - add a issue record
                    # - send a user warning, or defer it to the notifications dispatcher
                    double += 1
                    break

            # bookings still not processed are actually NEW reservations:
            if is_new_reservation:
                deliverygroup = DeliveryGroup.objects.get(dg_name=category)
                new_res = Reservation(
                    user=user,
                    deliverygroup=deliverygroup,
                    t_start=booking.t_start,
                    t_end=booking.t_end,
                )
                new_res.save()
                log.success(f"✨🗓 New reservation: {new_res}")
                booking.reservation = new_res
                booking.sync_state = "K"
                booking.save()
                new += 1

        log.debug(f"💫🎫✅ Processed {len(bookings_new)} NEW bookings.")

        # now that all new bookings have been processed we need to check if the
        # new situation is having "adjacent" reservations that should be merged:
        merged = self._merge_reservations_all(username, category)

        return new, start, end, merged, double

    def _process_new_bookings_all(self):
        """Process all bookings having `sync_state` set to `new`."""
        usernames = (
            PpmsBooking.objects.filter(sync_state="N")
            .values_list("username", flat=True)
            .distinct()
        )

        for category, system_ids in self.supersystems.items():
            log.debug(f"Category: {category}, IDs: {system_ids}")
            for username in usernames:
                # TODO: use the returned values on processed bookings:
                self._process_new_bookings(category, system_ids, username)

    def _update_bookings(self, runningsheet, date):
        """Update the DB with PPMS bookings from the given runningsheet and date.

        Parameters
        ----------
        runningsheet : list(pyppms.booking.PpmsBooking)
            The runningsheet retrieved from PPMS.
        date : datetime.datetime
            The date associated to the runningsheet.

        Returns
        -------
        int, int
            A tuple with counts of success / failed updates.
        """
        # first mark all existing bookings for the given date as "deleted"
        PpmsBooking.mark_all_deleted(date)

        okay = fail = skipped = 0

        for booking in runningsheet:
            if booking.system_id not in self.supersystems_ids:
                log.trace(f"⭕🎫 Skipping, system ID not in list: {booking.desc}")
                skipped += 1
                continue

            log.debug(f"🔎🎫 Checking booking in the DB: {booking.desc}")

            d_booking, created = PpmsBooking.objects.get_or_create(
                username=booking.username,
                system_id=booking.system_id,
                t_start=make_aware(booking.starttime),
                t_end=make_aware(booking.endtime),
                # NOTE: we must specify *EXACTLY* those fields that are members
                # of the `UniqueConstraint` of the model
            )
            # now adjust 'sync_state' and possibly other fields that are not part of the
            # constraint:
            # `sync_state` of existing entries has been set to "D" (deleted) by the
            # `mark_all_deleted()` call above, for entries that have been created newly
            # here it will be set to the model's default value "N" (new)
            if not created:
                d_booking.sync_state = "K"
                log.debug("🔄🎫 Refreshed booking (sync_state=known) in the DB.")
            else:
                log.success(f"✨🎫 Created NEW booking in the DB: {d_booking}")
            d_booking.ppms_session = booking.session
            d_booking.save()
            okay += 1

        if skipped:
            log.debug(f"⭕🎫 Skipped {skipped} bookings (system IDs not in list).")

        return okay, fail

    def _update_ppms_user_details(self, username, ppms_name, ppms_group):
        """Update the PPMS details of a user record in the DIOP-DB.

        Parameters
        ----------
        username : str
            The username identifying the record in the DIOP-DB.
        ppms_name : str
            The "PPMS Full Name" to be set for the record.
        ppms_group : str
            The "PPMS Group" to be set for the record.

        Returns
        -------
        int, int
            A tuple with the number of updated and failed users.
        """
        log.debug(
            f"Updating 👩‍🔬👨‍🔬 user record for [{username}] with PPMS details: "
            f"[{ppms_name}]/[{ppms_group}]"
        )
        okay = fail = 0
        try:
            d_user = User.objects.get(username=username)
            if d_user.ppms_fullname != ppms_name or d_user.ppms_group != ppms_group:
                d_user.ppms_fullname = ppms_name
                d_user.ppms_group = ppms_group
                d_user.save()
            okay += 1
        except User.DoesNotExist:
            # this one should explicitly be re-raised, as it indicates some potentially
            # severe underlying problem:
            raise
        except Exception as err:  # pylint: disable-msg=broad-except
            # silence all other exceptions after issuing a warning message:
            log.warning(f"Unexpected exception: {err}")
            fail += 1

        return okay, fail

    def pull_bookings(self, dt=date.today()):
        """Fetch PPMS bookings, put them into the DIOP-DB and process them.

        After pulling all bookings for the given date (using the PPMS
        runningsheet) and putting them into the DIOP-DB, they will be processed
        and the DIOP reservations will be updated accordingly.

        Parameters
        ----------
        dt : datetime.date, optional
            The date for which to fetch bookings, by default `date.today.()`.

        Returns
        -------
        int, int
            A tuple with counts of success / failed booking updates. Please note
            that this doesn't contain any numbers on the changes to
            *reservations* occurring from processing the booking changes!

        Notes
        -----
        For being able to register a new Reservation in the database, the
        corresponding DeliveryGroup has to exist already!
        """
        log.debug(f"▶🔄📋🎫 Pulling PPMS bookings for {dt}...")
        self._populate_name_mapping()
        runningsheet = self.conn.get_running_sheet(
            core_facility_ref=self.cf_ref,
            date=datetime.combine(dt, time.min),
            ignore_uncached_users=True,
            localisation=settings.PYPPMS_LOC_FILTER,
        )
        log.debug(f"Got {len(runningsheet)} bookings for {dt}")
        okay, fail = self._update_bookings(runningsheet, dt)
        log.success(f"⏹🔄📋🎫✅ Fetched {okay} bookings for {dt}.")

        self._process_booking_updates()

        return okay, fail

    def pull_users(self, force_refresh=False):
        """Query PPMS on known users and update the DIOP users table.

        Parameters
        ----------
        force_refresh : bool, optional
            Passed on to `pyppms.ppms.PpmsConnection.get_user()`, by default False.

        Returns
        -------
        int, int
            A tuple with counts of success / failed updates.
        """
        d_users = User.objects.filter(accessgroup_member=True, enabled=True)
        log.debug(
            f"▶🔄👩‍🔬👨‍🔬 Fetching {len(d_users)} active user details from PPMS..."
        )
        ppms_users = []
        for user in d_users:
            try:
                ppms_user = self.conn.get_user(user.username, skip_cache=force_refresh)
                ppms_users.append(ppms_user)
            except KeyError:
                # potentially there are many users that do NOT have an account in the
                # booking system, so we're only trace-logging this:
                log.trace(f"👩‍🔬👨‍🔬 Skipping [{user.username}]: not existing in PPMS!")
        log.debug(f"🔄👩‍🔬👨‍🔬 Got {len(ppms_users)} user details from PPMS.")
        okay = fail = 0
        for ppms_user in ppms_users:
            try:
                u_okay, u_fail = self._update_ppms_user_details(
                    username=ppms_user.username,
                    ppms_name=ppms_user.fullname,
                    ppms_group=ppms_user.ppms_group,
                )
                okay += u_okay
                fail += u_fail
            except Exception as err:  # pylint: disable-msg=broad-except
                log.warning(
                    f"Failed updating PPMS details for [{ppms_user.username}]: {err}"
                )
                fail += 1

        log.debug(f"⏹🔄👩‍🔬👨‍🔬 Finished updating users: okay={okay}, failed={fail}.")
        return okay, fail
