import datetime

from django.utils import timezone
from polls.models import Question
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


def create_question(question_text, days):
    """Create a question with the given `question_text`."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time)


class AuthenticationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin', email='email@some.domain', password='12345')

    def test_user_have_authenticate(self):
        """Test if user is already authenticate"""
        self.client.post(reverse('login'), {'username': 'admin', 'password': '12345'}, follow=True)
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_have_not_authenticate(self):
        """Test if user is already authenticate"""
        self.client.post(reverse('login'), {'username': 'admins', 'password': '12345'}, follow=True)
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertNotContains(response, "admins")
        self.assertEqual(response.status_code, 200)
