from django.shortcuts import render, HttpResponse, redirect
from account.forms import RegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from case.models import case , Task , Document
from case.forms import Reg_Case, Reg_Task , DocumentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
import os
from django.core.files.storage import default_storage


#python imports
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = spacy.load('en')
import speech_recognition as sr


from bs4 import BeautifulSoup
import requests
import re

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))

def getfreq(temp_data):
    mp_codes={}
    mp_tags={}
    unique_codes=[]
    for i in range(len(temp_data)):
        if temp_data[i][0].lower() in mp_codes.keys():
            mp_codes[temp_data[i][0].lower()]=mp_codes[temp_data[i][0].lower()]+1
        else:
            mp_codes[temp_data[i][0].lower()]=1

        if temp_data[i][0].lower() in mp_tags.keys():
            continue
        else:
            mp_tags[temp_data[i][0].lower()]=temp_data[i][1].lower()

    return mp_codes,mp_tags

"""
ny_bb = url_to_string('https://www.coursera.org/instructor/andrewng')
article = nlp(ny_bb)
len(article.ents)
print(article)
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#from django.conf.settings import MEDIA_ROOT
#from django.urls import reverse
# Create your views here.


@transaction.atomic
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			user.userprofile.designation = profile_form.cleaned_data.get('designation')
			user.userprofile.city = profile_form.cleaned_data.get('city')
			user.userprofile.unq = profile_form.cleaned_data.get('unq')
			user.userprofile.save()
			return redirect('/account/login')
		else:
			messages.error(request,form.errors)
			args = {'form':form, 'profile_form':profile_form}
			return render(request, 'account/reg_form.html', args)
	else:
		form = RegistrationForm()
		profile_form = UserProfileForm()
		args = {'form':form, 'profile_form':profile_form}
		return render(request, 'account/reg_form.html', args)


@login_required
def view_profile(request):
    if request.user.userprofile.designation == 'investigation head':
        new_cases = case.objects.filter(case_info = '',investigation_head = request.user.userprofile)
        ongoing_cases = case.objects.filter(status='Under Investigation',investigation_head=request.user.userprofile).count()
        completed_cases = case.objects.filter(status='Completed',investigation_head=request.user.userprofile).count()
        args = {'user': request.user,'new_cases':new_cases,'ongoing_cases':ongoing_cases,'completed_cases':completed_cases}
    elif request.user.userprofile.designation == 'member':
        form3 = DocumentForm()
        mp_codes={}
        mp_tags={}
        mp_places={}
        probability={}
        main_mp={}
        if request.method == 'POST':
            form3 = DocumentForm()
            print(request.user.userprofile.unq)
            t1 = Task.objects.filter(task_member=request.user.userprofile)
            print(t1)
            k = Document.objects.filter(unq = t1[0].case_number)
            print(t1[0].task_number)
            #1 file
            #print(k[0].file1)
            f = default_storage.open(os.path.join('', str(k[0].file1)), 'r')
            data = f.read()
            f.close()
            #print(data)
            article1 = nlp(data)
            k1 = [(X.text, X.label_) for X in article1.ents]
            print(len(k1))

            #2 file
            f = default_storage.open(os.path.join('', str(k[0].csvfile1)), 'r')
            data = f.read().splitlines()
            f.close()
            for i in range(len(data)):
                t1 = data[i].split(",")
                if t1[0].lower() in mp_places.keys():
                    continue
                else:
                    mp_places[t1[0].lower()]=t1[1].lower()

            print(mp_places)
            #article1 = nlp(data)
            print(len(k1))



            #1 csvfile1
            f = default_storage.open(os.path.join('', str(k[0].audio1)), 'rb')
            #data = f.read()
            #print(f)
            r = sr.Recognizer()
            harvard = sr.AudioFile(f)

            #1 audiofile1
            with harvard as source:
                audio = r.record(source)
            k = r.recognize_google(audio)
            article1 = nlp(k)
            k1.extend([(X.text, X.label_) for X in article1.ents])
            f.close()
            print([(X.text, X.label_) for X in article1.ents])
            print('hello')
            print('hello')
            #k1.extend([(X.text, X.label_) for X in article1.ents])

            print(len(k1))
            print(len(set(k1)))



            mp_codes, mp_tags = getfreq(k1)
            print(mp_codes)
            print(mp_tags)

            total =0
            for i in mp_tags:
                print("i ",mp_codes[i])
                total=total+mp_codes[i]


            for i in mp_codes:
                probability[i] = mp_codes[i]/total

            for i in mp_places:
                places = mp_places[i]
                for j in mp_tags:
                    if(i==j):
                        if places in main_mp.keys():
                            main_mp[places] = main_mp[places]+probability[j]
                        else:
                            main_mp[places] = probability[j]

            print("main ",main_mp)
            print("probabity" , probability)
            print("total ",total)
        form = Reg_Task()
        ongoing_task = Task.objects.filter()
        ongoing_cases = case.objects.filter(status='Under Investigation',members=request.user.userprofile).count()
        completed_cases = case.objects.filter(status='Completed',members=request.user.userprofile).count()
        args = {'mp_main':main_mp , 'mp_codes':mp_codes, 'mp_tags':mp_tags, 'user': request.user, 'ongoing_cases':ongoing_cases,'completed_cases':completed_cases , 'form':form, 'ongoing_task':ongoing_task,'form3':form3}
    else:
        args = {'user':request.user}
        if request.method == 'POST':
            form = Reg_Case(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/account/profile')
            else:
                form = Reg_Case()
            args = {'user':request.user,'form':form}


    return render(request, 'account/profile.html', args)


"""
@login_required
def function1(request):
    form = NewInput1()
    if request.method=="POST":
        form = NewInput1(request.POST)

        if form.is_valid():

			model_instance = form.save(commit=False)
            article1=""
            article2="32"
            article3=""
            article4=""
            article5=""

            try:
                data1 = request.FILES['file1']
                f1 = data1.read().decode('utf-8')#.splitlines()
                article1 = nlp(f1)
                k1 = [(X.text, X.label_) for X in article1.ents]
            except:
                1

            try:
                data2 = request.FILES['file2']
                f2 = data2.read().decode('utf-8')#.splitlines()
                article2 = nlp(f2)
                print(article2)
                k2 = [(X.text, X.label_) for X in article2.ents]
            except:
                1

            try:
                data3 = request.FILES['file3']
                f3 = data3.read().decode('utf-8')#.splitlines()
                article3 = nlp(f3)
                k3 = [(X.text, X.label_) for X in article3.ents]
            except:
                1

            try:
                data4 = request.FILES['csvfile1']
                f4 = data4.read().decode('utf-8')#.splitlines()
                print(f4.split('\n')[3])
            except:
                1

            try:
                ny_bb4 = url_to_string(model_instance.url1)
                article4 = nlp(ny_bb4)
                print(set([(X.text, X.label_) for X in article4.ents]))
            except:
                1

            try:
                ny_bb5 = url_to_string(model_instance.url2)
                articler5 = nlp(ny_bb5)
            except:
                1

            return render(request , 'filetonlp/input1.html', {'form':form , 'article2':article4})

    return render(request , account/profile.html, {'form':form })
"""
