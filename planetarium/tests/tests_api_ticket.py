import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from planetarium.models import (
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    ShowSession,
    ShowTheme,
    Ticket,
)
from planetarium.serializers import TicketListSerializer


TICKET_URL = reverse("planetarium:ticket-list")


def detail_url(ticket_id):
    return reverse("planetarium:ticket-detail", args=[ticket_id])


def sample_show_theme():
    return ShowTheme.objects.create(name=f"Test theme{uuid.uuid4().hex}")


def sample_astronomy_show(**params):
    defaults = {
        "title": f"Test show {uuid.uuid4().hex}",
        "description": "Test description",
    }
    defaults.update(params)
    astronomy_show = AstronomyShow.objects.create(**defaults)
    astronomy_show.show_theme.add(sample_show_theme().id)
    astronomy_show.save()
    return astronomy_show


def sample_planetarium_dome(**params):
    defaults = {
        "name": f"Test dome {uuid.uuid4().hex}",
        "rows": 2,
        "seats_in_row": 2,
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show_session(**params):
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "planetarium_dome": sample_planetarium_dome(),
        "show_time": datetime.now(),
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def sample_user(**params):
    defaults = {
        "email": f"user_{uuid.uuid4().hex}@user_test.com",
        "password": "password1",
    }
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def sample_reservation(**params):
    defaults = {
        "user": sample_user(),
    }
    defaults.update(params)
    return Reservation.objects.create(**defaults)


def sample_ticket(**params):
    defaults = {
        "row": 1,
        "seat": 1,
        "show_session": sample_show_session(),
        "reservation": sample_reservation(),
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)


class BaseApiTests(APITestCase):
    """This class for cleaning cache after each test"""

    def tearDown(self):
        cache.clear()


class UnauthenticatedTicketTests(BaseApiTests):
    """Test the ticket API for unauthenticated users"""

    def test_auth_required(self):
        res = self.client.get(TICKET_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBusApiTests(BaseApiTests):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="TestPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_ticket_list(self):
        """Test get list of tickets for authenticated user"""
        sample_ticket()
        sample_ticket()
        res = self.client.get(TICKET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)

    def test_filter_ticket_by_show_session_title(self):
        """Test filter tickets by show session title"""
        show_session = sample_show_session()
        ticket1 = sample_ticket(show_session=show_session)
        ticket2 = sample_ticket()
        res = self.client.get(
            TICKET_URL,
            {"title": show_session.astronomy_show.title},
        )
        serializer1 = TicketListSerializer(ticket1)
        serializer2 = TicketListSerializer(ticket2)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_filter_ticket_by_user_email(self):
        """Test filter tickets by user email"""
        reservation = sample_reservation()
        ticket1 = sample_ticket(reservation=reservation)
        ticket2 = sample_ticket()
        res = self.client.get(
            TICKET_URL,
            {"email": reservation.user.email},
        )
        serializer1 = TicketListSerializer(ticket1)
        serializer2 = TicketListSerializer(ticket2)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_retrieve_ticket_with_cache(self):
        ticket1 = sample_ticket()
        cache.set("ticket_view1", ticket1)
        res = self.client.get(TICKET_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        cache_data = cache.get("ticket_view1")
        self.assertIsNotNone(cache_data)

        ticket2 = sample_ticket()
        cache.set("ticket_view2", ticket2)
        cache_data = cache.get("ticket_view2")
        self.assertIsNotNone(cache_data)

    def test_create_ticket_forbidden(self):
        """Test that creating a ticket is forbidden for authenticated users"""
        payload = {
            "row": 1,
            "seat": 1,
            "show_session": sample_show_session().id,
            "reservation": sample_reservation().id,
        }
        res = self.client.post(TICKET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserTicketTests(BaseApiTests):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="TestPass123",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_ticket_successful(self):
        """Test that creating a ticket is successful for admin users"""
        show_session = sample_show_session()
        reservation = sample_reservation()
        payload = {
            "row": 1,
            "seat": 1,
            "show_session": show_session.id,
            "reservation": reservation.id,
        }
        res = self.client.post(TICKET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_with_invalid_data(self):
        """Test that creating a ticket is successful for admin users"""
        show_session = sample_show_session()
        reservation = sample_reservation()
        payload = {
            "row": 1,
            "seat": 1,
            "show_session": show_session.id,
        }
        res = self.client.post(TICKET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_ticket(self):
        """Test that deleting a ticket is successful for admin users"""
        ticket = sample_ticket()
        url = detail_url(ticket.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())