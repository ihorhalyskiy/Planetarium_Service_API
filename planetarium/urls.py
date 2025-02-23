from rest_framework import routers

from django.urls import (
    path,
    include
)

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("show-theme", ShowThemeViewSet)
router.register("astronomy-show", AstronomyShowViewSet)
router.register("planetarium-dome", PlanetariumDomeViewSet)
router.register("show-session", ShowSessionViewSet)
router.register("reservation", ReservationViewSet)
router.register("ticket", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "planetarium"