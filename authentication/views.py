from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import mixins 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import user_profile_form
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView
# from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomPasswordChange,CustomPasswordResetForm,CustomSetPassword
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def register(request):
    return render(request, "access/register.html", {})

def staff_register(request):
    if request.method =="POST":
        # get data from custom html form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not first_name or not last_name or not email or not password1 or not password2:
            return HttpResponse("All fields are required!")
        
        if password1 != password2:
            return HttpResponse("Passwords doesn't match!...Try again")
        
        try:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1, is_staff=True)
            login(request, user)
            return redirect("department")
        except Exception as e:
            return HttpResponse(f"Error creating user: {str(e)}")
        
    else:
        return render(request, "access/staff_register.html", {})


def student_register(request):
    if request.method =="POST":
        # get data from custom html form
        matric_num = request.POST.get('matric_num')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not matric_num or not first_name or not last_name or not email or not password1 or not password2:
            messages.warning(request,"All fields are required!")
            return redirect("student_register")
        
        if password1 != password2:
            messages.warning(request,"Passwords doesn't match!...Try again")
            return redirect("student_register")
      
        
        try:
            user = User.objects.create_user(username=matric_num, first_name=first_name, last_name=last_name, email=email, password=password1)
            login(request, user)
            messages.success(request,"user account created")
            return redirect("department")
        except Exception as e:
            messages.error(request,f"Student with {matric_num} exist")
            return redirect("student_register")
        
    else:
        return render(request, "access/student_register.html", {})
    

@login_required
def department_form(request):
    form = user_profile_form()
    if request.method =="POST":
        form = user_profile_form(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            try:
                pre_form = form.save(commit=False)
                pre_form.user = request.user
                pre_form.save()
                user = User.objects.get(username=request.user)
                user.is_active = False
                user.save()
                messages.warning(request, "visit the library to activate your account")
                return redirect("login")
            except Exception as e:
                return HttpResponse(f"Error {str(e)}")
        else:
            print(form.errors)
            messages.warning(request, "in valid form inputs")
            return redirect("department")
    
    return render(request, "access/department.html", {"form": form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user authentication(checks if credendials are correct)
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if user.username == "admin":
                login(request, user)
                return redirect("index")
            else:
                try:
                    messages.success(request,"login success")
                    login(request, user)
                    request.user.profile
                    print(request.user.profile)
                    return redirect("user_index")
                except Exception:
                    messages.success(request,"Set up your account to proceed")
                    login(request, user)
                    return redirect("department")
        else:
            messages.warning(request,"the password or username is wrong")
    else:
        pass
    return render(request, "access/login.html", {})


def logout_user(request):
    try:
        logout(request)
    except Exception as e:
        return HttpResponse(f"Error {e}")
    return redirect("login")

@login_required
def change_password(request):
    form = CustomPasswordChange(user=request.user)

    if request.method == "POST":
        form = CustomPasswordChange(user=request.user, data=request.POST)
        # if request.POST["new_password1"] and request.POST["new_password2"] and request.POST["old_password"] :
        #     messages.error(request, "⚠️ ")
        #     return redirect("change_pwd")  
        if request.POST["new_password1"] != request.POST["new_password2"]:
            messages.error(request, "⚠️ password does not match")
            return redirect("change_pwd")  
        if form.is_valid():
            user = form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "✅ Your password has been updated successfully!")
            return redirect("user_index")  
        else:
            messages.error(request, "⚠️ Password is too similar to username or too not valid.")
    context = {"form":form}
    return render(request,"user/change_password.html", context)
# views.py
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.core.mail import send_mail
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def password_reset_request(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         try:
#             user = User.objects.get(email=email)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")

#             # send reset link by email
#             send_mail(
#                 "Password Reset Request",
#                 f"Click the link to reset your password: {reset_link}",
#                 "no-reply@example.com",
#                 [email],
#             )

#             messages.success(request, "✅ Check your email for a reset link.")
#             return redirect("login")
#         except User.DoesNotExist:
#             messages.error(request, "⚠️ No user found with this email.")

#     return render(request, "accounts/password_reset_request.html")
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import SetPasswordForm

# UserModel = get_user_model()

# def password_reset_confirm(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = UserModel.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == "POST":
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "✅ Your password has been reset. You can now log in.")
#                 return redirect("login")
#         else:
#             form = SetPasswordForm(user)
#         return render(request, "accounts/password_reset_confirm.html", {"form": form})
#     else:
#         messages.error(request, "⚠️ Invalid or expired reset link.")
#         return redirect("password_reset_request")

# utils/secure_url.py
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.core.signing import Signer, BadSignature

# signer = Signer()

# def encode_secure(value):
#     """
#     Encode and sign a value for safe use in URLs.
#     """
#     # base64 encode
#     encoded = urlsafe_base64_encode(force_bytes(value))
#     # sign the encoded value
#     signed = signer.sign(encoded)  
#     return signed   # looks like: "MTIz:randomsignature"

# def decode_secure(signed_value):
#     """
#     Decode and verify a signed value from URLs.
#     """
#     try:
#         # verify signature
#         unsigned = signer.unsign(signed_value)
#         # decode base64 back to original
#         decoded = urlsafe_base64_decode(unsigned).decode()
#         return decoded
#     except (BadSignature, ValueError, TypeError):
#         return None   # invalid or tampered
# from utils.secure_url import decode_secure
# from django.http import HttpResponse, Http404

# def profile_view(request, token):
#     user_id = decode_secure(token)
#     if not user_id:
#         raise Http404("Invalid or tampered link")

#     return HttpResponse(f"Showing profile for user {user_id}")
# from utils.secure_url import encode_secure

# def get_profile_link(user):
#     token = encode_secure(user.pk)
#     return f"/profile/{token}/"

def landing_page(request):
    return render(request,"access/landing.html")

class CustomPasswordReset(PasswordResetView):
    template_name = "access/password_reset.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    email_template_name = "access/password_reset_email.html"

# class CustomPasswordResetDone(PasswordResetDoneView):
#     template_name = "access/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPassword
    template_name = "access/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(request,"password does not match")
        return super().post(request, *args, **kwargs)
    
    