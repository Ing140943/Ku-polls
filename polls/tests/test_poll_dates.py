"""These module is use for testing the polls."""

import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionModelTests(TestCase):
    """Creating question that test only Model class."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions \
            whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for \
            questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() return True for \
        questions whose pub_date is within the last day."""
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_polls_pass_pub_date(self):
        """Test that the polls already pass the published date."""
        published_date = timezone.now()
        now = timezone.now() + datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=published_date, end_date=now)
        self.assertTrue(question.is_published())

    def test_polls_pass_published_even_pass_the_end_date(self):
        """Test that the polls already pass the published date."""
        published_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end = timezone.now()
        question = Question(pub_date=published_date, end_date=end)
        self.assertTrue(question.is_published())

    def test_polls_not_published_yet(self):
        """Test that the polls already pass the published date."""
        published_date = timezone.now() + \
            datetime.timedelta(days=10, seconds=1)
        question = Question(pub_date=published_date)
        self.assertFalse(question.is_published())

    def test_unavailable_to_vote_expired_polls(self):
        """Test that we can not vote if the polls is expired."""
        end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(end_date=end)
        self.assertFalse(question.can_vote())

    def test_can_not_vote_polls_unpublished_yet(self):
        """Test that the polls already pass the published date."""
        published_date = timezone.now() + datetime.timedelta(days=1, seconds=1)
        now = timezone.now()
        question = Question(pub_date=published_date, end_date=now)
        self.assertFalse(question.can_vote())


def create_question(question_text, days):
    """Create a question with the given `question_text` and published the \
        given number `days` offset to now (negative for questions published \
        in the past, positive for questions that have yet to be published)."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)