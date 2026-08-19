from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Student, Teacher, Course, Enrollment, Marks, Attendance


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            elif user.groups.filter(name='Teachers').exists():
                return redirect('/teacher-dashboard/')

            elif user.groups.filter(name='Students').exists():
                return redirect('/student-dashboard/')

            return redirect('/dashboard/')

        return render(
            request,
            'students/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'students/login.html')


@login_required
def dashboard(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    course_count = Course.objects.count()
    enrollment_count = Enrollment.objects.count()

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'enrollment_count': enrollment_count,
    }

    return render(request, 'students/dashboard.html', context)

@login_required
def teacher_dashboard(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    marks = Marks.objects.all()
    attendance = Attendance.objects.all()

    context = {
        'students': students,
        'courses': courses,
        'marks': marks,
        'attendance': attendance,
    }

    return render(
        request,
        'students/teacher_dashboard.html',
        context
    )
@login_required
def add_marks(request):
    enrollments = Enrollment.objects.all()

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment')
        exam_name = request.POST.get('exam_name')
        marks_obtained = request.POST.get('marks_obtained')
        total_marks = request.POST.get('total_marks')

        enrollment = Enrollment.objects.get(id=enrollment_id)

        Marks.objects.create(
            enrollment=enrollment,
            exam_name=exam_name,
            marks_obtained=marks_obtained,
            total_marks=total_marks
        )

        return redirect('/teacher-dashboard/')

    return render(
        request,
        'students/add_marks.html',
        {'enrollments': enrollments}
    )

@login_required
def add_attendance(request):
    enrollments = Enrollment.objects.all()

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment')
        date = request.POST.get('date')
        status = request.POST.get('status')

        enrollment = Enrollment.objects.get(id=enrollment_id)

        Attendance.objects.create(
            enrollment=enrollment,
            date=date,
            status=status
        )

        return redirect('/teacher-dashboard/')

    return render(
        request,
        'students/add_attendance.html',
        {'enrollments': enrollments}
    )

@login_required
def student_dashboard(request):
    marks = Marks.objects.filter(
        enrollment__student__email=request.user.email
    )

    attendance = Attendance.objects.filter(
        enrollment__student__email=request.user.email
    )

    context = {
        'marks': marks,
        'attendance': attendance,
    }

    return render(
        request,
        'students/student_dashboard.html',
        context
    )
def logout_view(request):
    logout(request)
    return redirect('/login/')