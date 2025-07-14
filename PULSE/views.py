from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from .models import Feedback, Employee, Department
from collections import Counter
from .twilio_utils import send_whatsapp_message
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User, Group

# DRF imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer, DepartmentSerializer

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        print(f"[LOGIN ATTEMPT] Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            django_login(request, user)
            print(f"[LOGIN SUCCESS] {username}")
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            print(f"[LOGIN FAIL] {username}")
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

import sys
sys.path.append(r'c:/Users/USER/Desktop/SCHOOL PROJECTS/PulseTrack/pulsetrack_ai_processor')
from .analyze_feedback import analyze_feedback
from .utils import generate_solution

@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        employee_msg = request.POST.get('Body', '')
        from_number = request.POST.get('From', '')

        # Use centralized AI processor
        analysis = analyze_feedback(employee_msg)
        solution = generate_solution(employee_msg, analysis)

        print(f"New feedback from {from_number}: {employee_msg}")
        print(f"Analysis: {analysis}")
        print(f"Solution: {solution}")

        # Link feedback to Employee if exists
        employee = Employee.objects.filter(phone_number=from_number).first()
        if not employee:
            employee = Employee.objects.create(name="Unknown", phone_number=from_number)
        Feedback.objects.create(
            raw_message=employee_msg,
            sentiment_score=analysis.get('sentiment_score', 0),
            detected_topics=analysis.get('topics', []),
            source_number=from_number,
            solution=solution,
            # Optionally, you could add a ForeignKey to Employee in Feedback for richer linkage
        )

        twilio_response = "Thanks for your feedback! Your feedback is anonymous."
        return HttpResponse(twilio_response, content_type='text/plain')
    return HttpResponse("Invalid request", status=400)

def feedback_data_api(request):
    # Get last 7 days of feedback
    feedbacks = Feedback.objects.filter(
        timestamp__gte=timezone.now() - timezone.timedelta(days=7)
    )

    # Prepare sentiment trend data
    daily_avg = feedbacks.extra(
        select={'day': 'DATE(timestamp)'}
    ).values('day').annotate(avg_sentiment=Avg('sentiment_score'))

    # Count topics
    all_topics = [topic for fb in feedbacks for topic in fb.detected_topics]
    topic_counts = Counter(all_topics).most_common(5)

    # Department-level aggregation
    department_stats = []
    from django.db.models import Prefetch
    employees = Employee.objects.select_related('department').all()
    dept_map = {e.phone_number: (e.department.name if e.department else "Unknown") for e in employees}
    dept_feedback = {}
    for fb in feedbacks:
        dept = dept_map.get(fb.source_number, "Unknown")
        if dept not in dept_feedback:
            dept_feedback[dept] = {'sentiments': [], 'count': 0}
        dept_feedback[dept]['sentiments'].append(fb.sentiment_score)
        dept_feedback[dept]['count'] += 1
    for dept, stats in dept_feedback.items():
        avg_sent = sum(stats['sentiments']) / len(stats['sentiments']) if stats['sentiments'] else 0
        department_stats.append({
            'department': dept,
            'avg_sentiment': avg_sent,
            'feedback_count': stats['count']
        })

    return JsonResponse({
        'dates': [entry['day'] for entry in daily_avg],
        'sentiments': [entry['avg_sentiment'] for entry in daily_avg],
        'topics': [{'name': k, 'count': v} for k, v in topic_counts],
        'departments': department_stats
    })


from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def send_bot_message_api(request):
    # Send a test message to all employees
    employees = Employee.objects.all()
    sent = 0
    failed = []
    for emp in employees:
        try:
            send_whatsapp_message(
                to_number=emp.phone_number,
                template_variables={"1": emp.name or "Employee", "2": "Test message"}
            )
            sent += 1
        except Exception as e:
            failed.append(emp.phone_number)
    return JsonResponse({"sent": sent, "failed": failed})

def send_test_message(request):
    # Example usage
    sid = send_whatsapp_message(
        to_number="+254748264302",
        template_variables={"1": "12/1", "2": "3pm"}
    )
    return HttpResponse(f"Message sent! SID: {sid}")

def is_hr(user):
    return user.groups.filter(name='HR').exists()

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign to HR group if it's the first user
            if User.objects.count() == 1:
                hr_group = Group.objects.get_or_create(name='HR')[0]
                user.groups.add(hr_group)
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import redirect

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_api(request):
    if request.method == 'GET':
        # List all departments for form dropdown
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response({'departments': serializer.data})
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@user_passes_test(is_hr)
def dashboard_view(request):
    return redirect('http://localhost:5173/')
