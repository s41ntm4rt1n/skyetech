from django.shortcuts import render
from .models import *
from django.core.mail import send_mail
from .forms import *
from django.shortcuts import get_object_or_404

def home(request):
    team=Member.objects.all()
    services=Services.objects.all()
    context={
        'team':team,
        'services':services,
    }
    return render(request, 'index.html', context)

def portfolio(request):
    projects=Project.objects.all()
    
    context={
        'projects':projects,
        
    }
    return render(request, 'portfolio.html', context)

def project(request, slug):
    projects=Project.objects.all()
    project=get_object_or_404(Project, slug=slug)
    context={
       'project':project,
       'projects':projects,
    }
    return render(request, 'project-details.html', context)

def documentation(request, slug):
    project=get_object_or_404(Project, slug=slug)
    parts=Part.objects.filter(project=project).order_by('title')
    context={
       'project':project,
       'parts':parts,
    }
    return render(request, 'documentation.html', context)

def about(request):
    team=Member.objects.all()
    about=About.objects.all()
    context={
        'team':team,
        'about':about,
    }
    return render(request, 'about.html', context)


def pricing(request):
    
    context={
       
    }
    return render(request, 'pricing.html', context)

def team(request):
    team=Member.objects.all()
    context={
       'team':team,
    }
    return render(request, 'team.html', context)

def team_details(request, slug):
    member=get_object_or_404(Member, slug=slug)
    context={
       'member':member,
    }
    return render(request, 'team-details.html', context)

def services(request):
    services=Services.objects.all()
    context={
      'services':services,
    }
    return render(request, 'services.html', context)

def faq(request):
    
    context={
       
    }
    return render(request, 'faq.html', context)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']


            body = f"Hello! My name is {name}\nEmail: {email}\nPhone Number: {phone}\nMessage: {message}"
            subject='Email from UIUTOPIA'
            send_mail(
                subject,
                body,
                'brian.robotsaint@gmail.com',
                ['brianmartinmurimi@gmail.com',],
                fail_silently=False,
                )
            form = ContactForm()
            context = {
                'form' : form,
                'show_popup': True,
                'message': 'Your Email Has Been Sent Successfully!'
             }

            return render(request, 'contact.html', context)
    else:
        form = ContactForm()
        context = {
            'form' : form,
        }
        return render(request, 'contact.html', context)
def error_404(request):
    message_title='404'
    message='The page you are looking for does not exist!'
    
    context={
      'message':message,
      'message_title':message_title,  
    }
    return render(request, 'error.html', context, status=404)

def error_500(request):
    message_title='500'
    message='Sorry, something went wrong on our end!'
    
    context={
      'message':message,
      'message_title':message_title,  
    }
    return render(request, 'error.html', context, status=500)