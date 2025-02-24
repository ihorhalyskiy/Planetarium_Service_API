from rest_framework import routers

from planetarium.views import (
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    ShowThemeViewSet,
    TicketViewSet,
)


router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("planetarium-domes", PlanetariumDomeViewSet)
router.register("show-sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = router.urls

app_name = "planetarium"