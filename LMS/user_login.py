from django.shortcuts import render, redirect


def REGISTER(request):
    return render(request, 'registration/register.html')