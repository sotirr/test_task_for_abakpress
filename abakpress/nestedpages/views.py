import re
from typing import List

from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import QuerySet

from .models import Page
from .forms import PageForm


class StaticPageView(View):

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        form = PageForm
        if url.endswith('/add') or url.startswith('add'):
            form = PageForm
            return render(request, 'nestedpages/create_page.html', context={'form': form})
        elif url.endswith('/edit'):
            url = re.search(r'(?P<url>.*)(add|edit)', url).group(1)
            instance: QuerySet = Page.objects.get(url=url)
            form = PageForm(instance=instance)
            return render(request, 'nestedpages/create_page.html', context={'form': form})
        else:
            page_data: QuerySet = get_object_or_404(Page, url=url)
            context: dict = self.generate_data_for_page(url, page_data)
        return render(request, 'nestedpages/index.html', context=context)

    def post(self, request: HttpRequest, url: str) -> HttpResponse:
        pars_url = re.search(r'(?P<url>.*)(?P<method>add|edit)', url)
        base_url: str = pars_url.group(1)
        method: str = pars_url.group(2)
        if method == 'edit':
            self.edit_form(request, base_url)
        else:
            self.create_form(request, base_url)

    def edit_form(self, request: HttpRequest, url:str) -> HttpResponse:
        instance: QuerySet = Page.objects.get(url=url)
        bound_form = PageForm(request.POST, instance=instance)
        if bound_form.is_valid():
            page_instance = bound_form.save(commit=False)
            page_instance.url = url
            page_instance.save()
            return redirect(page_instance.get_absolute_url())
        return render(request, 'nestedpages/create_page.html',
                      context={'form': bound_form})
    
    def create_form(self, request: HttpRequest, url:str)  -> HttpResponse:
        full_url: str = url + request.POST['name'] + '/'
        bound_form = PageForm(request.POST)
        if bound_form.is_valid():
            page_instance = bound_form.save(commit=False)
            page_instance.url = full_url
            page_instance.parent_url = url
            page_instance.save()
            return redirect(page_instance.get_absolute_url())
        return render(request, 'nestedpages/create_page.html',
                      context={'form': bound_form})

    def generate_data_for_page(self, url: str, page_data: QuerySet) -> dict:
        children: QuerySet = Page.objects.all().filter(parent_url=url)
        context = {
            'name': page_data.name, 
            'head': page_data.head, 
            'content': page_data.content,
            'own_url': page_data.get_absolute_url(),
            'children': children,
        }
        return context

