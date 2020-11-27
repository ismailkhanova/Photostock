from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Picture, Category



class PictureList(ListView):
    model = Picture
    template_name = 'pictures/my_picture_list.html'
    context_object_name = 'pics_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context



class PictureOwnerList(LoginRequiredMixin, ListView):
    model = Picture
    template_name = 'pictures/my_picture_list.html'
    context_object_name = 'pics_list'

    def get_queryset(self):
        return Picture.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


class PictureDetail(DetailView):
        model = Picture
        context_object_name = "pic"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cat_menu"] = Category.objects.all()
            if self.request.user.is_authenticated:
                if Picture.objects.filter(user=self.request.user).exists():
                    context["download"] = True
            return context


class PictureCreate(LoginRequiredMixin, CreateView):
        model = Picture
        fields = ['title', 'picture', 'category', 'description']
        success_url = reverse_lazy('picture_list')

        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cat_menu"] = Category.objects.all()
            return context


class PictureUpdate(LoginRequiredMixin, UpdateView):
        model = Picture
        fields = ['title', 'picture', 'category', 'description']
        success_url = reverse_lazy('picture_list')


        def dispatch(self, request, *args, **kwargs):
            obj = self.get_object()
            if obj.user != self.request.user:
                raise Http404("Вы не являетесь владельцем этой публикации, чтобы редактировать её")
            return super(PictureUpdate, self).dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cat_menu"] = Category.objects.all()
            return context


class PictureDelete(LoginRequiredMixin, DeleteView):
    model = Picture
    fields = ['title', 'picture', 'description']
    success_url = reverse_lazy('picture_list')


    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("Вы не являетесь владельцем этой публикации, чтобы удалить её")
        return super(PictureDelete, self).dispatch(request, *args, **kwargs)

class PictureCategory(ListView):
    model = Picture
    template_name = 'pictures/categories.html'
    context_object_name = 'pic_list'

    def get_queryset(self):
        picture_type = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Picture.objects.filter(category=picture_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context

