from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import student, rooms, RoomAllocation
from django.utils import timezone
import matplotlib.pyplot as plt
import matplotlib
from .forms import studentform
matplotlib.use('Agg')
import numpy as np
from io import BytesIO
from datetime import date
import random
import string
from django.core.mail import send_mail
from .forms import ForgotPasswordForm
from django.contrib.auth import logout
def base(request):
    return render(request, "base.html")  
def members(request):
    return render(request, "homepage.html")  
def admin_dashboard(request):
    return render(request, 'admin.html')

def student_dashboard(request):
    student_id = request.session.get('student_id')
    student_obj = get_object_or_404(student, id=student_id)
    allocation = RoomAllocation.objects.filter(student=student_obj).first()
    return render(request, "student_dashboard.html", {
        "student": student_obj,
        "allocation": allocation
    })

def login_view(request):
    role = request.GET.get("role")
    if not role:
        return redirect('members')

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if role == "admin":
            if username == "admin" and password == "admin123":
                request.session['admin_logged_in'] = True
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid admin credentials")

        elif role == "student":
            try:
                student_obj = student.objects.get(Email=username)
                if password == student_obj.rollno or password == student_obj.password:
                    request.session['student_id'] = student_obj.id
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Invalid student password")
            except student.DoesNotExist:
                messages.error(request, "Invalid student email")

    template = 'adminlogin.html' if role == "admin" else 'stulogin.html'
    return render(request, template, {'role': role})

def forgot(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            hno=form.cleaned_data['hallticketno'].strip()
            try:
                student_obj = student.objects.get(Email=email,rollno=hno)
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                student_obj.password = new_password
                student_obj.save()

                send_mail(
                    subject='Your New Password',
                    message=f"Hello {student_obj.name},\n\nYour new password is: {new_password}\nUse it to log in and change it later.\n\n- Hostel Allocation System",
                    from_email='annadichandana744@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, 'A new password has been sent to your email.')
                return render(request, 'password_reset_done.html')

            except student.DoesNotExist:
                messages.error(request, 'No student found with this email.')
            except Exception as e:
                messages.error(request, 'Error while sending the email.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('base')  

def view_details(request):
    student_id = request.session.get('student_id')
    student_obj = get_object_or_404(student, id=student_id)
    allocation = RoomAllocation.objects.filter(student=student_obj).first()

    tips = [
        "Stay hydrated throughout the day.",
        "Attend all your classes for maximum benefit.",
        "Back up your work regularly.",
        "Use the library for peaceful study.",
        "Don’t forget to network with your batchmates.",
        "Organize your tasks with a planner.",
        "Sleep well before exams — it improves memory!"
    ]

    tip_of_the_day = tips[random.randint(1,7)]

    return render(request, "view_details.html", {
        "student": student_obj,
        "allocation": allocation,
        "tip_of_the_day": tip_of_the_day
    })

def edit_profile(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student_obj = student.objects.get(id=student_id)

    if request.method == "POST":
        student_obj.name = request.POST.get("name")
        student_obj.rollno = request.POST.get("rollno")
        student_obj.branch = request.POST.get("branch")
        student_obj.admission_year = request.POST.get("admission_year")
        student_obj.Email = request.POST.get("email")
        student_obj.phonenumber = request.POST.get("phone")
        student_obj.save()
        return redirect('student_dashboard')

    return render(request, 'edit_profile.html', {'student': student_obj})
def room_info(request):
    student_id = request.session.get('student_id')
    student_obj = get_object_or_404(student, id=student_id)
    allocation = RoomAllocation.objects.filter(student=student_obj).first()
    room = allocation.room if allocation else None
    roommates = RoomAllocation.objects.filter(room=room).exclude(student=student_obj) if room else []
    return render(request, "room_info.html", {
        "student": student_obj,
        "room": room,
        "roommates": roommates
    })
def view_students(request):
    students = student.objects.all()
    student_data = []

    for s in students:
        allocation = RoomAllocation.objects.filter(student=s).first()
        student_data.append({
            'name': s.name,
            'rollno': s.rollno,
            'branch': s.branch,
            'year': s.current_year,
            'email': s.Email,
            'phone': s.phonenumber,
            'room': allocation.room.roomno if allocation else None
        })

    return render(request, 'view_students.html', {'student_data': student_data})
def view_rooms(request):
    all_rooms = rooms.objects.all()
    room_data = [{
        'sno': idx + 1,
        'roomno': room.roomno,
        'occupied': room.occupied,
        'remaining': room.remaining_beds,
        'total': room.totalbeds
    } for idx, room in enumerate(all_rooms)]

    return render(request, 'view_rooms.html', {'rooms': room_data})
def add_room(request):
    if request.method == "POST":
        roomno = request.POST.get("room_no")
        totalbeds = request.POST.get("total_beds")
        rooms.objects.create(roomno=roomno, totalbeds=totalbeds)
        messages.success(request, "Room added successfully")
        return redirect('view_rooms')
    return render(request, 'add_room.html')
def allocate_room(request):
    if request.method == "POST":
        student_ids = request.POST.getlist("student_ids")
        room_id = request.POST.get("room_id")
        if not student_ids or not room_id:
            messages.error(request, "Please select students and a room.")
            return redirect('allocate_room')
        room_obj = get_object_or_404(rooms, id=room_id)
        new_students = []
        already_allocated = []
        for sid in student_ids:
            student_obj = get_object_or_404(student, id=sid)
            if RoomAllocation.objects.filter(student=student_obj).exists():
                already_allocated.append(student_obj.name)
            else:
                new_students.append(student_obj)
        if room_obj.remaining_beds < len(new_students):
            messages.error(request, f"Only {room_obj.remaining_beds} bed(s) available in Room {room_obj.roomno}.")
            return redirect('allocate_room')
        for s in new_students:
            RoomAllocation.objects.create(student=s, room=room_obj, allocated_on=timezone.now())
        if new_students:
            messages.success(request, f"Room allocated to {len(new_students)} student(s).")
        if already_allocated:
            messages.warning(request, f"Skipped already allocated: {', '.join(already_allocated)}")
        return redirect('view_students')  
    allocated_ids = RoomAllocation.objects.values_list('student_id', flat=True)
    students = student.objects.exclude(id__in=allocated_ids)
    rooms_list = [room for room in rooms.objects.all() if room.remaining_beds > 0]
    return render(request, 'allocate_room.html', {
        'students': students,
        'rooms': rooms_list,    
    })
def manage_students(request):
    students = student.objects.all()
    return render(request, 'manage_students.html', {'students': students})
def edit_student(request, student_id=None):
    if student_id:
        student_obj = get_object_or_404(student, id=student_id)
    else:
        student_obj = None

    if request.method == 'POST':
        form = studentform(request.POST, instance=student_obj)
        if form.is_valid():
            form.save()
            return redirect('manage_students')
    else:
        form = studentform(instance=student_obj)

    return render(request, 'edit_student.html', {'form': form, 'student_id': student_id})
def room_overview(request):
    all_rooms = rooms.objects.all()
    room_data = [{
        'sno': idx + 1,
        'id': room.id,
        'roomno': room.roomno,
        'occupied': room.occupied,
        'remaining': room.remaining_beds,
        'status': 'Full' if room.occupied == room.totalbeds else 'Available'
    } for idx, room in enumerate(all_rooms)]
    return render(request, 'roomdetvisual.html', {'rooms': room_data})
def room_chart(request):
    all_rooms = rooms.objects.all().order_by('roomno')
    labels = [room.roomno for room in all_rooms]
    occupied = [room.occupied for room in all_rooms]
    remaining = [room.remaining_beds for room in all_rooms]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width / 2, occupied, width, label='Occupied', color='#ff6666')
    ax.bar(x + width / 2, remaining, width, label='Remaining', color='#66b3ff')
    ax.set_ylabel('Beds')
    ax.set_title('Room Allocation Overview')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='image/png')