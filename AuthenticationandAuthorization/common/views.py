from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    permission_required = ['auth.view_user']