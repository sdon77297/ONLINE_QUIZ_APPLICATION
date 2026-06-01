from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.quiz_list,
        name='quiz_list'
    ),

    path(
        'start/<uuid:quiz_id>/',
        views.start_quiz,
        name='start_quiz'
    ),

]
