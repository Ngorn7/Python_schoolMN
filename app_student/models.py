from django.db import models


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name='Date of Birth')
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # --- CRUD helper methods (thin wrappers used by the views) ---

    @classmethod
    def create_category(cls, **kwargs):
        """Create a new student record."""
        return cls.objects.create(**kwargs)

    @classmethod
    def show_category(cls, pk=None):
        """Return a single student (if pk given) or all students."""
        if pk is not None:
            return cls.objects.get(pk=pk)
        return cls.objects.all()

    def update_category(self, **kwargs):
        """Update this student's fields and save."""
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()
        return self

    def delete_category(self):
        """Delete this student record."""
        return self.delete()

    @classmethod
    def search_category(cls, query):
        """Search students by first or last name."""
        return cls.objects.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
