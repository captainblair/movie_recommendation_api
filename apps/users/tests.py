from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Test cases for user registration."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/users/'
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'wrongpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='testpass123'
        )
        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTestCase(TestCase):
    """Test cases for user authentication."""
    
    def setUp(self):
        self.client = APIClient()
        self.token_url = '/api/auth/token/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_token_obtain_success(self):
        """Test successful token obtain."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_token_obtain_invalid_credentials(self):
        """Test token obtain with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
