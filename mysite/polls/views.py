from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def update_question(request, pk):
    """
    Get the list of questions on our website
    """
    questions = Question.objects.get(id=pk)
    serializer = QuestionSerializer(questions, data=request.data, partial=True)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(status=400, data=serializer.errors)

@api_view(['GET'])
def get_questions(request):
    """
    Get the list of questions on our website
    """
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

class IndexView(generic.ListView): # generic.ListView is a generic view that lists objects
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list' 

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView): 
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView): 
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


