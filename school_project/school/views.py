from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from .models import (
    Student,
    Teacher,
    SchoolClass,
    Attendance,
    Fee,
    Result,
    StudyMaterial,
    Achievement,
)

from .forms import (
    StudentForm,
    TeacherForm,
    ClassForm,
)


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, 'home.html')


# =========================================================
# ADMIN LOGIN
# =========================================================

def user_login(request):

    if request.user.is_authenticated:

        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')

        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if hasattr(user, 'student_profile'):
                return redirect('student_dashboard')

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'login.html')


# =========================================================
# LOGOUT
# =========================================================

@login_required
def user_logout(request):

    logout(request)

    return redirect('home')


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    students = Student.objects.count()
    teachers = Teacher.objects.count()
    classes = SchoolClass.objects.count()

    today = timezone.localdate()

    present_today = Attendance.objects.filter(
        date=today,
        status='Present'
    ).count()

    unpaid_fees = Fee.objects.filter(
        paid=False
    ).count()

    total_results = Result.objects.count()

    recent_students = (
        Student.objects
        .select_related('school_class', 'user')
        .order_by('-id')[:10]
    )

    recent_results = (
        Result.objects
        .select_related('student')
        .order_by('-id')[:5]
    )

    return render(
        request,
        'dashboard.html',
        {
            'students': students,
            'teachers': teachers,
            'classes': classes,
            'present_today': present_today,
            'unpaid_fees': unpaid_fees,
            'total_results': total_results,
            'recent_students': recent_students,
            'recent_results': recent_results,
        }
    )


# =========================================================
# STUDENTS
# =========================================================

@login_required
def student_list(request):

    students = (
        Student.objects
        .select_related('school_class', 'user')
        .order_by('roll_no')
    )

    return render(
        request,
        'students.html',
        {'students': students}
    )


@login_required
def student_add(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if form.is_valid():

            if not username or not password:

                messages.error(
                    request,
                    'Username and password are required.'
                )

                return render(
                    request,
                    'student_add.html',
                    {'form': form}
                )

            if User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    'Username already exists.'
                )

                return render(
                    request,
                    'student_add.html',
                    {'form': form}
                )

            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data.get('email', '')
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(
                request,
                f'Student {student.name} added successfully.'
            )

            return redirect('students')

    else:

        form = StudentForm()

    return render(
        request,
        'student_add.html',
        {'form': form}
    )


@login_required
def student_edit(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        if form.is_valid():

            form.save()

            if student.user:

                if username:
                    student.user.username = username

                if form.cleaned_data.get('email'):
                    student.user.email = form.cleaned_data.get(
                        'email'
                    )

                if password:
                    student.user.set_password(password)

                student.user.save()

            messages.success(
                request,
                'Student updated successfully.'
            )

            return redirect('students')

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'student_edit.html',
        {
            'form': form,
            'student': student
        }
    )


@login_required
def student_delete(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    name = student.name

    if student.user:
        student.user.delete()

    student.delete()

    messages.success(
        request,
        f'Student {name} deleted successfully.'
    )

    return redirect('students')


# =========================================================
# TEACHERS
# =========================================================

@login_required
def teacher_list(request):

    teachers = Teacher.objects.all().order_by('name')

    return render(
        request,
        'teachers.html',
        {'teachers': teachers}
    )


@login_required
def teacher_add(request):

    if request.method == 'POST':

        form = TeacherForm(request.POST)

        if form.is_valid():

            teacher = form.save()

            messages.success(
                request,
                f'Teacher {teacher.name} added successfully.'
            )

            return redirect('teachers')

    else:

        form = TeacherForm()

    return render(
        request,
        'teacher_add.html',
        {'form': form}
    )


@login_required
def teacher_edit(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == 'POST':

        form = TeacherForm(
            request.POST,
            instance=teacher
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Teacher updated successfully.'
            )

            return redirect('teachers')

    else:

        form = TeacherForm(
            instance=teacher
        )

    return render(
        request,
        'teacher_edit.html',
        {
            'form': form,
            'teacher': teacher
        }
    )


@login_required
def teacher_delete(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    teacher.delete()

    messages.success(
        request,
        'Teacher deleted successfully.'
    )

    return redirect('teachers')


# =========================================================
# CLASSES
# =========================================================

@login_required
def class_list(request):

    classes = (
        SchoolClass.objects
        .annotate(
            student_count=Count('student')
        )
        .order_by('name', 'section')
    )

    return render(
        request,
        'classes.html',
        {'classes': classes}
    )


@login_required
def class_add(request):

    if request.method == 'POST':

        form = ClassForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Class added successfully.'
            )

            return redirect('classes')

    else:

        form = ClassForm()

    return render(
        request,
        'class_add.html',
        {'form': form}
    )


@login_required
def class_edit(request, pk):

    school_class = get_object_or_404(
        SchoolClass,
        pk=pk
    )

    if request.method == 'POST':

        form = ClassForm(
            request.POST,
            instance=school_class
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Class updated successfully.'
            )

            return redirect('classes')

    else:

        form = ClassForm(
            instance=school_class
        )

    return render(
        request,
        'class_edit.html',
        {
            'form': form,
            'school_class': school_class
        }
    )


@login_required
def class_delete(request, pk):

    school_class = get_object_or_404(
        SchoolClass,
        pk=pk
    )

    student_count = Student.objects.filter(
        school_class=school_class
    ).count()

    if student_count > 0:

        messages.error(
            request,
            f'Cannot delete {school_class}. '
            f'{student_count} student(s) are assigned to this class.'
        )

        return redirect('classes')

    school_class.delete()

    messages.success(
        request,
        'Class deleted successfully.'
    )

    return redirect('classes')


# =========================================================
# ATTENDANCE
# =========================================================

@login_required
def attendance_list(request):

    if request.method == 'POST':

        student_id = request.POST.get('student')
        attendance_date = request.POST.get('date')
        status = request.POST.get('status')

        if not student_id or not attendance_date or not status:

            messages.error(
                request,
                'Please fill all attendance fields.'
            )

            return redirect('attendance')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Attendance.objects.update_or_create(
            student=student,
            date=attendance_date,
            defaults={
                'status': status
            }
        )

        messages.success(
            request,
            f'Attendance saved for {student.name}.'
        )

        return redirect('attendance')

    records = (
        Attendance.objects
        .select_related(
            'student',
            'student__school_class'
        )
        .order_by(
            '-date',
            'student__roll_no'
        )
    )

    students = (
        Student.objects
        .select_related('school_class')
        .order_by('roll_no')
    )

    return render(
        request,
        'attendance.html',
        {
            'students': students,
            'records': records,
            'today': timezone.localdate()
        }
    )


# =========================================================
# FEES
# =========================================================

@login_required
def fee_list(request):

    if request.method == 'POST':

        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        paid = request.POST.get('paid') == 'on'

        if not student_id or not amount:

            messages.error(
                request,
                'Please enter student and amount.'
            )

            return redirect('fees')

        try:
            amount = Decimal(amount)

        except InvalidOperation:

            messages.error(
                request,
                'Enter a valid fee amount.'
            )

            return redirect('fees')

        if amount <= 0:

            messages.error(
                request,
                'Fee amount must be greater than zero.'
            )

            return redirect('fees')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Fee.objects.create(
            student=student,
            amount=amount,
            paid=paid
        )

        messages.success(
            request,
            f'Fee added for {student.name}.'
        )

        return redirect('fees')

    fees = (
        Fee.objects
        .select_related(
            'student',
            'student__school_class'
        )
        .order_by('-date', '-id')
    )

    students = (
        Student.objects
        .select_related('school_class')
        .order_by('roll_no')
    )

    return render(
        request,
        'fees.html',
        {
            'fees': fees,
            'students': students
        }
    )


@login_required
def fee_toggle(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    fee.paid = not fee.paid
    fee.save()

    messages.success(
        request,
        'Fee status updated.'
    )

    return redirect('fees')


# =========================================================
# RESULTS
# =========================================================

@login_required
def result_list(request):

    if request.method == 'POST':

        student_id = request.POST.get('student')
        subject = request.POST.get(
            'subject',
            ''
        ).strip()

        marks = request.POST.get('marks')
        total_marks = request.POST.get('total_marks')

        if (
            not student_id
            or not subject
            or marks == ''
            or total_marks == ''
        ):

            messages.error(
                request,
                'Please fill all result fields.'
            )

            return redirect('results')

        try:

            marks = int(marks)
            total_marks = int(total_marks)

        except ValueError:

            messages.error(
                request,
                'Please enter valid marks.'
            )

            return redirect('results')

        if marks < 0 or total_marks <= 0:

            messages.error(
                request,
                'Invalid marks.'
            )

            return redirect('results')

        if marks > total_marks:

            messages.error(
                request,
                'Marks cannot be greater than total marks.'
            )

            return redirect('results')

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Result.objects.create(
            student=student,
            subject=subject,
            marks=marks,
            total_marks=total_marks
        )

        messages.success(
            request,
            f'Result saved for {student.name}.'
        )

        return redirect('results')

    results = (
        Result.objects
        .select_related(
            'student',
            'student__school_class'
        )
        .order_by(
            'student__roll_no',
            'subject'
        )
    )

    students = (
        Student.objects
        .select_related('school_class')
        .order_by('roll_no')
    )

    return render(
        request,
        'results.html',
        {
            'results': results,
            'students': students
        }
    )


# =========================================================
# STUDENT REGISTER
# =========================================================

def student_register(request):

    classes = SchoolClass.objects.all().order_by(
        'name',
        'section'
    )

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        password = request.POST.get('password', '')
        school_class_id = request.POST.get('school_class')

        if not name or not username or not password:

            messages.error(
                request,
                'Name, username and password are required.'
            )

            return render(
                request,
                'student_register.html',
                {'classes': classes}
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return render(
                request,
                'student_register.html',
                {'classes': classes}
            )

        if Student.objects.filter(
            roll_no=roll_no
        ).exists():

            messages.error(
                request,
                'Roll number already exists.'
            )

            return render(
                request,
                'student_register.html',
                {'classes': classes}
            )

        if not school_class_id:

            messages.error(
                request,
                'Please select your class.'
            )

            return render(
                request,
                'student_register.html',
                {'classes': classes}
            )

        school_class = get_object_or_404(
            SchoolClass,
            id=school_class_id
        )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        Student.objects.create(
            user=user,
            name=name,
            roll_no=roll_no,
            email=email,
            phone=phone,
            school_class=school_class
        )

        messages.success(
            request,
            'Student account created successfully.'
        )

        return redirect('student_login')

    return render(
        request,
        'student_register.html',
        {'classes': classes}
    )


# =========================================================
# STUDENT LOGIN
# =========================================================

def student_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if hasattr(user, 'student_profile'):

                login(request, user)

                return redirect(
                    'student_dashboard'
                )

            messages.error(
                request,
                'This account is not a student account.'
            )

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'student_login.html'
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@login_required
def student_dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    attendance = Attendance.objects.filter(
        student=student
    )

    total_days = attendance.count()

    present_days = attendance.filter(
        status='Present'
    ).count()

    absent_days = attendance.filter(
        status='Absent'
    ).count()

    attendance_percentage = 0

    if total_days:

        attendance_percentage = round(
            (present_days / total_days) * 100,
            2
        )

    results = Result.objects.filter(
        student=student
    )

    total_marks = sum(
        r.marks for r in results
    )

    total_possible = sum(
        r.total_marks for r in results
    )

    result_percentage = 0

    if total_possible:

        result_percentage = round(
            (total_marks / total_possible) * 100,
            2
        )

    unpaid_fees = Fee.objects.filter(
        student=student,
        paid=False
    ).count()

    materials_count = StudyMaterial.objects.count()

    achievements_count = Achievement.objects.filter(
        student=student
    ).count()

    return render(
        request,
        'student_dashboard.html',
        {
            'student': student,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'attendance_percentage': attendance_percentage,
            'result_percentage': result_percentage,
            'unpaid_fees': unpaid_fees,
            'materials_count': materials_count,
            'achievements_count': achievements_count,
        }
    )


# =========================================================
# STUDENT ATTENDANCE
# =========================================================

@login_required
def student_attendance(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    records = (
        Attendance.objects
        .filter(student=student)
        .order_by('-date')
    )

    total_days = records.count()

    present_days = records.filter(
        status='Present'
    ).count()

    absent_days = records.filter(
        status='Absent'
    ).count()

    percentage = 0

    if total_days:

        percentage = round(
            (present_days / total_days) * 100,
            2
        )

    return render(
        request,
        'student_attendance.html',
        {
            'student': student,
            'records': records,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'percentage': percentage,
        }
    )


# =========================================================
# STUDENT RESULTS
# =========================================================

@login_required
def student_results(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    results = (
        Result.objects
        .filter(student=student)
        .order_by('subject')
    )

    total_marks = sum(
        r.marks for r in results
    )

    total_possible = sum(
        r.total_marks for r in results
    )

    percentage = 0

    if total_possible:

        percentage = round(
            (total_marks / total_possible) * 100,
            2
        )

    return render(
        request,
        'student_results.html',
        {
            'student': student,
            'results': results,
            'total_marks': total_marks,
            'total_possible': total_possible,
            'percentage': percentage,
        }
    )


# =========================================================
# STUDENT PROGRESS
# =========================================================

@login_required
def student_progress(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    attendance = Attendance.objects.filter(
        student=student
    )

    total_days = attendance.count()

    present_days = attendance.filter(
        status='Present'
    ).count()

    attendance_percentage = 0

    if total_days:

        attendance_percentage = round(
            (present_days / total_days) * 100,
            2
        )

    results = Result.objects.filter(
        student=student
    )

    total_marks = sum(
        r.marks for r in results
    )

    total_possible = sum(
        r.total_marks for r in results
    )

    result_percentage = 0

    if total_possible:

        result_percentage = round(
            (total_marks / total_possible) * 100,
            2
        )

    subjects_evaluated = results.values(
        'subject'
    ).distinct().count()

    return render(
        request,
        'student_progress.html',
        {
            'student': student,
            'attendance_percentage': attendance_percentage,
            'result_percentage': result_percentage,
            'subjects_evaluated': subjects_evaluated,
        }
    )


# =========================================================
# STUDENT FEES
# =========================================================

@login_required
def student_fees(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    fees = (
        Fee.objects
        .filter(student=student)
        .order_by('-date')
    )

    total_fee = sum(
        fee.amount for fee in fees
    )

    paid_fee = sum(
        fee.amount
        for fee in fees
        if fee.paid
    )

    pending_fee = total_fee - paid_fee

    return render(
        request,
        'student_fees.html',
        {
            'student': student,
            'fees': fees,
            'total_fee': total_fee,
            'paid_fee': paid_fee,
            'pending_fee': pending_fee,
        }
    )


# =========================================================
# ADMIN - STUDY MATERIAL LIST
# =========================================================

@login_required
def study_material_list(request):

    materials = (
        StudyMaterial.objects
        .all()
        .order_by('-created_at')
    )

    return render(
        request,
        'study_materials_admin.html',
        {
            'materials': materials
        }
    )


# =========================================================
# ADMIN - ADD STUDY MATERIAL
# =========================================================

@login_required
def study_material_add(request):

    if request.method == 'POST':

        title = request.POST.get(
            'title',
            ''
        ).strip()

        subject = request.POST.get(
            'subject',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        link = request.POST.get(
            'link',
            ''
        ).strip()

        if not title or not subject:

            messages.error(
                request,
                'Title and Subject are required.'
            )

            return render(
                request,
                'study_material_add.html'
            )

        StudyMaterial.objects.create(
            title=title,
            subject=subject,
            description=description,
            link=link
        )

        messages.success(
            request,
            'Study material added successfully.'
        )

        return redirect(
            'study_materials_admin'
        )

    return render(
        request,
        'study_material_add.html'
    )


# =========================================================
# ADMIN - DELETE STUDY MATERIAL
# =========================================================

@login_required
def study_material_delete(request, pk):

    material = get_object_or_404(
        StudyMaterial,
        pk=pk
    )

    material.delete()

    messages.success(
        request,
        'Study material deleted successfully.'
    )

    return redirect(
        'study_materials_admin'
    )


# =========================================================
# STUDENT - STUDY MATERIALS
# =========================================================

@login_required
def student_materials(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    materials = (
        StudyMaterial.objects
        .all()
        .order_by('-created_at')
    )

    return render(
        request,
        'student_materials.html',
        {
            'student': student,
            'materials': materials
        }
    )


# =========================================================
# STUDENT - ACHIEVEMENTS
# =========================================================

@login_required
def student_achievements(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    achievements = (
        Achievement.objects
        .filter(student=student)
        .order_by('-date')
    )

    return render(
        request,
        'student_achievements.html',
        {
            'student': student,
            'achievements': achievements
        }
    )

    # =========================================================
# ADMIN - ACHIEVEMENTS
# =========================================================

@login_required
def achievement_list(request):

    achievements = (
        Achievement.objects
        .select_related(
            'student',
            'student__school_class'
        )
        .order_by('-date', '-id')
    )

    students = (
        Student.objects
        .select_related('school_class')
        .order_by('roll_no')
    )

    return render(
        request,
        'achievements.html',
        {
            'achievements': achievements,
            'students': students,
        }
    )


# =========================================================
# ADMIN - ADD ACHIEVEMENT
# =========================================================

@login_required
def achievement_add(request):

    students = (
        Student.objects
        .select_related('school_class')
        .order_by('roll_no')
    )

    if request.method == 'POST':

        student_id = request.POST.get('student')
        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        if not student_id or not title:

            messages.error(
                request,
                'Please select a student and enter achievement title.'
            )

            return render(
                request,
                'achievement_add.html',
                {
                    'students': students
                }
            )

        student = get_object_or_404(
            Student,
            id=student_id
        )

        Achievement.objects.create(
            student=student,
            title=title,
            description=description
        )

        messages.success(
            request,
            f'Achievement added successfully for {student.name}.'
        )

        return redirect(
            'achievements'
        )

    return render(
        request,
        'achievement_add.html',
        {
            'students': students
        }
    )


# =========================================================
# ADMIN - DELETE ACHIEVEMENT
# =========================================================

@login_required
def achievement_delete(request, pk):

    achievement = get_object_or_404(
        Achievement,
        pk=pk
    )

    achievement.delete()

    messages.success(
        request,
        'Achievement deleted successfully.'
    )

    return redirect(
        'achievements'
    )