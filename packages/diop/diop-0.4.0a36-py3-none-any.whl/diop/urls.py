from django.urls import path

from . import views


urlpatterns = [
    path("", views.dg_states, name="index"),
    path("machines/basic/", views.MachineListBasic.as_view(), name="machines_basic"),
    path("machines/", views.MachineList.as_view(), name="machine_list"),
    path("sessions/", views.SessionList.as_view(), name="session_list"),
    path("session/<int:uid>/", views.SessionDetails.as_view(), name="session_details"),
    path("update/<str:item>/", views.update_item, name="update_item"),
    path(
        "issues_unresolved/",
        views.status_issues_unresolved,
        name="status_issues_unresolved",
    ),
    path(
        "last_update/<str:item>/",
        views.last_update_item,
        name="last_update_item",
    ),
    path("ops/", views.OperatorsDash.as_view(), name="operators_dash"),
    path(
        "reservation/<int:id>/",
        views.ReservationDetails.as_view(),
        name="reservation_details",
    ),
]
