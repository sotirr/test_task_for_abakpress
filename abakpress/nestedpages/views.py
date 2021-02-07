import re

from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import QuerySet

from .models import Page
from .forms import CreatePageForm, EditPageForm


class StaticPageView(View):

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        site: str = request.get_host()
        page_data: QuerySet = get_object_or_404(Page, url=url)
        context: dict = self.generate_data_for_page(url, page_data, site)
        return render(request, 'nestedpages/index.html', context=context)

    def generate_data_for_page(self, url: str, page_data: QuerySet, site: str) -> dict:
        children: QuerySet = Page.objects.all().filter(parent=page_data)
        tree = {}
        relatives = self.dfs(tree, page_data)
        context = {
            'name': page_data.name,
            'head': page_data.head,
            'content': page_data.convert_to_html(site),
            'own_url': page_data.get_absolute_url(),
            'children': children,
            'relatives': relatives
        }
        return context

    def dfs(self, tree, root):
        tree[root] = {child: {} for child in Page.objects.all().filter(parent=root)}
        for child in tree[root]:
            self.dfs(tree[root], child)
        return tree

    def convert_to_html(self, site):
        regex_bold = r'\*\*(.+?)\*\*'
        regex_italic = r'\\\\(.+?)\\\\'
        regex_link = r'\(\((.+?) (.+?)\)\)'
        replace_bold = r'<b>\1</b>'
        replace_italic = r'<i>\1</i>'
        replace_link = r'<a href="http://localhost/\1">\2</a>'
        replaced_bold = re.sub(regex_bold, replace_bold, self.content)
        replaced_italic = re.sub(regex_italic, replace_italic, replaced_bold)
        replaced_link = re.sub(regex_link, replace_link, replaced_italic)
        return replaced_link


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
