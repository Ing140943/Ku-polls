"""These module is use for implementation in IndexView class."""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging

logger = logging.getLogger("polls")

class IndexView(generic.ListView):
    """This class is use for be interface of our web application."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions and \
            it is not including those set to be published in the future."""
        # return Question.objects.all() # test for unavailable polls
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """This class create interface for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        # return Question.objects.all() # test for unavailable polls
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    """THis class is create interface of result page."""

    model = Question
    template_name = 'polls/results.html'


@login_required  # (login_url='/accounts/login/')
def vote(request, question_id):
    """Submit the answer to specific question."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "This question is not allowed to vote.")
        return redirect('polls:index')
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        # record the vote
        user = request.user
        # Get the previous
        vote = get_vote_for_user(question, user)
        # case 1: user has not voted for this poll question yet
        #         Create a new Vote object
        if not vote:
            # vote = Vote.objects.create(choice=selected_choice, user=user)
            vote = Vote(user=request.user, choice=selected_choice)
        else:
            # case 2: user has already voted
            #         Modify the existing vote and save it
            vote.choice = selected_choice
        # selected_choice.votes += 1
        # selected_choice.save()
        vote.save()
        logger.info(f"{user} voted in {question}.")
        return HttpResponseRedirect(reverse('polls:results',
                                    args=(question.id,)))

@login_required
def voted(request, question_id):
    """Return the choice that the user selected."""
    question = get_object_or_404(Question, pk=question_id)
    vote = get_vote_for_user(question,request.user)
    
    if not question.can_vote():
        messages.error(request, "You are not allowed to vote this poll")
        return redirect('polls:index')

    if vote:
        return render(request, 'polls/detail.html', {'question': question, "current_choice": vote.choice})
    else: 
        return render(request, 'polls/detail.html', {'question': question,"current_choice": vote})

def get_vote_for_user(question: Question,user: User):
    """Find and return an existing vote for a user on a poll question.

    Returns:
        The user's Vote or None if no vote for this poll_question
        """
    try:
        return Vote.objects.get(user=user, choice__question=question)
    except Vote.DoesNotExist:
        return None
