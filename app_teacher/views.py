from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Teacher
from .forms import TeacherForm, TeacherSearchForm


@login_required
def show_teacher(request):
    query = request.GET.get('q', '').strip()
    if query:
        teachers = Teacher.search_teacher(query)
    else:
        teachers = Teacher.show_teacher()
    form = TeacherSearchForm(initial={'q': query})
    return render(request, 'app_teacher/teacher_list.html', {
        'teachers': teachers,
        'form': form,
        'query': query,
    })


@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            subjects = form.cleaned_data.pop('subjects')
            teacher = Teacher.create_teacher(**form.cleaned_data)
            teacher.subjects.set(subjects)
            messages.success(request, 'Teacher created successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'app_teacher/teacher_form.html', {'form': form, 'title': 'Add Teacher'})


@login_required
def update_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            subjects = form.cleaned_data.pop('subjects')
            teacher.update_teacher(**form.cleaned_data)
            teacher.subjects.set(subjects)
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'app_teacher/teacher_form.html', {'form': form, 'title': 'Edit Teacher'})


@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete_teacher()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'app_teacher/teacher_confirm_delete.html', {'teacher': teacher})
