from django.shortcuts import render, get_object_or_404
from .models import Quiz


def quiz_list(request):

    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz.html', {'quizzes': quizzes})


def start_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("options")
    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})
