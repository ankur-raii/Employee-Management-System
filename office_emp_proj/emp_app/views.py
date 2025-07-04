from django.shortcuts import render, HttpResponse
from .models import Employee, Department, Role
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps =  Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'all_emp.html', context)



# def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST('bonus'))
        phone = int(request.POST['phone'])
        # phone = int(phone) if phone and phone.isdigit() else 0  # default to 0 or raise validation error
        # hire_date = request.POST.get('hire_date', '')
        # try:
        #     hire_date = datetime.strptime(hire_date, "%Y-%m-%d").date()
        # except (ValueError, TypeError):
        #     return HttpResponse("Invalid date format. Use YYYY-MM-DD.")
            
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            dept_id=dept,
            role_id=role,
            salary=salary,
            bonus=bonus,
            phone=phone,
            hire_date=datetime.now()  # or use request.POST['hire_date'] if you have a date input
        )
        new_emp.save()
        
        return HttpResponse('Employee added successfully')
    
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse('An Exception Occurred')
    
    
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        dept = int(request.POST.get('dept', 0))
        role = int(request.POST.get('role', 0))
        salary = int(request.POST.get('salary', 0))
        bonus = int(request.POST.get('bonus', 0))
        phone = int(request.POST.get('phone', 0))

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            dept_id=dept,
            role_id=role,
            salary=salary,
            bonus=bonus,
            phone=phone,
            hire_date=datetime.now()
        )
        new_emp.save()
        
        return render(request, 'emp_added.html')
    
    return render(request, 'add_emp.html')



def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return render(request, 'emp_removed.html')
        except Employee.DoesNotExist:
            return HttpResponse('Employee not found')
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')
        emps = Employee.objects.all()
        if name:
            emps= emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        
        context = {
            'emps': emps,
        }
        
        return render(request, 'all_emp.html', context)
    
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')