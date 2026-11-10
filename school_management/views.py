from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app_student.models import Student
from app_subject.models import Subject
from app_teacher.models import Teacher


@login_required
def dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'subject_count': Subject.objects.count(),
        'teacher_count': Teacher.objects.count(),
    }
    return render(request, 'dashboard.html', context)
