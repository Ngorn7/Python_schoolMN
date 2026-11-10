from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['subject_name']

    def __str__(self):
        return self.subject_name

    # --- CRUD helper methods ---

    @classmethod
    def create_subject(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def show_subject(cls, pk=None):
        if pk is not None:
            return cls.objects.get(pk=pk)
        return cls.objects.all()

    def update_subject(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()
        return self

    def delete_subject(self):
        return self.delete()

    @classmethod
    def search_subject(cls, query):
        return cls.objects.filter(subject_name__icontains=query)
