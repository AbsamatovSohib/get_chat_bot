from django.shortcuts import render
from quiz.task import job
from django.http import HttpResponse


def cele(request):
    return HttpResponse("salom dunyo")

