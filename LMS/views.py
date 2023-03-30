from django.shortcuts import render, redirect
from app.models import Categories, Course

def BASE(request):
    return render(request, 'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'main/home.html', context)

def SINGLE_COURSE(request):
    return render(request, 'main/single_course.html')

def CONTACT_US(request):
    return render(request, 'main/contact_us.html')

def ABOUT_US(request):
    return render(request, 'main/about_us.html')

