# labels/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelsIndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


# E302 fix: added blank line
class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно создана"


# E302 fix: added blank line
class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно изменена"


# E302 fix: added blank line
class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            # E501 fix: wrapped line
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется"
            )
            return redirect("labels:index")
        return super().post(request, *args, **kwargs)
