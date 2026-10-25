from django import forms
from .models import Student, Teacher, SchoolClass


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'roll_no', 'email',
            'phone', 'school_class'
        ]


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'name', 'email', 'phone', 'subject'
        ]


class ClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name', 'section']