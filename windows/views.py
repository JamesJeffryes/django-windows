from django.shortcuts import render, reverse, redirect, render_to_response, get_object_or_404
from django.views import generic

from .forms import DonorIdForm, SelectForm, SubmitForm
from .models import Window, Donor
from .tasks import send_next_email


class IndexView(generic.FormView):
    template_name = 'windows/index.html'
    form_class = DonorIdForm

    def form_valid(self, form):
        obj = get_object_or_404(Donor, pk=form.cleaned_data['donor_id'])
        return redirect('windows:donor', pk=form.cleaned_data['donor_id'])


class DonorView(generic.UpdateView):
    model = Donor
    template_name_suffix = '_update_form'
    fields = ['first_name', 'last_name', 'email_address']
    success_url = 'select'


class SelectView(generic.FormView):
    form_class = SelectForm
    template_name = 'windows/select.html'
    success_url = 'confirm'

    def form_valid(self, form):
        self._update_windows(form)
        redirect('windows:confirm', pk=self.kwargs['pk'])
        return super().form_valid(form)

    def _update_windows(self, form):
        donor = Donor.objects.get(donor_id=self.kwargs['pk'])
        old_w = Window.objects.filter(sponsor=donor).first()
        if old_w:
            old_w.sponsor = None
            old_w.plaque = ''
            old_w.save()
        new_w = Window.objects.get(pk=form.cleaned_data['window'].id)
        new_w.sponsor = donor
        new_w.plaque = form.cleaned_data['plaque']
        new_w.save()
        donor.responded = True
        donor.save()


class ConfirmView(generic.edit.FormMixin, generic.DetailView):
    model = Donor
    template_name = 'windows/confirm.html'
    form_class = SubmitForm
    success_url = '/windows/list'

    def add_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context['window'] = Window.objects.get(sponsor=self.object)
        return context

    def post(self, request, *args, **kwargs):
        send_next_email()
        form = self.get_form()
        return self.form_valid(form)


class ListView(generic.ListView):
    model = Window
