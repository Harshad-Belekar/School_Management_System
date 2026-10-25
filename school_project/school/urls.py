from django.urls import path
from . import views


urlpatterns = [

    # ================= HOME =================

    path(
        '',
        views.home,
        name='home'
    ),


    # ================= ADMIN LOGIN =================

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),


    # ================= ADMIN DASHBOARD =================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    # ================= STUDENTS =================

    path(
        'students/',
        views.student_list,
        name='students'
    ),

    path(
        'students/add/',
        views.student_add,
        name='student_add'
    ),

    path(
        'students/<int:pk>/edit/',
        views.student_edit,
        name='student_edit'
    ),

    path(
        'students/<int:pk>/delete/',
        views.student_delete,
        name='student_delete'
    ),


    # ================= TEACHERS =================

    path(
        'teachers/',
        views.teacher_list,
        name='teachers'
    ),

    path(
        'teachers/add/',
        views.teacher_add,
        name='teacher_add'
    ),

    path(
        'teachers/<int:pk>/edit/',
        views.teacher_edit,
        name='teacher_edit'
    ),

    path(
        'teachers/<int:pk>/delete/',
        views.teacher_delete,
        name='teacher_delete'
    ),


    # ================= CLASSES =================

    path(
        'classes/',
        views.class_list,
        name='classes'
    ),

    path(
        'classes/add/',
        views.class_add,
        name='class_add'
    ),

    path(
        'classes/<int:pk>/edit/',
        views.class_edit,
        name='class_edit'
    ),

    path(
        'classes/<int:pk>/delete/',
        views.class_delete,
        name='class_delete'
    ),


    # ================= ATTENDANCE =================

    path(
        'attendance/',
        views.attendance_list,
        name='attendance'
    ),


    # ================= FEES =================

    path(
        'fees/',
        views.fee_list,
        name='fees'
    ),

    path(
        'fees/<int:pk>/toggle/',
        views.fee_toggle,
        name='fee_toggle'
    ),


    # ================= RESULTS =================

    path(
        'results/',
        views.result_list,
        name='results'
    ),


    # ================= STUDENT REGISTER / LOGIN =================

    path(
        'student-register/',
        views.student_register,
        name='student_register'
    ),

    path(
        'student-login/',
        views.student_login,
        name='student_login'
    ),

    path(
        'student-dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),


    # ================= STUDENT PAGES =================

    path(
        'student/attendance/',
        views.student_attendance,
        name='student_attendance'
    ),

    path(
        'student/results/',
        views.student_results,
        name='student_results'
    ),

    path(
        'student/progress/',
        views.student_progress,
        name='student_progress'
    ),

    path(
        'student/fees/',
        views.student_fees,
        name='student_fees'
    ),


    # ================= STUDY MATERIALS =================

    path(
        'study-materials/',
        views.study_material_list,
        name='study_materials_admin'
    ),

    path(
        'study-materials/add/',
        views.study_material_add,
        name='study_material_add'
    ),

    path(
        'study-materials/<int:pk>/delete/',
        views.study_material_delete,
        name='study_material_delete'
    ),


    # ================= STUDENT MATERIALS =================

    path(
        'student/materials/',
        views.student_materials,
        name='student_materials'
    ),


    # ================= ADMIN ACHIEVEMENTS =================

    path(
        'achievements/',
        views.achievement_list,
        name='achievements'
    ),

    path(
        'achievements/add/',
        views.achievement_add,
        name='achievement_add'
    ),

    path(
        'achievements/<int:pk>/delete/',
        views.achievement_delete,
        name='achievement_delete'
    ),


    # ================= STUDENT ACHIEVEMENTS =================

    path(
        'student/achievements/',
        views.student_achievements,
        name='student_achievements'
    ),

]