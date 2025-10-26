from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
