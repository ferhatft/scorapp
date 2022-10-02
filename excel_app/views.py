from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from scorfonksiyonlari.decorators import authUser
from verify_email.email_handler import send_verification_email

from excel_app.forms import CustomUserForm, SignupForm

#from django.db.models import Count


def permissionDenied(request):
    return render(request, "permission_denied.html")


@authUser(permission_user="kontrolcu")
@authUser(permission_user="denetci")
@authUser(permission_user="bakimci")
def home(request):
    if request.user.is_authenticated and not request.user.profile.kontrolcu:
        return redirect("/bakimRapor/")
    elif request.user.is_authenticated and request.user.profile.kontrolcu:
        return redirect("/kontrolRaporlar/")
    return render(request, "login.html")



# Sign Up View

class SignUpView(CreateView):
    form_class = SignupForm
    success_url = "/"
    template_name = 'register.html'

    def form_valid(self, form):
        username, password, email = form.cleaned_data.get('username'), form.cleaned_data.get('password1'), form.cleaned_data.get("email")
        if "@ms.asay.com.tr" in email:

            inactive_user = send_verification_email(self.request, form)
            return render(self.request, "register.html", {"msg": "Hesabınız Başarıyla Oluşturuldu, Mail Adresinize Gönderilen Aktivasyon Linkiyle Lütfen Hesabınızı Doğrulayın."})

        else:
            form.save()
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()

            return render(self.request,"register.html", {"msg": "Hesabınız Başarıyla Oluşturuldu Ama Üyeliğiniz Aktif Değil Lütfen Yöneticiyle İrtibata Geçiniz"})

    def dispatch(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(auth_views.LoginView):
    template_name = "login.html"
    form_class = CustomUserForm

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data.get("username"))
        if user.check_password(form.cleaned_data.get("password")) and not user.is_active:
            msg = ""
            if "@ms.asay.com.tr" in user.email:
                msg = "Lütfen Hesabınızı E-mail Adresinize Gelen Linkten Aktif Ediniz."
            else:
                msg = "Hesabınız Aktif Değil Lütfen Yöneticiyle İrtibata Geçin"

            return render(self.request, "login.html", {"msg": msg})
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if(request.user.is_authenticated and request.user.profile.bakimci):
            return redirect("/bakimRapor")
        elif (request.user.is_authenticated and request.user.profile.kontrolcu):
            return redirect("/kontrolRaporlar")
        elif (request.user.is_authenticated and request.user.profile.denetci):
            return redirect("/bakimRapor")
        elif (request.user.is_authenticated):
            return render(request, "permission_denied.html")

        return super().dispatch(request, *args, **kwargs)
