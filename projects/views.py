from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from projects.forms import projectForm, milestoneForm, MyForm, UserForm, StaffForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout, login, authenticate
from django.views.generic.edit import FormView
from datetime import datetime,date
from django.db.models import Q
from projects.models import Attachment, Project, Milestone, Staff, Allocation, Message
import os
import json
import mimetypes
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core import serializers
from itertools import chain


def send_message(request, project_id):
    if request.GET.get('message'):
        message = request.GET.get('message')
        text = message
        link_id = project_id
        frm = request.user
        try:       
            project = Project.objects.get(id=link_id)
            project.message_set.create(
            time = datetime.now(),
            text = text,
            frm = frm,
            )
        except Exception as inst:
            print(inst)
            return HttpResponse(status=404)
        print("Create")
        return HttpResponse(status=200)

def get_messages(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Exception as isnt:
        print(inst)
        return HttpResponse(status=404)

    username = request.user
    user = User.objects.get(username = username)
    if user.is_superuser:
        messages = project.message_set.all().order_by('time')
        #data = serializers.serialize('json', messages)
        #return HttpResponse(data, content_type='application/json')        
    else:
        messages = project.message_set.all().filter(Q(to = user)|Q(to=None)|Q(frm=user)).order_by('time')

    try:
        return render(request,'projects/messages.html',{'messages': messages})
    except:
        return HttpResponse("Error in template")


def person_list(request, project_id):
    
    worker_list = []
    try:
        milestones = Project.objects.get(id=project_id).milestone_set.all()
    
    except Exception as inst:
        print(inst)
        return HttpResponse("Not found", status=404)

    for milestone in milestones:
        worker_list.append( allocations(request, milestone.url_id) )

    result =[]
    for worker in worker_list:
        result = list(chain(result, worker))
    
    sorted_result = sorted(
    result,
    key=lambda instance: not instance.active)
    print("Here")
    try:
        data = serializers.serialize('json',sorted_result)
    except Exception as inst:
        print(inst)
    return HttpResponse(data, content_type='application/json')

def get_person(request, person_id):
    try:
        user = User.objects.get(username= person_id)
        person = Staff.objects.get(user=user)
    except:
        
        print("Failed")
        HttpResponse("No such person found", status= 404)

    if request.GET.get("toggle", False):
        #Set active
        user.is_active = not user.is_active
        print("Status")
        user.save()
        
        return HttpResponse(status=200)

    whole = person.allocation_set.all()
    total = len(whole)
    #Add completed
#    current = whole.filter(active = True, completed = False)
    filtered = whole.filter(active = True)
#    woriking = len(current)
    completed = len(filtered)
    failed = total - (completed)

    pay_dollar=0
    pay_euro=0
    pay_pound=0
    for job in filtered:
        if job.pay_type == '$':
            pay_dollar += job.pay
        elif job.pay_type == u'\u00A3':
            pay_pound += job.pay
        elif job.pay_type == u'\u20AC':
            pay_euro += job.pay
    
    failure = whole.filter(active = False)
    lost_dollar=0
    lost_euro=0
    lost_pound=0

    for job in failure:
        if job.pay_type == '$':
            lost_dollar += job.pay
        elif job.pay_type == u'\u00A3':
            lost_pound += job.pay
        elif job.pay_type == u'\u20AC':
            lost_euro += job.pay
    
    person_details = {'email': person.user.email}
    person_details['full_name'] = person.full_name
    person_details['active']= person.user.is_active
    #person_details = {}
    person_details['picture'] = str(person.picture)
    person_details['contact'] = person.phone
    person_details['type']= person.type
    person_details['total']=total
#    person_details['working']=working
    person_details['completed']=completed
    person_details['failed']= failed
    person_details['pay_gain']= [pay_dollar, pay_euro, pay_pound]
    person_details['pay_lost']= [lost_dollar, lost_euro, lost_pound]
    print("here")
    print(person_details)
    try:
    #For normal Dictionaries, Use serializer for QuerySet
        data = json.dumps(person_details)
    except Exception as inst:
        print( inst)
    print("Sending data")
    return HttpResponse(data, content_type='application/json')

    #person.allocation_set.all().filter(active = True)
    #return HttpResponse(status=200)

def get_staff_list(max_results =0, starts_with=""):
    user_list = []
    staff_list = []
    print("Searching for staff", starts_with)
    if starts_with:
        user_list = User.objects.filter(first_name__istartswith=starts_with)
        for user in user_list:
            staff_list.append(Staff.objects.get(user = user))
        print(staff_list)
#    if max_results > 0:
#        if staff_list.count() > max_results:
#            staff_list = staff_list[:max_results]
    print("Returning")
    return staff_list

def suggest_staff(request):

    staff_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        #print("Request Recieved", starts_with)

    staff_list = get_staff_list(4,starts_with)
    #print("Response Ready")
    data = serializers.serialize("json",staff_list)
    #print( data)
    return HttpResponse(data, content_type='application/json')

def allocations(request, milestone_id):
    try:
        milestone = Milestone.objects.get(url_id = milestone_id)
    except:
        return HttpResponse("No such milestone", status = 404)

    allocations = milestone.allocation_set.all().order_by("-active")
    return allocations

def download_file(request, path, document_root):
    the_file = os.path.join(document_root,path)
    
    #print the_file.encode('ascii', errors='backslashreplace')
    filename = os.path.basename(the_file.encode('ascii', errors='backslashreplace'))
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % the_file
    return response

@user_passes_test(lambda u: u.is_superuser)
def projects(request, year=0,month=None):
    MONTHS = {
    'jan' : 0,
    'feb':1,
    'mar':2,
    'apr':3,
    'may':4,
    'jun':5,
    'jul':6,
    'aug':7,
    'sep':8,
    'oct':9,
    'nov':10,
    'dec':11,
    }
    
    MONTH_NAMES = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
    ]
    if not year:
        year = datetime.now().year
    else:
        year = int(year)
    if month is None or month not in MONTHS:
        current_month = datetime.now().month
    else:
        current_month = MONTHS[month]+1

    print month

    projects = Project.objects.filter(start_date__month = current_month, start_date__year = year).order_by('completed','start_date')
    
    context_dic= {}
    current_month -=1
    prev_month = (current_month-1)%12
    next_month = (current_month+1)%12

    context_dic["current_month"] = MONTH_NAMES[current_month]
    if prev_month > current_month:
        context_dic["prev_month"] = str(year-1) + '/' + MONTH_NAMES[prev_month]
    else:
        context_dic["prev_month"] = str(year) + '/' + MONTH_NAMES[prev_month]
        
    if next_month < current_month:
        context_dic["next_month"] = str(year+1) + '/' + MONTH_NAMES[next_month]
    else:
        context_dic["next_month"] = str(year) + '/' + MONTH_NAMES[next_month]

    context_dic['projects'] = projects
    
    if request.method == "POST":
        form = projectForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            pass
    else:
        form = projectForm()

    context_dic['form'] = form;
    return render(request, 'projects/project_list.html', context_dic)

@ensure_csrf_cookie
def milestone_page(request, project_id, mile_id):
    context_dic={}
    try:
        project = Project.objects.get(pk=project_id)
        milestone = Milestone.objects.get(project= project_id, url_id=mile_id)
    except:
        return HttpResponseRedirect('/projects/'+project_id)

    if request.GET.get("complete", False):
        milestone.completed = True;
        milestone.save()

    if request.GET.get("important", False):
        current = milestone.important
        milestone.important = not current
        milestone.save()  
    #In case on input request
    if request.method == "POST":
        if 'username' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
    
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    pass
            else:
                HttpResponse("Invalid Username or Password")

        elif 'name' in request.POST:
            name = request.POST['name']
            allocation = request.POST['allocation']
            user_id = request.POST['user_id']
            try:
                print("Trying Allocation")
                pay = int(allocation)
            except:
                #produce an error saying incorect field or something
                pass
            else:
                try:
                    print("Trying User")
                    person = Staff.objects.get(user= user_id)
                    #user = User.objects.get(username = name)
                except:
                    #produce an error saying incorect username or something
                    pass
                else:
                    print("Found User")
                    pay_type = project.pay_type

                    try:
                        prev = milestone.allocation_set.get(active = True)
                    except:
                        pass
                    else:
                        prev.active = False
                        prev.save()
                    
                    alloc = milestone.allocation_set.create(person=person,
                    pay= pay,
                    pay_type= pay_type,
                    active=True,
                    )
                    return HttpResponseRedirect('/projects/'+project_id+"/"+mile_id)

#    if request.GET.get('success', False) and not milestone.success:
#        print ("In Milestone")
#        project.save()
#        milestone.completed = True
#        milestone.save()
#        #print ("Saved")
#        try:
#            context_dic['project'] = project;
#            return HttpResponse(status=200)
#        except:
#            print "Couldn't respond"
#
#    if request.GET.get('fail', False) and not milestone.completed:
#        #print ("In Milestone")
#        milestone.completed = True
#        milestone.success = False
#        milestone.save()
#        #print ("Saved")
#        try:
#            #context_dic['project'] = project;
#            return HttpResponse(status=200)
#        except:
#            print "Couldn't respond"
    context_dic['project_id'] = project_id
    context_dic['milestone'] = milestone
    attachments = Attachment.objects.all().filter(milestone= milestone)
    #context_dic['attachments'] = attachments
    #context_dic['allocations'] = allocations(request, milestone.url_id)
    context_dic['days_left'] = (milestone.deadline -date.today()).days
    print(context_dic['days_left'])
    return render(request, 'projects/milestone_view.html', context_dic)


def project_page(request, project_id, month=0):

    context_dic = {id: 'project_id'}
    try:
        project = Project.objects.get(id= project_id)
    except:
        return HttpResponseRedirect('/site/')
    context_dic['project'] = project;
#        print project.id

    if request.GET.get("success", False):
        project.success = True
        project.completed = True
        project.save()
        
    if request.GET.get("fail", False):
        project.success = False
        project.completed = True
        project.save()


    project.update_cost()
    
    #Delete this after checking if its still in use
    if request.GET.get('click', False) and not project.completed:
        project.completed= True
        print(project.completed)
        project.save()
        try:
            #context_dic['project'] = project;
            return HttpResponse(status=200)
        except:
            print "Couldn't respond"

    milestones = Milestone.objects.filter(project=project_id).order_by("completed", "start_date")
    context_dic['milestones'] = milestones
    print "Milestones fetched"
    return milestone_form(request, project_id, context_dic)


def milestone_form(request, project_id, context_dic={}):

    project = context_dic["project"]
    if request.method == "POST":
        form2 = milestoneForm(request.POST)
        form = MyForm(request.POST, request.FILES)

        form2.data['project'] = project.id
        if form2.is_valid():
            form2.save(commit= False)
            data = form2.cleaned_data
            #print data['title']
            #print data['project'], "DATA"
            form2.save()
            project.update_cost()

            current = Milestone.objects.get(title=data['title'], project = project_id)
            print current
            if form.is_valid():
                for f in request.FILES.getlist('file'):
                    Attachment.objects.create(milestone=current, file=f)
                return HttpResponseRedirect('/projects/'+project_id)
        else:
            print form2.errors

    else:
        form2 = milestoneForm()
        form = MyForm()
    print(project.last_updated)
    context_dic['updated'] = project.last_updated.isoformat()
    context_dic['form'] = form
    context_dic['form2'] = form2
    return render(request,'projects/project_view.html', context_dic)
@user_passes_test(lambda u: u.is_superuser)      
def staff(request):
   
    staff = Staff.objects.all()
    if request.method == "POST":
        print request.FILES
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)
        
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            staff = staff_form.save(commit=False)
            staff.user = user

            if 'picture' in request.FILES:
                staff.picture = request.FILES['picture']
            staff.save()
            print "Saved"
            return HttpResponseRedirect('/projects/staff/')

        else:
            print user_form.errors, staff_form.errors
    else:
        user_form = UserForm()
        staff_form = StaffForm()

    return render(request, "projects/staff.html", {'staff': staff, 'user_form': user_form, 'staff_form': staff_form})

@user_passes_test(lambda u: u.is_superuser)  
def analytics(request):
    return HttpResponse("WOW")


def logout_view(request):
    print("Recieved")
    logout(request)
    return HttpResponseRedirect('/site/')

@user_passes_test(lambda u: u.is_superuser)  
def invoice_list(request):
    return HttpResponse("Page Exists!")

@user_passes_test(lambda u: u.is_superuser)  
def invoice(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == "POST":
        data= []
        total = 0
        #print(request.POST)
        address = request.POST['address']
        try:
            discount = int(request.POST["discount"])
        except ValueError:
            discount = 0

        for key in request.POST:
            try:
                x = project.milestone_set.get(title = key)
            except:
                pass
            else:
                x.paid = True
                x.save()
                try:
                    qty = int(request.POST[key+"_qty"])
                except ValueError:
                    qty = 1
                total += (x.cost * qty)
                data.append({'title' : x.title, 'cost' : x.cost, 'type':project.pay_type, 'qty': qty})
            
        name = generate(project.client, project.client_mail, data, address,total, discount)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(name+".pdf"), chunk_size),
                           content_type=mimetypes.guess_type(name+".pdf"))
        response['Content-Length'] = os.path.getsize(name+".pdf")
        response['Content-Disposition'] = "attachment; filename=%s" % (name+".pdf")
        return response
    else:
        unpaid = project.milestone_set.all().filter(paid=False)
        return render(request,'projects/invoice.html', {'unpaid':unpaid, 'project_id':project.id})


def generate(name, email, data, addr, total, discount=0):
    print ("Generating PDF")
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import letter
    c = canvas.Canvas(name+".pdf", pagesize = letter)
    c.drawString(1*inch, 9*inch, "Sofza")
    c.drawString(1*inch, 8.7*inch, "Raised By")
    c.drawString(1*inch, 8.4*inch, "Haris Mehmood")
    c.drawString(1*inch, 8.1*inch, "Invoice Payment Notice")

    c.drawString(4*inch, 9*inch, "Towards")
    c.drawString(4*inch, 8.7*inch, name)
    c.drawString(4*inch, 8.4*inch, email)
    c.drawString(4*inch, 8.1*inch, addr)
    c.line(0, 7.7*inch, 8*inch, 7.7*inch)
    
    point = 7.5
    
    c.drawString(1*inch, point*inch, 'Title')
    c.drawString(5*inch, point*inch, 'Cost')
    c.drawString(6*inch, point*inch, 'Qty')
    c.drawString(7*inch, point*inch, 'Amount')
    point -= 0.1
    c.line(0, point*inch, 8*inch, point*inch)
    for x in data:
        point -= 0.2
        c.drawString(1*inch, point*inch, x['title'])
        c.drawString(5*inch, point*inch, x['type']+str(x['cost']))
        c.drawString(6*inch, point*inch, str(x['qty']))
        c.drawString(7*inch, point*inch, x['type']+str(x['qty']*x['cost']))
        point -= 0.1
        c.line(0, point*inch, 8*inch, point*inch)
    point -= 0.3

    c.drawString(1*inch, point*inch, "Total: "+x['type']+str(total))
    point -= 0.3
    
    if discount:
        c.drawString(1*inch, point*inch, "Discount: "+x['type']+ str(discount))
        point -= 0.3
        total-=discount
    c.drawString(1*inch, point*inch, "Due amount: "+x['type']+str(total))
    point -= 0.3
    c.save()
    return name
#x_max = 8.3", y_max = 11.7"
