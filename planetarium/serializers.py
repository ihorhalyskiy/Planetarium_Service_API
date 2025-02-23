from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = [
            "id",
            "name"
        ]


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = [
            "id",
            "title",
            "description",
            "show_theme"
        ]


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_theme = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    show_theme = ShowThemeSerializer(many=True)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        ]


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time"
        ]


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = serializers.CharField(
        source="astronomy_show.title",
        read_only=True
    )
    planetarium_dome = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True
    )


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowRetrieveSerializer()
    planetarium_dome = PlanetariumDomeSerializer()


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.email",
        read_only=True
    )
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "created_at",
            "user"
        ]


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "show_session",
            "reservation"
        ]


class TicketListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="reservation.user.email",
        read_only=True
    )
    astronomy_show = serializers.CharField(
        source="show_session.astronomy_show.title",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "user",
            "astronomy_show"
        ]


class TickerRetrieveSerializer(TicketSerializer):
    show_session = ShowSessionRetrieveSerializer()
    reservation = ReservationSerializer()
