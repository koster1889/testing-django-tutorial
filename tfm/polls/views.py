# from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Question

def index(request):
    questions = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'questions': questions
    }

    return HttpResponse(template.render(context, request))




def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist...")
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

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
