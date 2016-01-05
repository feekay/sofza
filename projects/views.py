from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from projects.forms import projectForm, milestoneForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import FormView
from datetime import date
from .forms import MyForm
from projects.models import Attachment, Project, Milestone
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
def projects(request):

    projects = Project.objects.all().exclude(completed= True)
    context_dic= {'projects': projects}
    
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

def milestone_page(request, project_id, name):
    context_dic={}
    try:
        milestone = Milestone.objects.get(project= project_id, title=name)
    except:
        return HttpResponseRedirect('/projects/'+project_id)
    context_dic['milestone'] = milestone

    attachments = Attachment.objects.all().filter(milestone= milestone)
    context_dic['attachments'] = attachments
    
    return render(request, 'projects/milestone_view.html', context_dic)

def project_page(request, project_id):

    context_dic = {id: 'project_id'}
    try:
        project = Project.objects.get(id= project_id)
    except:
        return HttpResponseRedirect('/site/')
    context_dic['project'] = project;
#        print project.id

    if request.GET.get('click', False) and not project.completed:
        project.completed= True
        project.save()
        try:
            #context_dic['project'] = project;
            return HttpResponse(status=200)
        except:
            print "Couldn't respond"

    milestones = Milestone.objects.filter(project=project_id)
    context_dic['milestones'] = milestones
    print "Milestones fetched"

        
    if request.method == "POST":
        form2 = milestoneForm(request.POST)
        form = MyForm(request.POST, request.FILES)

        form2.data['project'] = project.id
        if form2.is_valid():
            form2.save(commit= False)
            data = form2.cleaned_data
            print data['title']
            print data['project'], "DATA"
            form2.save()

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

    context_dic['form'] = form
    context_dic['form2'] = form2
    return render(request,'projects/project_view.html', context_dic)
