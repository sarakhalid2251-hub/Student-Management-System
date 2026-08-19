from django.contrib import admin
from .models import Student, Teacher, Course, Enrollment, Attendance, Marks


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'name',
        'email',
        'phone',
        'date_of_birth',
        'enrollment_date',
    )
    search_fields = (
        'student_id',
        'name',
        'email',
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'teacher_id',
        'name',
        'email',
        'phone',
        'subject',
        'joining_date',
    )
    search_fields = (
        'teacher_id',
        'name',
        'email',
        'subject',
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_code',
        'course_name',
        'teacher',
    )
    search_fields = (
        'course_code',
        'course_name',
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'enrollment_date',
    )

    search_fields = (
        'student__name',
        'course__course_name',

    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment',
        'date',
        'status',
    )

    list_filter = (
        'status',
        'date',
    )

    search_fields = (
        'enrollment__student__name',
        'enrollment__course__course_name',
    )

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment',
        'exam_name',
        'marks_obtained',
        'total_marks',
        'percentage',
        'grade',
    )

    search_fields = (
        'enrollment__student__name',
        'enrollment__course__course_name',
        'exam_name',
    )

    def percentage(self, obj):
        return f"{obj.calculate_percentage():.2f}%"

    def grade(self, obj):
        return obj.calculate_grade()