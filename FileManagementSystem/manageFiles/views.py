from distutils import filelist
from django.shortcuts import redirect, render

from manageFiles.models import JGDepartment, JGDivision, JGSection,File
from .forms import FileForm
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.views.generic import View
from manageFiles import models
from .processPDF import html_to_pdf
from django.template.loader import render_to_string

#Delete
from django.http import HttpResponseRedirect
from django.urls import reverse



def GeneratePdf(request, id):
    data = models.File.objects.get(pk=id)
    open('templates/temp.html', "w" , encoding="UTF-8").write(render_to_string('result.html', {'data': data}))

    # Converting the HTML template into a PDF file
    pdf = html_to_pdf('temp.html')
    
    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')

def FileList_delete(request, id):
    id = File.objects.get(pk=id)
    id.delete()
    return HttpResponseRedirect(reverse('create_file'))
   
   
        
def create_file(request):

    form = FileForm()

    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/File/List')
    context = {'form':form}
    return render(request, 'X/form_add_new_file.html', context)
   

def new_func(request):
    return render(request, 'index.html')


def load_departments(request):
    division_id = request.GET.get('file_division')
    departments = JGDepartment.objects.filter(JGDivision_id=division_id).order_by('NothiCode')
    return render(request, 'X/departments_dropdown_list_options.html', {'departments': departments})

def load_sections(request):
    department_id = request.GET.get('file_department')
    sections = JGSection.objects.filter(JGDepartment=department_id).order_by('NothiCode')
    return render(request, 'X/sections_dropdown_list_options.html', {'sections': sections})


def File_list(request):
    data = File.objects.all()
    lst_data = {'Dt':data}
    return render(request,'file_list.html',lst_data)
