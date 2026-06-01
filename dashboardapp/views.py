from django.shortcuts import render

def dashboard(request):

    context = {

        "total_courses": 12,
        "total_quizzes": 50,
        "completed_quizzes": 15,
        "average_score": 82,

        "recent_results": [

            {
                "quiz": "Python Basics",
                "course": "Python",
                "score": 90,
                "date": "20-May-2026"
            },

            {
                "quiz": "HTML Quiz",
                "course": "Web Development",
                "score": 85,
                "date": "18-May-2026"
            },

            {
                "quiz": "SQL Fundamentals",
                "course": "Database",
                "score": 80,
                "date": "15-May-2026"
            },

        ]
    }

    return render(request, "dashboard/dashboard.html", context)
