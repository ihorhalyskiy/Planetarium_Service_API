from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from accounts.serializers import UserSerializer


class AccountsUserTest(APITestCase):
    def setUp(self):
        self.email = "email@email.com"
        self.password = "password123"
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
        )

    def test_create_user(self):
        """Test creating a user with an email is successful"""
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_email_unique(self):
        """Test that email is unique"""
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(
                email=self.email,
                password="password123",
            )

    def test_create_user_without_email(self):
        """Test creating a user without an email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="password123")


class AccountsUserSerializerTest(APITestCase):
    def test_serializer_user_create(self):
        payload = {
            "email": "email@email.com",
            "password": "password123",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        serializer = UserSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])

    def test_serializer_user_password_too_short(self):
        payload = {
            "email": "email@email.com",
            "password": "1234567",
        }
        serializer = UserSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors["password"]), 1)
