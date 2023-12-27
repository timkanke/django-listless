from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView, ListView, View, UpdateView


class Index(TemplateView):
    template_name = 'textblockapp/index.html'
