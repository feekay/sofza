from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from projects.forms import projectForm, milestoneForm, MyForm, UserForm, StaffForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout, login, authenticate
from django.views.generic.edit import FormView
from datetime import datetime
from projects.models import Attachment, Project, Milestone, Staff, Allocation, Message
import os
import mimetypes
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper


def staff_list(max_results =0, starts_with=""):
    

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
            try:
                print("Trying Allocation")
                pay = int(allocation)
            except:
                #produce an error saying incorect field or something
                pass
            else:
                try:
                    print("Trying User")
                    user = User.objects.get(username = name)
                except:
                    #produce an error saying incorect username or something
                    pass
                else:
                    print("Found User")
                    pay_type = project.pay_type
                    person = Staff.objects.get(user= user)
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
    context_dic['attachments'] = attachments
    context_dic['allocations'] = allocations(request, milestone.url_id)
    return render(request, 'projects/milestone_view.html', context_dic)


def project_page(request, project_id, month=0):

    context_dic = {id: 'project_id'}
    try:
        project = Project.objects.get(id= project_id)
    except:
        return HttpResponseRedirect('/site/')
    context_dic['project'] = project;
#        print project.id
    project.update_cost()
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

    context_dic['updated'] = project.last_updated.isoformat()
    context_dic['form'] = form
    context_dic['form2'] = form2
    return render(request,'projects/project_view.html', context_dic)
#@user_passes_test(lambda u: u.is_superuser)      
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
    logout(request)
    return HttpResponseRedirect('/site/')

#@user_passes_test(lambda u: u.is_superuser)  
def invoice(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == "POST":
        data= []
        total = 0
        print(request.POST)
        address = request.POST['address']
        discount = int(request.POST["discount"])
        
        for key in request.POST:
            try:
                x = project.milestone_set.get(title = key)
            except:
                pass
            else:
                x.paid = True
                x.save()
                total += x.cost
                data.append({'title' : x.title, 'cost' : x.cost})
            
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
    c.drawString(1*inch, 8.7*inch, "Haris Mehmood")
    c.drawString(1*inch, 8.4*inch, "Invoice Payment Notice")
    c.line(0, 8.1*inch, 8*inch, 8.1*inch)
    c.drawString(1*inch, 7.7*inch, "Invoiced to:")
    c.drawString(1*inch, 7.4*inch, name)
    c.drawString(1*inch, 7.1*inch, email)
    c.drawString(1*inch, 6.8*inch, addr)
    c.line(0, 6.5*inch, 8*inch, 6.5*inch)
    
    point = 6.2
    for x in data:
        c.drawString(1*inch, point*inch, x['title'] + " " + str(x['cost']))
        point -= 0.3
    if discount:
        c.drawString(1*inch, point*inch, "Discount: "+ str(discount))
        point -= 0.3
        total-=discount
    c.drawString(1*inch, point*inch, "Total: "+str(total))
    point -= 0.3
    c.save()
    return name
#x_max = 8.3", y_max = 11.7"
