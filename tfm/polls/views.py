# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from django.shortcuts import render

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
    response = "results for question %s " % question_id
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse("Youre voting on question %s." % question_id)
