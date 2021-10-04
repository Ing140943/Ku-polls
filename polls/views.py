"""These module is use for implementation in IndexView class."""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


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


def vote(request, question_id):
    """Submit the answer to specific question."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "This question is not allowed to vote.")
        return redirect('polls:index')
    else:
        try:
            selected_choice = \
                question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice."
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            messages.success(request,
                             "Your choice successfully recorded. Thank you.")
            return HttpResponseRedirect(reverse('polls:results',
                                                args=(question.id,)))
