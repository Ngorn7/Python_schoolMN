from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Subject
from .forms import SubjectForm, SubjectSearchForm


@login_required
def show_subject(request):
    query = request.GET.get('q', '').strip()
    if query:
        subjects = Subject.search_subject(query)
    else:
        subjects = Subject.show_subject()
    form = SubjectSearchForm(initial={'q': query})
    return render(request, 'app_subject/subject_list.html', {
        'subjects': subjects,
        'form': form,
        'query': query,
    })


@login_required
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            Subject.create_subject(**form.cleaned_data)
            messages.success(request, 'Subject created successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'app_subject/subject_form.html', {'form': form, 'title': 'Add Subject'})


@login_required
def update_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject.update_subject(**form.cleaned_data)
            messages.success(request, 'Subject updated successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'app_subject/subject_form.html', {'form': form, 'title': 'Edit Subject'})


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete_subject()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject_list')
    return render(request, 'app_subject/subject_confirm_delete.html', {'subject': subject})
