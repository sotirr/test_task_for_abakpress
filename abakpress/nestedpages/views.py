import re
from typing import List

from django.views import View
from django.views.generic import CreateView, UpdateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import QuerySet

from .models import Page
from .forms import CreatePageForm, EditPageForm


class StaticPageView(View):

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        page_data: QuerySet = get_object_or_404(Page, url=url)
        context: dict = self.generate_data_for_page(url, page_data)
        return render(request, 'nestedpages/index.html', context=context)

    def generate_data_for_page(self, url: str, page_data: QuerySet) -> dict:
        children: QuerySet = Page.objects.all().filter(parent=page_data)
        context = {
            'name': page_data.name, 
            'head': page_data.head, 
            'content': page_data.content,
            'own_url': page_data.get_absolute_url(),
            'children': children,
        }
        return context


class CreateStaticPageView(View):
    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        form = CreatePageForm
        return render(request, 'nestedpages/create_page.html', context={'form': form})
    
    def post(self, request: HttpRequest, url: str) -> HttpResponse:
        full_url: str = url + request.POST['name'] + '/'
        parent = Page.objects.filter(url=url).first()
        bound_form = CreatePageForm(request.POST)
        if bound_form.is_valid():
            page_instance = bound_form.save(commit=False)
            page_instance.url = full_url
            page_instance.parent = parent
            page_instance.save()
            return redirect(page_instance.get_absolute_url())
        return render(request, 'nestedpages/create_page.html',
                      context={'form': bound_form})


class EditStaticPageView(View):
    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        instance: QuerySet = Page.objects.get(url=url)
        form = EditPageForm(instance=instance)
        return render(request, 'nestedpages/create_page.html', context={'form': form})

    def post(self, request: HttpRequest, url: str) -> HttpResponse:
        instance: QuerySet = Page.objects.get(url=url)
        bound_form = EditPageForm(request.POST, instance=instance)
        if bound_form.is_valid():
            page_instance = bound_form.save()
            return redirect(page_instance.get_absolute_url())
        return render(request, 'nestedpages/create_page.html',
                      context={'form': bound_form})
