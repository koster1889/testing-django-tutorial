# from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_input = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_input)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.htlm', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def create(request):
    nr_or_poll_options = 5
    
    try:
        new_poll = request.POST
    except:
        new_poll = None
    if new_poll:
        new_question = Question(question_text=new_poll['question-text'])
        options = []
        
        for i in range(nr_or_poll_options):
            option = new_poll['choice-' + str(i)]
            if option:
                options.append(option)

        new_question.pub_date = timezone.now()
        new_question.save()

        for option in options:
            new_choice = Choice(choice_text=option, question=new_question)
            new_choice.save()

        return HttpResponseRedirect(reverse('polls:details', args=(new_question.id,)))
    else:
        return render(request, 'polls/create.html', {'poll_options_list': range(nr_or_poll_options)})
