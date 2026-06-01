from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.result_history,
        name='result_history'
    ),

    path(
        'detail/<uuid:result_id>/',
        views.result_detail,
        name='result_detail'
    ),

]
