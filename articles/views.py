from django.views.generic import ListView, DetailView
from django.views.generic.edit import (UpdateView, DeleteView, CreateView)
from django.urls import reverse_lazy
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


"""
    use LoginRequiredMixin left of CreateView, To restrict view access to only logged in users,
    We want the CreateView to already know we intend to restrict access.
    we avoid resubmitting the form and access when user not log in!
    Django has automatically redirected users to the log in page.
"""


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    # to set the current user to author we need to customize it.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'


"""
    use UserPassesTestMixin => add it second in our list of mixins for BlogUpdateView.
    That means a user must first be logged in and then they must pass the user test before accessing UpdateView
    
    obj.author == self.request.user => if the author on the current object matches the current user on the webpage
    (whoever is logged in and trying to make the change), then allow it.If false, 403 error will automatically be thrown.
    
"""


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

