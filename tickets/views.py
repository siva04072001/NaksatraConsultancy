from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import tickets
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import render_to_string
from datetime import datetime, date, timedelta
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from helpdesk import settings
from django.contrib.auth import get_user_model
from celery import shared_task

# Create your views here.

#home page
def index(request):
    return render(request, 'index.html')

def registers(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            userId = form.cleaned_data.get('userId')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            designation=form.cleaned_data.get('designation')
            msg = 'user created'
            mydict = {'username': username,'password':password,'email':email,'designation':designation}

            html_template = 'ackemail.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome to Service Desk'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

            return redirect('registers')
    

        else:
            msg = 'form is not valid'
        return render('superadmin/sucess.html')


    else:
        form = SignUpForm()
    return render(request,'login/registers.html', {'form': form, 'msg': msg})

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            userId = form.cleaned_data.get('userId')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            designation=form.cleaned_data.get('designation')
            msg = 'user created'
            mydict = {'username': username,'password':password,'email':email,'designation':designation}

            html_template = 'register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome to Service Desk'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

            return redirect('register')
    

        else:
            msg = 'form is not valid'
        return render('superadmin/sucess.html')


    else:
        form = SignUpForm()
    return render(request,'superadmin/register.html', {'form': form, 'msg': msg})


#login user
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superadmin and user.is_authorized=="True":
                login(request, user)
                return redirect('superadmin')
            elif user is not None and user.is_admin and user.is_authorized=="True":
                login(request, user)
                return redirect('admin')
            elif user is not None and user.is_engineer and user.is_authorized=="True":
                login(request, user)
                return redirect('engineer')
            elif user is not None and user.is_employee and user.is_authorized=="True":
                login(request, user)
                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login/login.html', {'form': form, 'msg': msg})

#logout user
def logout_view(request):
    logout(request)
    return redirect('/login')

#enter superadmin after login
@login_required(login_url='login')
def superadmin(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            userId = form.cleaned_data.get('userId')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            designation=form.cleaned_data.get('designation')
            msg = 'user created'
            mydict = {'username': username,'password':password,'email':email,'designation':designation}

            html_template = 'register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome to Service Desk'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

            return redirect('register')


        else:
            msg = 'form is not valid'
        return render('superadmin/sucess.html')


    else:
        form = SignUpForm()
    return render(request,'superadmin/register.html', {'form': form, 'msg': msg})

#super admin user view page
@login_required(login_url='login')
def superadminview(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            user=User.objects.all()
        return render(request, 'superadmin/superadminview.html',{"user": user})

    else:
        return render(request, 'login/login.html', {})

#admin page after login
@login_required(login_url='login')
def admin(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=Tickets.objects.all()
            tickets_count=tickets.count()
            closedticket=Tickets.objects.filter(status = 'closed')
            closedtickets=closedticket.count()
            assignedticket=Tickets.objects.filter(status ='assigned')
            assignedtickets=assignedticket.count()
            todoticket=Tickets.objects.filter(status ='To Do')
            todotickets=todoticket.count()
            onticket=Tickets.objects.filter(status ='On Progress')
            ontickets=onticket.count()
            testticket=Tickets.objects.filter(status ='Testing')
            testtickets=testticket.count()
            compticket=Tickets.objects.filter(status ='Completed')
            comptickets=compticket.count()
            activetickets=comptickets+testtickets+ontickets+todotickets+assignedtickets

        return render(request, 'admin/admindash.html',{
            "tickets":tickets,
        "tickets_count":tickets_count,
        "closedtickets":closedtickets,
        "assignedtickets":assignedtickets,
        "todotickets":todotickets,
        "ontickets": ontickets,
        "testtickets":testtickets,
        "comptickets":comptickets,
        "activetickets":activetickets})

    else:
        return render(request, 'login/login.html', {})


#engineer dash page after login
@login_required(login_url='login')
def engineerdash(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:

            closedticket=Tickets.objects.filter(status = 'closed', assigned=request.user)
            closedtickets=closedticket.count()
            assignedticket=Tickets.objects.filter(status ='assigned', assigned=request.user)
            assignedtickets=assignedticket.count()
            todoticket=Tickets.objects.filter(status ='To Do', assigned=request.user)
            todotickets=todoticket.count()
            onticket=Tickets.objects.filter(status ='On Progress', assigned=request.user)
            ontickets=onticket.count()
            testticket=Tickets.objects.filter(status ='Testing', assigned=request.user)
            testtickets=testticket.count()
            compticket=Tickets.objects.filter(status ='Completed', assigned=request.user)
            comptickets=compticket.count()
            totalticket=Tickets.objects.filter(status ='Unassigned', assigned=request.user)
            totaltickets=totalticket.count()
            activetickets=comptickets+testtickets+ontickets+todotickets+assignedtickets
            tickets_count=activetickets+totaltickets

        return render(request, 'engineer/engineerdash.html',{
            "tickets":tickets,
            "tickets_count":tickets_count,
        "closedtickets":closedtickets,
        "assignedtickets":assignedtickets,
        "todotickets":todotickets,
        "ontickets": ontickets,
        "testtickets":testtickets,
        "comptickets":comptickets,
        "activetickets":activetickets})

    else:
        return render(request, 'login/login.html', {})

#employee dash page after login
@login_required(login_url='login')
def employeedash(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:

            closedticket=Tickets.objects.filter(status = 'closed', username=request.user)
            closedtickets=closedticket.count()
            assignedticket=Tickets.objects.filter(status ='assigned', username=request.user)
            assignedtickets=assignedticket.count()
            todoticket=Tickets.objects.filter(status ='To Do', username=request.user)
            todotickets=todoticket.count()
            onticket=Tickets.objects.filter(status ='On Progress', username=request.user)
            ontickets=onticket.count()
            testticket=Tickets.objects.filter(status ='Testing', username=request.user)
            testtickets=testticket.count()
            compticket=Tickets.objects.filter(status ='Completed', username=request.user)
            comptickets=compticket.count()
            totalticket=Tickets.objects.filter(status ='Unassigned', username=request.user)
            totaltickets=totalticket.count()
            activetickets=comptickets+testtickets+ontickets+todotickets+assignedtickets
            tickets_count=activetickets+totaltickets

        return render(request, 'employee/employeedash.html',{
            "tickets":tickets,
            "tickets_count":tickets_count,
        "closedtickets":closedtickets,
        "assignedtickets":assignedtickets,
        "todotickets":todotickets,
        "ontickets": ontickets,
        "testtickets":testtickets,
        "comptickets":comptickets,
        "activetickets":activetickets})

    else:
        return render(request, 'login/login.html', {})



#admindash board page after login
@login_required(login_url='login')
def admintable(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=Tickets.objects.filter(expired=False)
            tickets_count=tickets.count()
            closedticket=Tickets.objects.filter(status = 'closed')
            closedtickets=closedticket.count()
            assignedticket=Tickets.objects.filter(status ='assigned')
            assignedtickets=assignedticket.count()
            todoticket=Tickets.objects.filter(status ='To Do')
            todotickets=todoticket.count()
            onticket=Tickets.objects.filter(status ='On Progress')
            ontickets=onticket.count()
            testticket=Tickets.objects.filter(status ='Testing')
            testtickets=testticket.count()
            compticket=Tickets.objects.filter(status ='Completed')
            comptickets=compticket.count()
            activetickets=comptickets+testtickets+ontickets+todotickets+assignedtickets
            paginator=Paginator(tickets,5)
            page_number=request.GET.get('page')
            tickets_pager=paginator.get_page(page_number)
        return render(request, 'admin/admin.html',{
            "tickets":tickets,
        "tickets_count":tickets_count,
        "closedtickets":closedtickets,
        "assignedtickets":assignedtickets,
        "todotickets":todotickets,
        "ontickets": ontickets,
        "testtickets":testtickets,
        "comptickets":comptickets,
        "activetickets":activetickets,
        })

    else:
        return render(request, 'login/login.html', {})

#stats
@login_required(login_url='login')
def stats(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            department=Department.objects.all()
            location=Location.objects.all()
            subdivision=Subdivision.objects.all()
            item=Item.objects.all()
            return render(request, 'admin/stats.html',{'department':department,'location':location,'subdivision':subdivision,'item':item
            })

#admin details page
@login_required(login_url='login')
def admindetail_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'admin/admin_detail.html', context)

#admin details page
@login_required(login_url='login')
def dept(request):
    cat=request.POST['cat']
    department=Department.objects.all()
    location=Location.objects.all()
    subdivision=Subdivision.objects.all()
    item=Item.objects.all()      
    reg =Department(cat=cat)
    reg.save()
    return render(request, 'admin/stats.html',{'department':department,'location':location,'subdivision':subdivision,'item':item})

@login_required(login_url='login')
def loca(request):
    loc=request.POST['loc']
    department=Department.objects.all()
    location=Location.objects.all()
    subdivision=Subdivision.objects.all()
    item=Item.objects.all()      
    reg =Location(loc=loc)
    reg.save()
    return render(request, 'admin/stats.html',{'department':department,'location':location,'subdivision':subdivision,'item':item})

@login_required(login_url='login')
def subd(request):
    sub=request.POST['sub']
    department=Department.objects.all()
    location=Location.objects.all()
    subdivision=Subdivision.objects.all()
    item=Item.objects.all()      
    reg =Subdivision(sub=sub)
    reg.save()
    return render(request, 'admin/stats.html',{'department':department,'location':location,'subdivision':subdivision,'item':item})

@login_required(login_url='login')
def itm(request):
    ite=request.POST['ite']
    department=Department.objects.all()
    location=Location.objects.all()
    subdivision=Subdivision.objects.all()
    item=Item.objects.all()      
    reg =Item(ite=ite)
    reg.save()
    return render(request, 'admin/stats.html',{'department':department,'location':location,'subdivision':subdivision,'item':item})

#admin profile page after login
@login_required(login_url='login')
def adminprofile(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=User.objects.all()

        return render(request, 'admin/adminprofile.html',{"tickets":tickets})

    else:
        return render(request, 'login/login.html', {})

#admin user detail1
@login_required(login_url='login')
def userdetail(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=User.objects.all()
            
        return render(request, 'admin/userdetail.html',{"tickets":tickets})

    else:
        return render(request, 'login/login.html', {})

#employee detail2
@login_required(login_url='login')
def admininfo_ticket(request,userId):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=User.objects.get(userId=userId)
        return render(request, 'admin/user_info.html',{"tickets":tickets})

    else:
        return render(request, 'login/login.html', {})

#closed ticket section in admin page
@login_required(login_url='login')
def adminclosed(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            ticket=Tickets.objects.all()
            p=Paginator(Tickets.objects.all(), 10)
            page=request.GET.get('page')
            tickets=p.get_page(page)
        return render(request, 'admin/adminclosed.html',{"ticket": ticket, "tickets":tickets})

    else:
        return render(request, 'login/login.html', {})

#engineer status page
@login_required(login_url='login')
def adminexpired(request):
    if request.user.is_authenticated:
        ticket=Tickets.objects.filter(~Q(status='closed'),expired=True)
        p=Paginator(ticket,6)
        page_number=request.GET.get('page')
        ticketfinal=p.get_page(page_number)
        return render(request, 'admin/admin_expired.html', {"ticket": ticketfinal, "page_number": page_number})

    else:
        return render(request, 'login/login.html', {})


#engineer page after login
@login_required(login_url='login')
def engineer(request):
    if request.user.is_authenticated:
        return render(request,'engineer/engineer.html')
    else:
        return render(request, 'login/login.html', {})

#employee page after login
@login_required(login_url='login')
def employee(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        dept=Department.objects.all()
        loc=Location.objects.all()
        sub=Subdivision.objects.all()
        ite=Item.objects.all()

        return render(request,'employee/employee.html' ,{"ticket": ticket, "dept":dept, "loc":loc, "sub":sub, "ite":ite})

    else:
        return render(request, 'login/login.html', {})

#employee status page
@login_required(login_url='login')
def statusticket(request):
    if request.user.is_authenticated:
        ticket=Tickets.objects.filter(~Q(status='closed'), username=request.user)
        p=Paginator(ticket,6)
        page_number=request.GET.get('page')
        ticketfinal=p.get_page(page_number)
        return render(request, 'employee/employee_status.html',{"ticket": ticketfinal, "page_number": page_number})

    else:
        return render(request, 'login/login.html', {})

#employee details page
@login_required(login_url='login')
def empdetail_ticket(request,Id):
    emp=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'emp':emp
    }
    return render(request, 'employee/employee_detail.html', context)

#engineer status page
@login_required(login_url='login')
def engineerticket(request):
    if request.user.is_authenticated:
        ticket=Tickets.objects.filter(~Q(status='closed'), assigned=request.user, expired=False)
        p=Paginator(ticket,6)
        page_number=request.GET.get('page')
        ticketfinal=p.get_page(page_number)
        return render(request, 'engineer/engineer.html', {"ticket": ticketfinal, "page_number": page_number})

    else:
        return render(request, 'login/login.html', {})

#engineer ticket closed page
@login_required(login_url='login')
def engineerticketclosed(request):
    if request.user.is_authenticated:


        ticket=Tickets.objects.filter(assigned=request.user)
        return render(request, 'engineer/engineerclosed.html', {"ticket": ticket})

    else:
        return render(request, 'login/login.html', {})

#admin closed ticket page
@login_required(login_url='login')
def close_ticket(request,Id):
    tickets=Tickets.objects.all()
    item=Tickets.objects.get(Id=Id)
    item.status="closed"
    item.save()
    context={
        'item':item,
        'tickets':tickets
    }
    messages.info(request,"Ticket Updated")
    return render(request, 'admin/admin.html', context)

#admin edit page
@login_required(login_url='login')
def assign_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'admin/adminedit.html', context)

#engineer report
@login_required(login_url='login')
def engreport(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'engineer/engreport.html', context)

#employee report
@login_required(login_url='login')
def empreport(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'employee/empreport.html', context)

#admin Report
@login_required(login_url='login')
def adminreport(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'admin/adminreport.html', context)

#super admin edit user page
@login_required(login_url='login')
def assign_user(request,Id):
    item=User.objects.get(userId = Id)
    context={
        'item':item
    }
    return render(request, 'superadmin/superadminedit.html', context)

#super admin update user process
@login_required(login_url='login')
def update_user(request,Id):

    item=User.objects.get(userId=Id)
    email=request.POST['email']
    mobNo=request.POST['mobNo']
    address=request.POST['address']
    designation=request.POST['designation']
    is_admin=request.POST['is_admin']
    is_engineer=request.POST['is_engineer']
    is_employee=request.POST['is_employee']
    reg =User(email=email,mobNo=mobNo,address=address,designation=designation,
    is_admin=is_admin,is_engineer=is_engineer,is_employee=is_employee)
    reg.save()
    context={
        'item':item,


    }
    messages.info(request,"Ticket Updated")
    return render(request, 'superadmin/superadminedit.html', context)

#super admin delete user
@login_required(login_url='login')
def delete_user(request,Id):

    item=User.objects.get(userId=Id)

    item.delete()

    messages.info(request,"user deleted")
    user=User.objects.all()
    p=Paginator(User.objects.all(), 10)
    page=request.GET.get('page')
    users=p.get_page(page)
    return render(request, 'superadmin/superadminview.html',{"user": user, "users":users})

#superadmin update user process
@login_required(login_url='login')
def update_user(request,Id):

    item=User.objects.get(userId=Id)
    item.email=request.POST['email']
    item.mobNo=request.POST['mobNo']
    item.address=request.POST['address']
    item.designation=request.POST['designation']
    item.save()
    context={
        'item':item

    }
    messages.info(request,"User Updated")
    return render(request, 'superadmin/superadminedit.html', context)

#admin update ticket process
@login_required(login_url='login')
def update_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item.due_date=request.POST['due_date']
    item.admindesc=request.POST['admindesc']
    item.assigned=request.POST['assigned']
    item.status="assigned"
    item.expired=False
    
    item.save()
    
    assigned=item.assigned
    name=item.username
    queries=item.queries
    location=item.location
    due_date=item.due_date
    mydict = {'Id':Id, 'username': name, 'assigned': assigned, 'queries':queries,'location':location, 'due_date':due_date}
    users= get_user_model().objects.filter(Q(username=assigned) | Q(username=name))
    for user in users:
        to_email=user.email
        html_template = 'assigned.html'
        html_message = render_to_string(html_template, context=mydict)
        subject = 'Ticket is Assigned...'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        message = EmailMessage(subject, html_message,email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
    context={
        'item':item,
        'eng':eng

    }
    messages.info(request,"Ticket Assigned")
    return render(request, 'admin/adminedit.html', context)

#engineer status page
@login_required(login_url='login')
def engassign_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'engineer/engineer_status.html', context)

#engineer details page
@login_required(login_url='login')
def engdetail_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'engineer/engineer_detail.html', context)

#admin status grant update process
@login_required(login_url='login')
def adminupdate_grant(request,userId):
    tickets=User.objects.get(userId=userId)
    tickets.is_authorized="True"
    email=tickets.email
    username=tickets.username
    password=tickets.password
    designation=tickets.designation
    tickets.save()
    mydict = {'username': username,'password':password, 'email':email,'designation':designation}

    html_template = 'grant_email.html'
    html_message = render_to_string(html_template, context=mydict)
    subject = 'Welcome to Service Desk'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    message = EmailMessage(subject, html_message,email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()

    context={
        'tickets':tickets

    }
    
    return render(request, 'admin/userdetail.html', context)

#admin status revoke update process
@login_required(login_url='login')
def adminupdate_revoke(request,userId):
    tickets=User.objects.get(userId=userId)
    tickets.is_authorized="False"
    email=tickets.email
    username=tickets.username
    password=tickets.password
    designation=tickets.designation
    tickets.save()
    mydict = {'username': username,'password':password, 'email':email,'designation':designation}

    html_template = 'revoke_email.html'
    html_message = render_to_string(html_template, context=mydict)
    subject = 'Welcome to Service Desk'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    message = EmailMessage(subject, html_message,email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()
    context={
        'tickets':tickets

    }
    
    return render(request, 'admin/userdetail.html', context)

#engineer update process
@login_required(login_url='login')
def engupdate_ticket(request,Id):
    item=Tickets.objects.get(Id=Id)
    item.issueReport=request.POST['issueReport']
    item.problemDesc=request.POST['problemDesc']
    item.causeProb=request.POST['causeProb']
    item.solGiven=request.POST['solGiven']
    item.notes=request.POST['notes']
    item.save()
    eng=User.objects.get(username=item.assigned)
    context={
        'item':item,
        'eng':eng

    }
    messages.info(request,"Ticket Updated")
    return render(request, 'engineer/engineer.html', context)

#engineer update status
@login_required(login_url='login')
def engupdate_status(request,Id):
    item=Tickets.objects.get(Id=Id)
    item.status=request.POST['status']
    item.save()
    eng=User.objects.get(username=item.assigned)
    context={
        'item':item,
        'eng':eng

    }
    messages.info(request,"Ticket Updated")
    return render(request, 'engineer/engineer_detail.html', context)

#new ticket user page
@login_required(login_url='login')
def userticket(request):
    if request.user.is_authenticated:
        dept=Department.objects.all()
        loc=Location.objects.all()
        sub=Subdivision.objects.all()
        ite=Item.objects.all()
        if request.method == 'POST':

            username=request.user
            category=request.POST["category"]
            location=request.POST["location"]
            subfactory=request.POST["subfactory"]
            item=request.POST["item"]
            queries=request.POST["queries"]
            Description=request.POST["Description"]
            mobileNo=request.POST["mobileNo"]
            mail=request.user.email
            priority=request.POST["priority"]
            uploadFile=request.FILES['file']
            status="Unassigned"
            assigned="Unassigned"
            assigned_date=date.today()
            
            if item == 'others':
                activateitem='True'
                item=request.POST['itemothers']


            ticket= Tickets(username=username,category=category,location=location,subfactory=subfactory,item=item,
            queries=queries,Description=Description,mobileNo=mobileNo,mail=mail,priority=priority,status=status,
            assigned=assigned,assigned_date=assigned_date,uploadFile=uploadFile)
            ticket.save()
            messages.success(request,'Ticket Generated Sucessfully.....')
            return render(request, 'employee/sucess.html', {"dept":dept,"loc":loc,"sub":sub,"ite":ite})


        return render(request, 'employee/employee.html', {"dept":dept,"loc":loc,"sub":sub,"ite":ite})
    else:
        return render(request, 'login/login.html', {})

#employee profile after login
@login_required(login_url='login')
def empprofile(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        return render(request,'employee/profile.html' ,{"ticket": ticket})

    else:
        return render(request, 'login/login.html', {})

#engineer profile after login
@login_required(login_url='login')
def engprofile(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        return render(request,'engineer/profile.html' ,{"ticket": ticket})

    else:
        return render(request, 'login/login.html', {})

#admin profile after login
@login_required(login_url='login')
def adminprofile(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        return render(request,'admin/profile.html' ,{"ticket": ticket})

    else:
        return render(request, 'login/login.html', {})

#superadmin profile after login
@login_required(login_url='login')
def sadminprofile(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        return render(request,'superadmin/profile.html' ,{"ticket": ticket})

    else:
        return render(request, 'login/login.html', {})

#send mail alert to engineer celery
@shared_task(bind=True)
def mail_alert(self):
    prev_day=datetime.now().date() + timedelta(days=1)
    ticket=Tickets.objects.filter(~Q(status='closed'),~Q(status='Completed'), due_date=prev_day)

    for tic in ticket:
        users= get_user_model().objects.filter(username=tic.assigned)
        Id=tic.Id
        queries=tic.queries
        location=tic.location
        for user in users:
            to_email=user.email
            name=user.username
            due_date=prev_day
            mydict = {'Id':Id, 'username': name, 'queries':queries,'location':location, 'due_date':due_date}
            html_template = 'AlertMail.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Ticket is Going to Expire...'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to_email]
            message = EmailMessage(subject, html_message,email_from, recipient_list)
            message.content_subtype = 'html'
            message.send() 

#send Expiry mail to engineer celery
@shared_task(bind=True)
def expiry_mail(self):
    prev_day=datetime.now().date()
    ticket=Tickets.objects.filter(~Q(status='closed'),~Q(status='Completed'), due_date=prev_day)

    for tic in ticket:
        users= get_user_model().objects.filter(username=tic.assigned)
        Id=tic.Id
        queries=tic.queries
        location=tic.location
        assigned_date=tic.assigned_date
        usernames=tic.username
        mobileNo=tic.mobileNo
        emp_mail=tic.mail
        category=tic.category
        subfactory=tic.subfactory
        Description=tic.Description
        priority=tic.priority
        tic.expired=True
        tic.save()
        
        for user in users:
            to_email=user.email
            name=user.username
            due_date=prev_day
            mydict = {'Id':Id,'emp_mail': emp_mail, 'name': name, 'priority':priority, 'Description':Description, 'subfactory':subfactory, 'category': category, 'mobileNo': mobileNo, 'assigned_date': assigned_date, 'username': usernames, 'queries':queries,'location':location, 'due_date':due_date}
            html_template = 'Expired.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Ticket is Expired'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [to_email]
            message = EmailMessage(subject, html_message,email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()  
            

#send Expiry mail to admin celery
@shared_task(bind=True)
def expiry_admin(self):
    prev_day=datetime.now().date()
    ticket=Tickets.objects.filter(~Q(status='closed'),~Q(status='Completed'), expired=True, due_date=prev_day)

    for tic in ticket:
        Id=tic.Id
        queries=tic.queries
        assigned_date=tic.assigned_date
        username=tic.username
        assigned=tic.assigned
        status=tic.status
        to_email="svshelpdesk2001@gmail.com"
        mydict = {'Id':Id,'assigned':assigned, 'username': username, 'status':status, 'assigned_date': assigned_date, 'queries':queries}
        html_template = 'adminexpired.html'
        html_message = render_to_string(html_template, context=mydict)
        subject = 'List of Expired Tickets Today'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        message = EmailMessage(subject, html_message,email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()   
