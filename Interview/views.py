from django.db.models.fields import DateTimeField
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Interview
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
import pytz
from django.core.mail import EmailMessage

utc=pytz.UTC

errors = []
def InterviewPanel(request):
    if request.method == "GET":
        return render(
            request, 
            "interview-panel.html",
            {
                "participants" : User.objects.all() , 
                "interviews" : Interview.objects.all().order_by('-start_time'),
                "errors" : list(set(errors))
            }
        )

    elif request.method == "POST":
        interview_participants = []
        for participant in request.POST.getlist('participants'):
            interview_participants.append(participant)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if is_valid(interview_participants , parse_datetime(start_time), parse_datetime(end_time) , -1):
            interview = Interview.objects.create(start_time=start_time , end_time=end_time)
            for participant in interview_participants:
                p = User.objects.get(username=participant)
                interview.participants.add(p)
            
            email_to = []
            for participant in interview_participants:
                p = User.objects.get(username=participant)
                email_to.append(p.email)

            email = EmailMessage(
                "Interview Scheduled",
                "Your interview is scheduled: " + start_time + " - " + end_time + ".",
                to = email_to
            )
            email.send()

        return render(
            request, 
            "interview-panel.html",
            {
                "participants" : User.objects.all() , 
                "interviews" : Interview.objects.all().order_by('-start_time'),
                "errors": list(set(errors)) 
            }
        )

def UpdateInterview(request , pk):
    
    if request.method == "GET":
        return render(
            request,
            "interview-update.html",
            {
                "interview":Interview.objects.get(pk=pk),
                "participants":User.objects.all(),
                "errors": errors
            }
        )

    elif request.method == "POST":
        interview_participants = []
        for participant in request.POST.getlist('participants'):
            interview_participants.append(participant)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if is_valid(interview_participants , parse_datetime(start_time), parse_datetime(end_time) , pk):
            interview = Interview.objects.get(pk=pk)
            interview.start_time=start_time
            interview.end_time=end_time
            interview.participants.clear()
            for participant in interview_participants:
                p = User.objects.get(username=participant)
                interview.participants.add(p)
            interview.save()

            email_to = []
            for participant in interview_participants:
                p = User.objects.get(username=participant)
                email_to.append(p.email)
                
            email = EmailMessage(
                "Interview Updated",
                "Your interview is updated: " + start_time + " - " + end_time + ".",
                to = email_to
            )
            email.send()

        return render(
            request, 
            "interview-update.html",
            {
                "interview":Interview.objects.get(pk=pk),
                "participants":User.objects.all(),
                "errors": errors
            }
        )
        

def is_valid(participants , start_time , end_time , ignore):

    print(ignore)
    errors.clear()
    flag = True
    if len(participants) < 2:
        errors.append("Less than 2 participants")
        flag = False
    
    interviews = Interview.objects.all()
    for interview in interviews:
        print(interview.pk , ignore)
        if interview.pk == int(ignore):
            continue
        print(interview.pk , ignore)
        print(type(interview.pk) , type(ignore))
        for p in interview.participants.all():
            if p.username in participants and clash(start_time , end_time , interview.start_time , interview.end_time):
                errors.append("Participant " + p.username + " already has interview scheduled")
                flag = False
        
    return flag

def clash(s1 , e1 , s2 , e2):

    s1 = s1.replace(tzinfo=utc)
    e1 = e1.replace(tzinfo=utc)
    s2 = s2.replace(tzinfo=utc)
    e2 = e2.replace(tzinfo=utc)

    if s1 > s2:
        s1 , e1 , s2 , e2 = s2 , e2 , s1 , e1
    
    
    return s2 < e1

# def deleteItem(request,pk):
#     item=Interview.objects.get(pk=pk)
#     item.delete()
#     return redirect('')





    


