from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect, QueryDict
from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView, ListView, View, UpdateView
from django.core.paginator import Paginator

from django_filters.views import FilterView

import pickle
from base64 import b64encode, b64decode
from urlobject import URLObject

from .models import Cat, Image, Item
from .filters import ItemFilter
from .forms import ItemFilterForm, ImageUploadForm, ItemUpdateForm
from .tables import ItemList
from .utils import getlines, filter_group, combine, FilterSet, PaginationLinks, find_object

from django import forms
from django.forms import modelform_factory

FILTER_TEMPLATES = {
    'q': lambda value: Q(title__icontains=value) | Q(author__icontains=value),
    **filter_group('title'),
}

FILTER_LABELS = {
    'Author': 'author',
    'Title': 'title',
    'Publish': 'publish',
}

PAGE_PARAM_NAME = 'page'

PAGE_SIZE = 10


def append_filter(request: HttpRequest) -> HttpResponseRedirect:
    url = URLObject(request.build_absolute_uri())
    filter_param = request.POST['filter_name'] + request.POST['filter_operation']
    filter_value = request.POST['filter_value']
    new_url = url.add_query_param(filter_param, filter_value)
    return HttpResponseRedirect(new_url)


class Index(TemplateView):
    template_name = 'listapp/index.html'


class CrudTable(ListView):
    model = Cat
    template_name = 'listapp/crudtable.html'


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        exclude = []


def get_cat_list(request):
    context = {}
    context['cats'] = Cat.objects.all()
    return render(request, 'listapp/partials/cat_list.html', context)


def add_cat(request):
    context = {'form': CatForm()}
    return render(request, 'listapp/partials/add_cat.html', context)


def add_cat_submit(request):
    context = {}
    form = CatForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        context['cat'] = form.save()
    else:
        return render(request, 'listapp/partials/add_cat.html', context)
    return render(request, 'listapp/partials/cat_row.html', context)


def add_cat_cancel(request):
    return HttpResponse()


def delete_cat(request, cat_pk):
    cat = Cat.objects.get(pk=cat_pk)
    cat.delete()
    return HttpResponse()


def edit_cat(request, cat_pk):
    cat = Cat.objects.get(pk=cat_pk)
    context = {}
    context['cat'] = cat
    context['form'] = CatForm(
        initial={
            'name': cat.name,
            'gender': cat.gender,
            'age': cat.age,
            'breed': cat.breed,
            'color': cat.color,
        }
    )
    return render(request, 'listapp/partials/edit_cat.html', context)


def edit_cat_submit(request, cat_pk):
    context = {}
    cat = Cat.objects.get(pk=cat_pk)
    context['cat'] = cat
    if request.method == 'POST':
        form = CatForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'listapp/partials/edit_cat.html', context)
    return render(request, 'listapp/partials/cat_row.html', context)


class FancyList(ListView):
    model = Item
    # queryset = Item.objects.all()
    template_name = 'listapp/fancy_list.html'

    def post(self, _request):
        if 'filter_name' in self.request.POST:
            return append_filter(self.request)

        # else:
        # action = self.request.POST['action']
        # item_ids = self.request.POST.getlist('item_id')

    # if action == 'edit':
    #     # bulk editing
    #     qs = [('item_id', item_id) for item_id in item_ids] + [
    #         ('redirect', self.request.POST.get('redirect', reverse('fancylist')))
    #     ]
    #     return HttpResponseRedirect(reverse('bulk_edit_books') + '?' + urlencode(qs))
    # else:
    #     raise BadRequest

    def get(self, _request):
        itemlist = Item.objects.all()

        filters = FilterSet()

        for filter_query in filters.build(FILTER_TEMPLATES, self.request.GET):
            itemlist = itemlist.filter(filter_query)

        itemlist = itemlist.distinct().order_by('id')

        paginator = Paginator(itemlist, PAGE_SIZE)
        page = paginator.get_page(self.request.GET.get(PAGE_PARAM_NAME, 1))

        url = URLObject(self.request.build_absolute_uri())

        return render(
            self.request,
            'listapp/fancy_list.html',
            context={
                'url': url,
                # 'categories': CATEGORIES.keys(),
                'filter_names': FILTER_LABELS,
                'page_obj': page,
                'filters': filters,
                'page_links': PaginationLinks(url, page, PAGE_PARAM_NAME),
                # 'isbn_form': SingleISBNForm(),
            },
        )


class ImageListView(ListView):
    model = Image
    template_name = 'listapp/image_list_view.html'


class ImageUpload(CreateView):
    model = Image
    form_class = ImageUploadForm
    template_name = 'listapp/image_upload.html'

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect('listapp/image_list_view.html')
        return render(request, 'listapp/image_upload.html', {'form': form})


class SimpleListView(ListView):
    model = Item
    queryset = Item.objects.all()
    context_object_name = 'item_list'
    template_name = 'listapp/simple_list_view.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)

        # Session key
        key = 'my_qs'

        key_url = 'key_url'

        # url for returning with applied filters
        self.request.session[key_url] = self.request.GET

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        self.request.session[key] = b64encode(pickle.dumps(self.filterset.qs.query)).decode('ascii')

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(SimpleListView, self).get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context


class ItemUpdateView(UpdateView):
    template_name = 'listapp/item_update_view.html'
    model = Item
    form_class = ItemUpdateForm
    context_object_name = 'item'

    # Form
    def get_success_url(self):
        return reverse('listapp:itemupdateview', kwargs={'pk': self.object.pk})

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
                        pk = object_list.filter(id__gt=self.object.id).order_by('id').only('id').first()
                        return redirect('listapp:itemupdateview', pk=pk.id)
                    elif 'reset' in request.POST:
                        return HttpResponseRedirect(reverse('listapp:itemupdateview', kwargs={'pk': self.object.pk}))
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

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        query = pickle.loads(b64decode(self.request.session[key]))
        qs = Item.objects.all()
        qs.query = query

        object_list = qs.order_by('id')
        return object_list

    def query_filter_url(self):
        object_list = self.get_object_list()

        # query_filter_url = self.kwargs['parameter']
        # query_filter_url = QueryDict(mutable=True)  # returns empty dict
        # query_filter_url = dict(self.request.GET)  # returns empty dict, expected since it would be getting url

        query_filter_url = urlencode({'publish': 'True'})  # Desired, however not hardcoded

        return query_filter_url

    # Create context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get query URL to return to list view
        key_url = 'key_url'
        query_params = self.request.session[key_url]

        current_object_id = self.object.id
        next_object_id = self.get_next_id(current_object_id)
        previous_object_id = self.get_previous_id(current_object_id)
        object_list = self.get_object_list()

        context['current_object_id'] = current_object_id
        context['next_object_id'] = next_object_id
        context['previous_object_id'] = previous_object_id
        context['object_list'] = object_list
        context['query_params'] = urlencode(query_params)

        try:  # If we have pk, create object with that pk
            pk = self.kwargs['pk']
            instances = Item.objects.filter(pk=pk)
            if instances:
                kwargs['object'] = instances[0]
        except Exception as e:
            pass  # No pk, so no detail
        return context


def search_item_author(request):
    search_text = request.GET.get('search')
    # look up all items that contain the text
    results = Item.objects.filter(author__icontains=search_text)
    context = {'results': results}
    return render(request, 'listapp/partialss/search-results.html', context)


def search_item_title(request):
    search_text = request.GET.get('search')
    # look up all items that contain the text
    results = Item.objects.filter(title__icontains=search_text)
    context = {'results': results}
    return render(request, 'listapp/partialss/search-results.html', context)
