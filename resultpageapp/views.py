from django.shortcuts import render
from .models import Result


def result_history(request):
    if not request.user.is_authenticated:
        return render(request, 'results/result.html', {'results': []})

    results = Result.objects.filter(
        student=request.user
    ).order_by('-submitted_at')

    return render(
        request,
        'results/result.html',
        {
            'results': results
        }
    )


def result_detail(request, result_id):

    result = Result.objects.get(
        id=result_id
    )

    return render(
        request,
        'results/result.html',
        {
            'result': result
        }
    )
