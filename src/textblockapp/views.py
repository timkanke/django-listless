from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView, ListView, View, UpdateView

from .models import Text


class Index(ListView):
    model = Text
    context_object_name = 'text_list'
    template_name = 'textblockapp/index.html'


class DiffView(DetailView):
    model = Text
    template_name = 'textblockapp/diffview.html'
