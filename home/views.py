import datetime
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from home.models import *
from django.contrib import messages


def signUp(request):
    if request.method == 'GET':
        context = {"Title": "Employee Management | Sign Up"}
        return render(request, "register.html", context)
    elif request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        querySet = User.objects.filter(username=username).values('id')
        if not querySet.exists():
            createUser = User.objects.create_user(username, email, password)
            createUser.first_name = firstName
            createUser.last_name = lastName
            createUser.is_active = True
            createUser.is_staff = True
            createUser.save()
            request.session['userid'] = createUser.id
            request.session['username'] = username
            request.session['password'] = password
            request.session['name'] = createUser.first_name + " " + createUser.last_name
            request.session['superuser'] = False
            Employees.objects.create(user=createUser, work_email=email, job_position="Administration",
                                     is_hr=True, is_manager=True, hiring_date=datetime.now())
        else:
            messages.warning(request, 'Email is already exist')
    response = redirect('logIn')
    return response


def logIn(request):
    if request.method == 'GET':
        checkUserIsLoggedIn = checkLogin(request)
        if checkUserIsLoggedIn:
            return redirect('index')
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            request.session['userid'] = user.id
            request.session['username'] = username
            request.session['password'] = password
            request.session['name'] = user.first_name + " " + user.last_name
            if user.is_superuser:
                request.session['superuser'] = True
            else:
                request.session['superuser'] = False
            try:
                e = Employees.objects.get(user=user)
                hr = e.is_hr
                manager = e.is_manager
            except:
                hr = False
                manager = False
            request.session['isHr'] = hr
            request.session['isManager'] = manager
        return redirect('index')
    else:
        return redirect('login/?msg=Invalid credentials')


def logOut(request):
    checkUserIsLoggedIn = checkLogin(request)
    if checkUserIsLoggedIn:
        del request.session['userid']
        del request.session['username']
        del request.session['password']
        del request.session['superuser']
        del request.session['name']
        del request.session['isHr']
        del request.session['isManager']
        request.session.modified = True
        response = redirect('/')
        return response
    else:
        return redirect('login')


def checkLogin(request):
    log = False
    try:
        username = request.session['username']
        password = request.session['password']
        user = authenticate(request, username=username, password=password)
        if user:
            log = True
    except:
        log = False
    return log


def index(request):
    chkLogin = checkLogin(request)
    if chkLogin:
        context = {"Title": "Dashboard"}
        return render(request, 'dashboard.html', context)
    else:
        return redirect('logIn')


def employeesOverview(request):
    chkLogin = checkLogin(request)
    if chkLogin:
        emp = Employees.objects.all()
        context = {"Title": "Employees Overview", "employees": emp}
        return render(request, 'employeesOverview.html', context)
    else:
        return redirect('logIn')


def createEmployee(request):
    if request.method == 'GET':
        chkLogin = checkLogin(request)
        if request.session['isHr'] or request.session['isManager']:
            if chkLogin:
                context = {"Title": "Create Employee"}
                return render(request, 'editEmployee.html', context)
            else:
                return redirect('logIn')
        else:
            errorHandler = {"Access Denied"}
            return errorHandler
    elif request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        querySet = User.objects.filter(username=username).values('id')
        if not querySet.exists():
            createUser = User.objects.create_user(username, email, password)
            createUser.first_name = firstName
            createUser.last_name = lastName
            createUser.is_active = True
            createUser.is_staff = True
            createUser.save()
            jobPosition = request.POST['jobPosition']
            hiringDate = request.POST['hiringDate']
            description = request.POST['description']
            emp = Employees.objects.create(user=createUser, work_email=email, job_position=jobPosition,
                                           hiring_date=hiringDate, description=description, is_hr=False,
                                           is_manager=False)
            return redirect("editEmployee", emp.id)


def editEmployee(request, pk):
    checkUserIsLoggedIn = checkLogin(request)
    if checkUserIsLoggedIn:
        if request.method == 'GET':
            data = Employees.objects.get(id=pk)
            context = {"Title": "Edit Employee", "data": data}
            return render(request, 'editEmployee.html', context)
        elif request.method == 'POST':
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            email = request.POST['email']
            jobPosition = request.POST['jobPosition']
            hiringDate = request.POST['hiringDate']
            description = request.POST['description']
            password = request.POST['password']
            editEmployee = Employees.objects.get(id=pk)
            user = User.objects.get(id=editEmployee.user.id)
            editEmployee.user = user
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.set_password(password)
            user.username = email
            editEmployee.work_email = email
            editEmployee.job_position = jobPosition
            editEmployee.hiring_date = hiringDate
            editEmployee.description = description
            editEmployee.save()
            user.save()
            return redirect("editEmployee", editEmployee.id)


def leavesOverview(request):
    chkLogin = checkLogin(request)
    if chkLogin:
        if request.session['isHr'] or request.session['isManager']:
            leaves = LeavesRequest.objects.all()
        else:
            user = request.session['userid']
            employee = Employees.objects.get(user=user)
            leaves = LeavesRequest.objects.filter(user=employee)
        context = {"Title": "Leaves Overview", "leaves": leaves}
        return render(request, 'leavesOverview.html', context)
    else:
        return redirect('logIn')


def createLeave(request):
    if request.method == 'GET':
        chkLogin = checkLogin(request)
        if chkLogin:
            context = {"Title": "Apply Leave"}
            return render(request, 'editLeave.html', context)
        else:
            return redirect('logIn')
    elif request.method == 'POST':
        user = request.session['userid']
        employee = Employees.objects.get(user=user)
        durationFrom = request.POST['durationFrom']
        durationTo = request.POST['durationTo']
        applyLeave = LeavesRequest.objects.create(user=employee, duration_from=durationFrom, duration_to=durationTo,
                                                  status="Pending")
        return redirect("editLeave", applyLeave.id)


def editLeave(request, pk):
    checkUserIsLoggedIn = checkLogin(request)
    if checkUserIsLoggedIn:
        if request.method == 'GET':
            data = LeavesRequest.objects.get(id=pk)
            context = {"Title": "Edit Leave", "data": data}
            return render(request, 'editLeave.html', context)
        elif request.method == 'POST':
            durationFrom = request.POST['durationFrom']
            durationTo = request.POST['durationTo']
            status = request.POST['status']
            editLeave = LeavesRequest.objects.get(id=pk)
            editLeave.duration_from = durationFrom
            editLeave.duration_to = durationTo
            editLeave.status = status
            editLeave.save()
            return redirect("editLeave", editLeave.id)
