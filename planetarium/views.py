from django.utils import timezone

from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from planetarium.models import (
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    ShowSession,
    ShowTheme,
    Ticket,
)
from planetarium.permissions import (
    IsAdminAllORIsAuthenticatedOrReadOnly,
    IsOwnerOrAdmin
)

from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ReservationSerializer,
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer,
    ShowSessionSerializer,
    ShowThemeSerializer,
    TickerRetrieveSerializer,
    TicketListSerializer,
    TicketSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action in [
            "list",
            "retrieve"
        ]:
            return queryset.prefetch_related(
                "show_theme"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer
        return AstronomyShowSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.prefetch_related(
                "astronomy_show",
                "planetarium_dome"
            )
        if self.action == "retrieve":
            return queryset.prefetch_related(
                "astronomy_show__show_theme",
                "planetarium_dome"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer
        return ShowSessionSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminAllORIsAuthenticatedOrReadOnly,
        IsOwnerOrAdmin
    ]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email"]

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        if self.action == "list":
            return queryset.prefetch_related("user")
        return queryset

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        for ticket in instance.tickets.all():
            time_diff = ticket.show_session.show_time - timezone.now()
            if time_diff.total_seconds() < 5 * 3600:
                raise ValidationError(
                    "Can't delete reservation less than 5 hours before session."
                )
        instance.delete()


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdminAllORIsAuthenticatedOrReadOnly,
        IsOwnerOrAdmin
    ]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "row",
        "seat",
        "reservation__user__email",
        "show_session__astronomy_show__title",
    ]

    @staticmethod
    def _params_to_ints(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        title = self.request.GET.get("title")
        email = self.request.GET.get("email")

        if title:
            queryset = queryset.filter(
                show_session__astronomy_show__title__icontains=title
            )

        if email:
            queryset = queryset.filter(
                reservation__user__email__icontains=email
            )

        if self.action == "list":
            return queryset.select_related(
                "show_session__astronomy_show",
                "reservation__user",
            )
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TickerRetrieveSerializer
        return TicketSerializer
