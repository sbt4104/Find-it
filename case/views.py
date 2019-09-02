from django.shortcuts import render, redirect
from case.forms import Reg_Case, New_Case, Update_Status, Reg_Task, Update_Task_Status#,Report_Form
from case.models import case, Task#, Report
# Create your views here.

def add_info(request, pk):
    if request.method == 'POST':
        c = case.objects.get(pk=pk)
        form = New_Case(request.POST,instance=c)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form = New_Case()
        c = case.objects.get(pk=pk)
        args = {'form':form,'case':c}
        return render(request,'case/add_info.html', args)

def cases(request):
    user = request.user
    if user.userprofile.designation == 'investigation head':
        cases = case.objects.filter(investigation_head=request.user.userprofile)
    else:
        cases = case.objects.filter(members=request.user.userprofile)
    args = {'cases': cases}
    return render(request,'case/cases.html',args)

def case_details(request, pk):
    if request.method == 'POST':
        c = case.objects.get(pk=pk)
        form = Update_Status(request.POST,instance=c)
        form2 = Report_Form(request.POST)
        if form.is_valid():
            form.save()
        if form2.is_valid():
            report_form = form2.save(commit=False)
            report_form.report_user = request.user.userprofile
            report_form.report_case = c
            report_form.save()
        reports = Report.objects.filter(report_case=c,report_task = None)
        args = {'case':c, 'form':form,'report_form':form2,'user':request.user,'reports':reports}
        return render(request, 'case/case_details.html', args)
    else:
        c = case.objects.get(pk = pk)
        form = Update_Status(initial={'status': c.status})
        form2 = Report_Form()
        reports = Report.objects.filter(report_case=c,report_task = None)
        args = {'case':c, 'form':form,'report_form':form2,'user':request.user,'reports':reports}
        return render(request, 'case/case_details.html', args)

def reg_task(request):
    if request.method == 'POST':
        form = Reg_Task(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.investigation_head = request.user.userprofile
            form.save()
            return redirect('/account/profile')
    else:
        form = Reg_Task()
        user = request.user
        if user.userprofile.designation == 'investigation head':
            tasks = Task.objects.filter(investigation_head=request.user.userprofile)
        else:
            tasks = Task.objects.filter(task_member=request.user.userprofile)
        args = {'user':user,'form':form,'tasks':tasks}
        return render(request,'case/reg_task.html',args)

def task_details(request,pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        form = Update_Task_Status(request.POST,instance=task)
        form2 = Report_Form(request.POST)
        if form.is_valid():
            form.save()
            reports = Report.objects.filter(report_case=task.task_case,report_task = task)
            args = {'task':task, 'form':form,'report_form':form2,'user':request.user,'reports':reports}
            return render(request, 'case/task_details.html', args)
        if form2.is_valid():
            report_form = form2.save(commit=False)
            report_form.report_user = request.user.userprofile
            report_form.report_case = task.task_case
            report_form.report_task = task
            report_form.save()
        reports = Report.objects.filter(report_case=task.task_case,report_task = task)
        args = {'task':task, 'form':form,'report_form':form2,'user':request.user,'reports':reports}
        return render(request, 'case/task_details.html', args)
    else:
        task = Task.objects.get(pk = pk)
        form = Update_Task_Status(initial={'task_status': task.task_status})
        form2 = Report_Form()
        reports = Report.objects.filter(report_case=task.task_case,report_task = task)
        args = {'task':task, 'form':form,'report_form':form2,'user':request.user,'reports':reports}
        return render(request, 'case/task_details.html', args)
