from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Student
from .forms import StudentForm, StudentSearchForm


@login_required
def show_category(request):
    """List all students, or filter by search query (?q=...)."""
    query = request.GET.get('q', '').strip()
    if query:
        students = Student.search_category(query)
    else:
        students = Student.show_category()
    form = StudentSearchForm(initial={'q': query})
    return render(request, 'app_student/student_list.html', {
        'students': students,
        'form': form,
        'query': query,
    })


@login_required
def create_category(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            Student.create_category(**form.cleaned_data)
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'app_student/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def update_category(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student.update_category(**form.cleaned_data)
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'app_student/student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required
def delete_category(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete_category()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'app_student/student_confirm_delete.html', {'student': student})
