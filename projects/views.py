from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
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

    #In case on input request
    if request.method == "POST":
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
#    if request.GET.get('success', False) and not milestone.success:
        #print ("In Milestone")
#        project.revenue += milestone.cost
#        project.save()
#        milestone.completed = True
#        milestone.success = True
#        milestone.save()
#        #print ("Saved")
#        try:
            #context_dic['project'] = project;
#            return HttpResponse(status=200)
#        except:
#            print "Couldn't respond"
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

@user_passes_test(lambda u: u.is_superuser)  
def invoice(request, project_id):
    project = Project.objects.get(id=project_id)
    unpaid = project.milestone_set.all().filter(paid=False)
    print unpaid
    return HttpResponse("WOW")
    
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
