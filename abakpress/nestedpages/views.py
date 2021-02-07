from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import QuerySet

from .models import Page
from .forms import CreatePageForm, EditPageForm


class StaticPageView(View):
    ''' main page view '''

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        ''' renders base view of page'''
        site: str = request.get_host()
        page_data: QuerySet = get_object_or_404(Page, url=url)
        context: dict = self.generate_data_for_page(url, page_data, site)
        return render(request, 'nestedpages/index.html', context=context)

    def generate_data_for_page(self, url: str, page_data: QuerySet, site: str) -> dict:
        ''' prepares context to rendering page '''
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
        ''' creates a graph to build a tree of links '''
        tree[root] = {
            child: {} for child in Page.objects.all().filter(parent=root)
        }
        for child in tree[root]:
            self.dfs(tree[root], child)
        return tree


class CreateStaticPageView(View):
    ''' create new page '''

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        ''' renders page with creating form '''
        form = CreatePageForm
        return render(
            request, 'nestedpages/create_page.html', context={'form': form}
        )

    def post(self, request: HttpRequest, url: str) -> HttpResponse:
        ''' creates new page into db '''
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
    ''' edit exist page '''

    def get(self, request: HttpRequest, url: str) -> HttpResponse:
        ''' renders page with filling form '''
        instance: QuerySet = Page.objects.get(url=url)
        form = EditPageForm(instance=instance)
        return render(
            request, 'nestedpages/create_page.html', context={'form': form}
        )

    def post(self, request: HttpRequest, url: str) -> HttpResponse:
        ''' saves edited forms into bd'''
        instance: QuerySet = Page.objects.get(url=url)
        bound_form = EditPageForm(request.POST, instance=instance)
        if bound_form.is_valid():
            page_instance = bound_form.save()
            return redirect(page_instance.get_absolute_url())
        return render(request, 'nestedpages/create_page.html',
                      context={'form': bound_form})
