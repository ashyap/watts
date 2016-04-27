from django.shortcuts import render
from .models import Employee, EmployeeLog, Company
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django import forms
from django.shortcuts import render, get_object_or_404
import datetime

def log_in_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user);
            return post_main(request);

@login_required
def logout_view(request):
    logout(request);
    return post_main(request);

@login_required
def post_main(request):
    employees = get_online_employees(request.user.id);
    user = None;
    timeLeft = timedelta(seconds=0);
    checkInButtuonEnabled = True;
    checkOutButtoneEnabled = False;

    if request.user.is_authenticated():
        user = get_employee(request.user.id);
        userCurrentLog = get_employee_log(user.id, datetime.date.today());
        if(userCurrentLog != None):
            if(userCurrentLog.timeIn != None):
                checkInButtuonEnabled = False;
                checkOutButtoneEnabled = True;
                delta = datetime.timedelta(minutes=user.shift);
                endTime = (datetime.datetime.combine(datetime.datetime.now(),userCurrentLog.timeIn) + delta);
                timeLeft = endTime - datetime.datetime.now();
                print(userCurrentLog.timeIn);
                print(endTime);
            if(userCurrentLog.timeOut != None):
                checkInButtuonEnabled = False;
                checkOutButtoneEnabled = False;
            print (user.userType);
    return render(request, 'pages/main.html', {'employees' : employees, 'user' : user, 'checkInButtuonEnabled' : checkInButtuonEnabled,
                                                'checkOutButtoneEnabled' : checkOutButtoneEnabled, 'timeLeft' : timeLeft.total_seconds()});
@login_required
def post_check_in(request):
    if request.user.is_authenticated():
        if(get_employee_log(request.user.id, datetime.date.today()) == None):
            employeeLog = EmployeeLog();
            employeeLog.employeeId = get_employee(request.user.id);
            employeeLog.timeIn = datetime.datetime.now();
            employeeLog.date = datetime.date.today();
            employeeLog.save();
        return post_main(request);

@login_required
def post_check_out(request):
    if request.user.is_authenticated():
        if(get_employee_log(request.user.id, datetime.date.today()) != None):
            employeeLog = EmployeeLog.objects.get(employeeId = request.user.id, date = datetime.date.today());
            employeeLog.timeOut = datetime.datetime.now();
            employeeLog.save();
        return post_main(request);

@login_required
def post_attendance_report(request, userId, startDate=None, endDate=None):
    if request.method == "POST":
        #form = ModelForm(request.Post());
        startDate = request.POST["start"];
        endDate = request.POST["end"];
    else:
        if(endDate == None):
            endDate = datetime.date.today();
        if(startDate == None):
            startDate = endDate - timedelta(days=7);

    if request.user.is_authenticated:
        employeeLogs = get_employee_logs(userId, startDate, endDate);
        employeeHours = [];

    for employeeLog in employeeLogs:
        if employeeLog.timeIn != None and employeeLog.timeOut != None:
            startTime = datetime.datetime.combine(datetime.datetime.now(),employeeLog.timeIn);
            endTime = datetime.datetime.combine(datetime.datetime.now(),employeeLog.timeOut);
            totalHours = endTime - startTime;
            employeeLog.hours = totalHours.total_seconds()/3600;
        else:
            employeeLog.hours = "?";

    return render(request, 'pages/attendance_report.html', {'employeeLogs' : employeeLogs});

@login_required
def post_edit_employee(request, userId):
    employee = get_object_or_404(Employee, pk=userId)
    if request.method == "POST":
        form = EmployeeForm(request.POST,instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return post_main(request);
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'pages/post_edit_employee.html', {'form' : form})

def get_online_employees(employeeId):
    employeeLogs = EmployeeLog.objects.filter(date = datetime.date.today()).exclude(employeeId = employeeId);
    employeeIds = [employee.employeeId.id for employee in employeeLogs];
    presentEmployees = Employee.objects.filter(id__in = employeeIds);
    for employee in presentEmployees:
        employeeLog = get_employee_log(employee.id, datetime.date.today())

        if(employeeLog.timeOut == None):
            employee.isOut = False;
        else:
            employee.isOut = True;
        
    return presentEmployees;

def get_employee(employeeId):
    employee = Employee.objects.get(id = employeeId);
    return employee;

def get_employee_log(employeeId, date):
    try:
        employeeLog = EmployeeLog.objects.get(date = date, employeeId = employeeId);
    except ObjectDoesNotExist:
        employeeLog = None;
    return employeeLog;

def get_employee_logs(employeeId, startDate, endDate):
    try:
        employeeLogs = EmployeeLog.objects.filter(date__range=(startDate, endDate), employeeId = employeeId).order_by('date');
    except ObjectDoesNotExist:
        employeeLogs = None;
    return employeeLogs;
