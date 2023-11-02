from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import ListView, UpdateView

from django.core import serializers
from django.core.serializers import json
import pickle

from .models import Item
from .forms import ItemUpdateForm
from .tables import ItemList


class Index(TemplateView):
    template_name = "listapp/index.html"


class SimpleListView(ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = "listapp/simple_list_view.html"

    def get_queryset(self):
        # Session key
        key = 'my_qs'

        qs = Item.objects.filter(author__icontains='Ezzie')
        # qs = Item.objects.all()

        # query = (str(qs.query))
        qs_json = serializers.serialize('json', qs)
        self.request.session[key] = qs_json
        print(qs_json)

        return qs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SimpleListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['some_data'] = 'This is just some data'
        qs = self.get_queryset()
        context['qs'] = qs
        return context


class ItemUpdateView(UpdateView):
    template_name = 'listapp/item_update_view.html'
    model = Item
    form_class = ItemUpdateForm
    context_object_name = 'item'

    # Form
    def get_success_url(self):
        return reverse('listapp:_detail', kwargs={'pk': self.object.pk})

    # Form
    def post(self, request, *args, **kwargs):

        object_list = self.get_object_list()

        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()

        if request.method == 'POST':
            if form.is_valid():
                if self.request.POST:
                    if 'save_add' in request.POST:
                        return self.form_valid(form)
                    elif 'save_continue' in request.POST:
                        self.form_valid(form)
                        pk = (object_list.filter(id__gt=self.object.id)
                              .order_by('id')
                              .only('id')
                              .first())
                        return redirect('listapp:_detail', pk=pk.id)
                    elif 'reset' in request.POST:
                        return HttpResponseRedirect(reverse('listapp:_detail', kwargs={'pk': self.object.pk}))
            else:
                return self.form_invalid(form)

    # Form
    def form_valid(self, form):
        return super().form_valid(form)

    # Add info to the form
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return kwargs

    # Navigation
    def get_next_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = object_list.filter(id__gt=current_object_id).order_by('id').only('id').first()
        if qs:
            return qs.id
        else:
            return None

    # Navigation
    def get_previous_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = object_list.filter(id__lt=current_object_id).order_by('-id').only('id').first()
        if qs:
            return qs.id
        else:
            return None

    def get_object_list(self, **kwargs):

        # Session key
        key = 'my_qs'

        qs_json = self.request.session[key]
        print(qs_json)
        for qs in serializers.deserialize('json', qs_json):
            print(qs)

        # qs_query = self.request.session[key]
        
        # item = qs
        reloaded_qs = Item.objects.all()

        query_str = self.request.session[key]
        # reloaded_query = Item.objects.raw('SELECT "listapp_item"."id", "listapp_item"."author", "listapp_item"."title", "listapp_item"."publish" FROM "listapp_item" WHERE "listapp_item"."author" LIKE %Ezzie% ESCAPE')

        # query_bytes = bytes(query_str, 'utf-8')
        # print('********')
        # print(reloaded_qs)
        # print(type(reloaded_qs))
        # print('********')
        # print(reloaded_qs.query)
        # print(type(reloaded_qs.query))
        # print('********')
        # print(query_str)
        # print(type(query_str))
        # print('********')
        # print(query_bytes)
        # print(type(query_bytes))
        # print('********')
        # print(reloaded_query)
        # print(type(reloaded_query))
        # print('********')

        object_list = reloaded_qs.order_by('id')
        return object_list

    # Create context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_object_id = self.object.id
        next_object_id = self.get_next_id(current_object_id)
        previous_object_id = self.get_previous_id(current_object_id)
        object_list = self.get_object_list()

        context['current_object_id'] = current_object_id
        context['next_object_id'] = next_object_id
        context['previous_object_id'] = previous_object_id
        context['object_list'] = object_list

        try:  # If we have pk, create object with that pk
            pk = self.kwargs['pk']
            instances = Item.objects.filter(pk=pk)
            if instances:
                kwargs['object'] = instances[0]
        except Exception as e:
            pass  # No pk, so no detail
        return context
