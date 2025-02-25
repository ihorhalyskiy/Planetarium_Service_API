from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from planetarium.models import (
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    ShowSession,
    ShowTheme,
    Ticket,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = [
            "id",
            "name"
        ]


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ShowTheme.objects.all()
    )

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
    capacity = serializers.SerializerMethodField()

    class Meta:
        model = PlanetariumDome
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_capacity(self, obj: PlanetariumDome) -> int:
        return obj.rows * obj.seats_in_row


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
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=[
                    "row",
                    "seat",
                    "show_session"
                ],
                message="This seat is already taken.",
            )
        ]

    def validate(self, data):
        row = data.get("row")
        seat = data.get("seat")
        show_session = data.get("show_session")
        dome = show_session.planetarium_dome
        if not (0 < row < dome.rows):
            raise serializers.ValidationError(
                {"row": f"Row {row} is out of range."}
            )
        if not (0 < seat < dome.seats_in_row):
            raise serializers.ValidationError(
                {"seat": f"Seat {seat} is out of range."}
            )
        if Ticket.objects.filter(row=row, seat=seat).exists():
            raise serializers.ValidationError(
                {"seat": f"Seat {seat} is already taken."}
            )
        return data


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
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=["row", "seat", "show_session"],
                message="This seat is already taken.",
            )
        ]


class TickerRetrieveSerializer(TicketSerializer):
    show_session = ShowSessionRetrieveSerializer()
    reservation = ReservationSerializer()
