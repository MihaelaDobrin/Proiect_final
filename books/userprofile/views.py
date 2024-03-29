import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from userprofile.forms import NewAccountForm

punctuation = '!$@?$@'


class UpdateProfile(LoginRequiredMixin, UpdateView):
    form_class = NewAccountForm
    model = User
    template_name = 'registration/new_account.html'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super(UpdateProfile, self).get_form_kwargs()
        kwargs.update({'pk':self.kwargs['pk'], 'state':'update'})
        return kwargs

    def get_succes_url(self):
        return reverse('catalog:home')


class CreateNewUser(CreateView):
    form_class = NewAccountForm
    model = User
    template_name = 'registration/new_account.html'

    def get_form_kwargs(self):
        kwargs = super(CreateNewUser, self).get_form_kwargs()
        kwargs.update({'pk':None, 'state':'create'})
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save(commit=False)
        return super(CreateNewUser, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateNewUser, self).form_invalid(form)

    def get_success_url(self):
        psw = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + punctuation)
            for _ in range(8))
        try:
            user_instance = User.objects.get(id=self.object.id)
            user_instance.set_password(psw)
            user_instance.save()
            content_email = f'Your username and password: {user_instance.username} {psw}'
            msg_html = render_to_string('emails/invite_user.html', {'content_email': str(content_email)})
            msg = EmailMultiAlternatives(subject='You are invited', body=content_email, from_email='contact@test.ro',
                                         to=[user_instance.email])
            msg.attach_alternative(msg_html, 'text/html')
            msg.send()
        except Exception:
            pass
        return reverse('login')