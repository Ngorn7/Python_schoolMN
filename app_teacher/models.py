from django.db import models


class Teacher(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    address = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    subjects = models.ManyToManyField('app_subject.Subject', blank=True, related_name='teachers')

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # --- CRUD helper methods ---

    @classmethod
    def create_teacher(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def show_teacher(cls, pk=None):
        if pk is not None:
            return cls.objects.get(pk=pk)
        return cls.objects.all()

    def update_teacher(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()
        return self

    def delete_teacher(self):
        return self.delete()

    @classmethod
    def search_teacher(cls, query):
        return cls.objects.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
