from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class SchoolClass(models.Model):

    name = models.CharField(max_length=50)

    section = models.CharField(
        max_length=10,
        default='A'
    )

    def __str__(self):
        return f"{self.name} - {self.section}"


class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='student_profile'
    )

    name = models.CharField(
        max_length=100
    )

    roll_no = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT
    )

    admission_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=15
    )

    subject = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Attendance(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent')
        ]
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'],
                name='unique_student_attendance'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.date}"


class Fee(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01)
        ]
    )

    paid = models.BooleanField(
        default=False
    )

    date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - ₹{self.amount}"


class Result(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=100
    )

    marks = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField(
        default=100
    )

    def __str__(self):
        return f"{self.student} - {self.subject}"


# ==============================
# STUDY MATERIAL
# ==============================

class StudyMaterial(models.Model):

    title = models.CharField(
        max_length=200
    )

    subject = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    link = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# ==============================
# ACHIEVEMENT
# ==============================

class Achievement(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.title}"