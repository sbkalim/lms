from django.contrib import messages
from django.shortcuts import render, redirect
from app.models import Categories, Course, Level, Video, UserCourse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum

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

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['pricefree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
        course = Course.objects.all()
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})
    return JsonResponse({'data': t})

def CORPORATE(request):
    return render(request, 'main/corporate.html')

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
        'category': category,
        'level': level,
        'course': course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count': PaidCourse_count,
    }
    return render(request, 'main/single_course.html', context)

def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    context= {
        'category': category
    }
    return render(request, 'main/contact_us.html', context)

def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request, 'main/about_us.html', context)

def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)

    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query )
    context = {
        'course': course,
        'category': category,
    }
    return render(request, 'search/search.html', context)

def COURSE_DETAILS(request, slug):
    category = Categories.get_all_category(Categories)
    # time_duration = Video.objects.filter(course__slug = slug).aggregate(sum= sum('time_duration'))
    course_id = Course.objects.get(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user.id, course= course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None
    course = Course.objects.filter(slug=slug)

    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context= {
        'course': course,
        'category': category,
        # 'time_duration': time_duration,
        'check_enroll': check_enroll,
    }
    return render(request, 'course/course_details.html', context)

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request, 'error/404.html', context)

def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)

    if course.price == 0:
        usercourse = UserCourse(
            user =request.user,
            course = course
        )
        usercourse.save()
        messages.success(request, 'Enrolled Successfully')
        return redirect('my_course')

    return render(request, 'checkout/checkout.html')

def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user.id)

    context={
        'course': course,
    }
    return render(request, 'course/my_course.html', context)

def WATCH_COURSE(request, slug):
    lecture = request.GET.get('lecture')
    course_id = Course.objects.get(slug = slug)
    course = Course.objects.filter(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
        video = Video.objects.get(id = lecture)
        if course.exists():
            course = course.first()
        else:
            return  redirect('404')
    except UserCourse.DoesNotExist:
        return redirect('404')

    context = {
        'course': course,
        'video': video,
        'lecture': lecture,
    }

    return render(request, 'course/watch_course.html', context)

