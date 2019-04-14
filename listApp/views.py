from django.shortcuts import render
from .models import List, Element, Viewer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils.decorators import method_decorator
from django import forms


@login_required
def home(request):
    context = {
        "lists": List.objects.all().order_by('-id'),
        "title": "My Lists"
    }
    return render(request, "listApp/index.html", context)

@login_required
def detail(request, pk):
    theList = get_object_or_404(List, pk = pk)
    elements = Element.objects.filter(theList = theList).order_by('-id')
    viewers = Viewer.objects.filter(theList = theList).order_by('-id')

    if request.method == 'POST':
        element_form = elementForm(request.POST or None)
        if element_form.is_valid():
            name = request.POST.get('name')
            links = request.POST.get('links')
            images = request.POST.get('images')
            element = Element.objects.create(theList = theList, author = request.user, name = name, links = links, images = images)
            element.save()
            return HttpResponseRedirect(theList.get_absolute_url())
    else:
        element_form = elementForm()

    context = {
        "list": theList,
        "title": theList.title,
        "elements": elements,
        "viewers": viewers,
        "element_form": element_form
    }
    return render(request, "listApp/details.html", context)

@login_required
def shared(request):
    viewers = Viewer.objects.all()

    context = {
        "title": "Shared Lists",
        "lists": List.objects.all(),
        "viewers": viewers,
    }

    return render(request, "listApp/shared.html", context)

##################################################
@method_decorator(login_required, name='dispatch')
class ListsListView(ListView):
    model = List
    template_name = 'listApp/index.html'
    context_object_name = 'lists'

@method_decorator(login_required, name='dispatch')
class ListsDetailView(DetailView):
    model = List
    template_name = 'listApp/details.html'
##################################################

@method_decorator(login_required, name='dispatch')
class ListsCreateView(CreateView):
    model = List
    template_name = 'listApp/form.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ListsUpdateView(UserPassesTestMixin, UpdateView):
    model = List
    template_name = 'listApp/form_update.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        currList = self.get_object()
        if self.request.user == currList.author:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ListsDeleteView(UserPassesTestMixin, DeleteView):
    model = List
    template_name = 'listApp/confirm_delete.html'
    success_url = '/'

    def test_func(self):
        currList = self.get_object()
        if self.request.user == currList.author:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ElementsDetailView(DetailView):
    model = Element
    template_name = 'listApp/elementdetails.html'

@method_decorator(login_required, name='dispatch')
class ElementsUpdateView(UserPassesTestMixin, UpdateView):
    model = Element
    template_name = 'listApp/form_update_elem.html'
    fields = ['name', 'links', 'images']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        currElem = self.get_object()
        if self.request.user == currElem.author:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ElementsDeleteView(UserPassesTestMixin, DeleteView):
    model = Element
    template_name = 'listApp/confirm_delete_elem.html'
    success_url = '/'

    def test_func(self):
        currElem = self.get_object()
        if self.request.user == currElem.author:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ViewersDetailView(DetailView):
    model = Viewer
    template_name = 'listApp/viewerdetails.html'

@method_decorator(login_required, name='dispatch')
class ViewersDeleteView(UserPassesTestMixin, DeleteView):
    model = Viewer
    template_name = 'listApp/confirm_delete_viewer.html'
    success_url = '/'

    def test_func(self):
        currViewer = self.get_object()
        if self.request.user == currViewer.author:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class ViewersCreateView(CreateView):
    model = Viewer
    template_name = 'listApp/form_viewer.html'
    fields = ['viewer']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.theList = List.objects.get(pk = self.kwargs['pk'])
        return super().form_valid(form)

class elementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'links', 'images']
