from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View

from django.urls.base import reverse

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationForm
from accounts.models import Account


# verificatio mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.models import Cart

# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=email, password=password)
            user.phone_number = phone
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email

            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email='+email)

        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


class LoginView(View):
    def get(self, request):
        ctx = {}
        if request.GET.get('next'):
            ctx['next'] = request.GET.get('next')
        return render(request, 'accounts/login.html', ctx)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        old_cart = request.cart
        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            cart = user.carts.all().order_by('-date_added').first()
            if not cart:
                cart = Cart.from_request(request)
                user.carts.add(cart)

            cart.transfer_from(old_cart)
            """   if not user.carts.count() and request.cart.cart_items:
                  user.carts.add(request.cart)
                  user.save() """
            if (request.POST.get('next')):
                return redirect(request.POST.get('next'))
            # messages.success(request, 'Your are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong email or password')
            return render(request, 'accounts/login.html')


class LogoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        auth.logout(request)
        return redirect('home')


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, 'Congratulations! Your account is activated.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link')
            return redirect('register')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        messages.success(
            request, f'Welcome back {request.user.first_name}')
        return render(request, 'accounts/dashboard.html')


class PasswordRecoveryView(View):

    def get(self, request, uidb64="", token=""):
        if not uidb64 or not token:
            return render(request, 'accounts/password_recovery.html')
        else:
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = Account._default_manager.get(pk=uid)
            except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
                user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'accounts/password_recovery.html', {
                'email': user.email,
                'verified': True,
                'token': token
            })
        else:
            return render(request, 'accounts/password_recovery.html', {
                'expired': True
            })

    def post(self, request):
        email = request.POST.get('email')
        user_id = request.POST.get('user_id')
        token = request.POST.get('token')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if token:
            user = Account.objects.get(email=email)
            checked = default_token_generator.check_token(user, token)
            if checked and password == repeat_password:
                user.set_password(password)
                user.save()
                messages.success(
                    request, f'Your password has been successfully changed!')
                return redirect('login')
            else:
                messages.error(request, f'Password verification failed')
                return redirect('login')
        if email:
            try:
                user = Account.objects.get(email=email)
                current_site = get_current_site(request)
                mail_subject = 'Password recovery'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk)),
                message = render_to_string('accounts/password_recovery_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': uid,
                    'token': token
                })

                to_email = email

                if settings.DEBUG:
                  # % url 'password-recovery-link' uidb64=uid token=token %}
                    url = reverse('password-recovery-link',
                                  kwargs={'uidb64': uid, 'token': token})
                    messages.warning(
                        request, f'http://{current_site}/{url}')

                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

            except:
                pass
        messages.info(
            request, f'A verification email has been sent to {email}. Please check the mailbox.')
        return redirect('login')

# chiedo email
# faccio post
# verifico se mail esiste
# preparo messaggio e mando mail con token univoco, scrivo poi un messaggio di cortesia e link alla login
# nell'email link
# nella view associata al link recupero utente e token
# verifico se sono buoni e nel caso mando a pagina con inserimento e conferma password
# a salvataggio avvenuto mando a pagina di login
