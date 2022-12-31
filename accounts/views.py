from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import EmailMultiAlternatives
import random
from django.views.decorators.cache import never_cache
import string
from .models import VerificationUser
from django.views.decorators.csrf import csrf_exempt
from main.models import Exam, UserExam
from django.contrib.auth import logout
from .forms import SignUpForm, UserUpdateForm, AddpermselectForm, SignUpExamForm, LoginForm, ProfileUserForm, ProfileAdminForm

# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'
@csrf_exempt
@never_cache
def SignUp(request):
    letters_and_digits = string.digits
    result_digit = ''.join((random.choice(letters_and_digits) for i in range(5)))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password1'] = form.cleaned_data['password1']
            request.session['email'] = form.cleaned_data['email']
            email = form.cleaned_data['email']
            subject = 'کد تایید'
            from_email = 'info@msn80.com' 
            to = email
            text_content = 'site'
            html_content = "<html lang='fa'><head><title></title></head><body style='text-align: right;'><div style='width:800px;background:#fff;align-text:center;text-align: center;'><div><h1 style='text-align: center;'><a href='https://www.msn80.com/'>سایت ام اس ان هشتاد</a></h1></div><hr width='100%' size='2' color='#A4168E'><div style='width:50%;height:20px; float: right;text-align: right;;margin-top:-32px;padding-right:390px;'></div><h2 style='text-align:right;'>درود به شما</h2></br><h3>.از اینکه در ام اس ان هشتاد میزبان شما هستیم صمیمانه خوشحالیم. لطفا برای فعال شدن حساب کاربری از کد زیر استفاده کنید. این امر به ما کمک میکند بتوانیم افتخار ارائه خدمت به شما را داشته باشیم</h3><h1 style='text-align:center;color:#B24909;'>کد تایید ثبت نام</h1><hr/><div style='height:210px;'><h1 style='align-text:center;text-align: center;background: #e5f3e3;'>"+result_digit+"</h1></div></div> </body></html>"
            message = EmailMultiAlternatives(subject, text_content, from_email, [to])
            message.attach_alternative(html_content, "text/html")
            message.send()
            form.save()
            user_exam = UserExam.objects.get(email=email)
            print(user_exam)
            VerificationUser.objects.create(UserExam_id = user_exam.id,user_email = email,verification_code = result_digit)
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('verification')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@csrf_exempt
@never_cache
def SignUpExam(request,pk):
    exam_name  = Exam.objects.get(pk=pk)
    request.session['url'] = request.GET.get("next", None)
    letters_and_digits = string.digits
    result_digit = ''.join((random.choice(letters_and_digits) for i in range(5)))
    if request.method == 'POST':
        form = SignUpExamForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password1'] = form.cleaned_data['password1']
            request.session['email'] = form.cleaned_data['email']
            email = form.cleaned_data['email']
            subject = 'کد تایید'
            from_email = 'info@msn80.com' 
            to = email
            text_content = 'site'
            html_content = "<html lang='fa'><head><title></title></head><body style='text-align: right;'><div style='width:800px;background:#fff;align-text:center;text-align: center;'><div><h1 style='text-align: center;'><a href='https://www.msn80.com/'>سایت ام اس ان هشتاد</a></h1></div><hr width='100%' size='2' color='#A4168E'><div style='width:50%;height:20px; float: right;text-align: right;;margin-top:-32px;padding-right:390px;'></div><h2 style='text-align:right;'>درود به شما</h2></br><h3>.از اینکه در ام اس ان هشتاد میزبان شما هستیم صمیمانه خوشحالیم. لطفا برای فعال شدن حساب کاربری از کد زیر استفاده کنید. این امر به ما کمک میکند بتوانیم افتخار ارائه خدمت به شما را داشته باشیم</h3><h1 style='text-align:center;color:#B24909;'>کد تایید ثبت نام</h1><hr/><div style='height:210px;'><h1 style='align-text:center;text-align: center;background: #e5f3e3;'>"+result_digit+"</h1></div></div> </body></html>"
            message = EmailMultiAlternatives(subject, text_content, from_email, [to])
            message.attach_alternative(html_content, "text/html")
            message.send()
            form.save()
            user_exam = UserExam.objects.get(email=email)
            print(user_exam)
            VerificationUser.objects.create(UserExam_id=user_exam.id,user_email = email,verification_code = result_digit)
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect(reverse('verification_exam'))
    else:
        form = SignUpExamForm()
    return render(request, 'user/screen/signup-user-exam.html', {'form': form,'pk':pk,'exam_name':exam_name})

@never_cache
def ForgetPassword(request):
    letters_and_digits = string.digits
    result_digit = ''.join((random.choice(letters_and_digits) for i in range(5)))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password1'] = form.cleaned_data['password1']
            request.session['email'] = form.cleaned_data['email']
            email = form.cleaned_data['email']
            subject = 'کد رهگیری'
            from_email = 'info@msn80.com' 
            to = email
            text_content = 'site'
            html_content = "<html lang='fa'><head><title></title></head><body style='text-align: right;'><div style='width:800px;background:#fff;align-text:center;text-align: center;'><div><h1 style='text-align: center;'><a href='https://www.msn80.com/'>سایت ام اس ان هشتاد</a></h1></div><hr width='100%' size='2' color='#A4168E'><div style='width:50%;height:20px; float: right;text-align: right;;margin-top:-32px;padding-right:390px;'></div><h2 style='text-align:right;'>درود به شما</h2></br><h3>.از اینکه در ام اس ان هشتاد میزبان شما هستیم صمیمانه خوشحالیم. لطفا برای فعال شدن حساب کاربری از کد زیر استفاده کنید. این امر به ما کمک میکند بتوانیم افتخار ارائه خدمت به شما را داشته باشیم</h3><h1 style='text-align:center;color:#B24909;'>کد تایید ثبت نام</h1><hr/><div style='height:210px;'><h1 style='align-text:center;text-align: center;background: #e5f3e3;'>"+result_digit+"</h1></div></div> </body></html>"
            message = EmailMultiAlternatives(subject, text_content, from_email, [to])
            message.attach_alternative(html_content, "text/html")
            message.send()
            form.save()
            VerificationUser.objects.create(user_email = email,verification_code = result_digit)
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('verification')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class Meta(UserCreationForm.Meta):
    pass

@never_cache
@csrf_exempt
def Verification(request):
    verification_code = request.POST.get('verification', None)
    email = request.session['email']
    username = request.session['username']
    password1 = request.session['password1']
    if verification_code:
        verification = VerificationUser.objects.filter(user_email = email,verification_code = verification_code)
        if verification:
            UserExam.objects.filter(email = email).update(is_active = True,is_admin_exam=True)
            user = authenticate(request, username=username,password=password1)
            login(request, user)
            return redirect('dashboard')
        elif not verification:
            messages.error(request,'کد تایید اشتباه می باشد، دوباره سعی کنید.')
    elif not verification_code:
        messages.info(request,'کد تایید را وارد کنید.')
    return render(request, 'verification.html')

@csrf_exempt
@never_cache
def SignUpResend(request):
    letters_and_digits = string.digits
    result_digit = ''.join((random.choice(letters_and_digits) for i in range(5)))
    email = request.session['email']
    subject = 'کد تایید'
    from_email = 'info@msn80.com' 
    to = email
    text_content = 'site'
    html_content = "<html lang='fa'><head><title></title></head><body style='text-align: right;'><div style='width:800px;background:#fff;align-text:center;text-align: center;'><div><h1 style='text-align: center;'><a href='https://www.msn80.com/'>سایت ام اس ان هشتاد</a></h1></div><hr width='100%' size='2' color='#A4168E'><div style='width:50%;height:20px; float: right;text-align: right;;margin-top:-32px;padding-right:390px;'></div><h2 style='text-align:right;'>درود به شما</h2></br><h3>.از اینکه در ام اس ان هشتاد میزبان شما هستیم صمیمانه خوشحالیم. لطفا برای فعال شدن حساب کاربری از کد زیر استفاده کنید. این امر به ما کمک میکند بتوانیم افتخار ارائه خدمت به شما را داشته باشیم</h3><h1 style='text-align:center;color:#B24909;'>کد تایید ثبت نام</h1><hr/><div style='height:210px;'><h1 style='align-text:center;text-align: center;background: #e5f3e3;'>"+result_digit+"</h1></div></div> </body></html>"
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.send()
    user_exam = UserExam.objects.get(email=email)
    VerificationUser.objects.create(UserExam_id = user_exam.id,user_email = email,verification_code = result_digit)
    return redirect('verification')
    return render(request, 'verification.html')

@never_cache
@csrf_exempt
def VerificationExam(request):
    nx = request.session['url']
    verification_code = request.POST.get('verification', None)
    email = request.session['email']
    username = request.session['username']
    password1 = request.session['password1']
    if verification_code:
        verification = VerificationUser.objects.filter(user_email = email,verification_code = verification_code)
        if verification:
            UserExam.objects.filter(email = email).update(is_active = True,is_user_exam=True)
            user = authenticate(request, username=username,password=password1)
            login(request, user)
            if nx:
                return redirect(nx)
            return redirect(reverse('quiz-list-exam', args=[request.user.exam_id]))
        elif not verification:
            messages.error(request,'کد تایید اشتباه می باشد، دوباره سعی کنید.')
        elif verification_code.isdigit() == False:
            messages.info(request,'لطفا کد تایید را درست وارد کنید.')
        elif not verification_code:
            messages.info(request,'کد تایید را وارد کنید.')
    return render(request, 'verification.html')

@never_cache
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'رمز ورود شما با موفقیت به روز شد!')
            return redirect('change_password')
        else:
            messages.error(request, 'لطفا خطای زیر را اصلاح کنید.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {
        'form': form
    })

@never_cache
def ListUser(request):
    userlist = User.objects.all()
    return render(request, 'userlist.html',{'userlist':userlist})

@never_cache
def UserChangePasswordView(request, pk): 
    context ={} 
    obj = get_object_or_404(User, pk = pk) 
    form = UserUpdateForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('list_user'))
    context["form"] = form 
    return render(request, "change-pass-user.html", context) 

@never_cache
def UserDeleteView(request,id):
    User.objects.get(id=id).delete()
    return redirect(reverse('list_user'))

@never_cache
def AddPermView(request, id):
    context ={} 
    obj = get_object_or_404(UserExam, id = id) 
    form = AddpermselectForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('user_list'))
    context["form"] = form 
    return render (request, 'Addpermselect.html', context)

@never_cache
def ProfileUserView(request, id):
    context ={} 
    obj = get_object_or_404(UserExam, id = id) 
    form = ProfileUserForm(request.POST or None, instance = obj) 
    if form.is_valid():
        meli = form.cleaned_data.get("meli")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        address = form.cleaned_data.get("address")
        if not meli:
            UserExam.objects.filter(pk = request.user.id).update(first_name = first_name,last_name = last_name,address = address)
            return redirect(reverse('dashboard_user'))
        else: 
            UserExam.objects.filter(pk = request.user.id).update(meli = meli,first_name = first_name,last_name = last_name,address = address)
            return redirect(reverse('dashboard_user'))
    context["form"] = form 
    return render (request, 'ProfileUserScreen.html', context)

@never_cache
def ProfileAdminView(request, id):
    context ={} 
    obj = get_object_or_404(UserExam, id = id) 
    form = ProfileAdminForm(request.POST or None, instance = obj) 
    if form.is_valid():
        meli = form.cleaned_data.get("meli")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        address = form.cleaned_data.get("address")
        mobile = form.cleaned_data.get("mobile")
        if not meli:
            UserExam.objects.filter(pk = request.user.id).update(first_name = first_name,last_name = last_name,address = address,mobile = mobile)
            return redirect(reverse('dashboard'))
        else: 
            UserExam.objects.filter(pk = request.user.id).update(meli = meli,first_name = first_name,last_name = last_name,address = address,mobile = mobile)
            return redirect(reverse('dashboard'))
    context["form"] = form 
    return render (request, 'ProfileAdminScreen.html', context)

@never_cache
@csrf_exempt
def loginExamUser(request,pk):
    nxt = request.GET.get("next", None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            try:
                fill = UserExam.objects.get(username=username)
                if fill.is_user_exam == 1:
                    if account is not None:
                        login(request, account)
                        if nxt:
                            return redirect(nxt)
                        else:
                            return redirect(reverse('quiz-list-exam',args=[fill.exam_id]))
                    else:
                        return redirect(reverse('login-user-exam',args=[pk]))
                else:
                    return redirect(reverse('login-user-exam',args=[pk]))
            except:
                return redirect(reverse('login-user-exam',args=[pk]))
        else:
            exam_login = Exam.objects.get(pk = pk)
            context = {'form':form,'pk':pk,'exam_login':exam_login}
            messages.error(request,'نام کاربری یا رمز عبور درست وارد نشده، لطفا دوباره سعی کنید.')
            #messages.add_message(request, messages.ERROR, "نام کاربری یا رمز عبور درست وارد نشده، لطفا دوباره سعی کنید.")
    else:
        form = LoginForm()
        exam_login = Exam.objects.get(pk = pk)
        context = {'form':form,'pk':pk,'exam_login':exam_login}
    return render(request, 'registration/login-user-exam.html', context)

@never_cache
@csrf_exempt
def loginExamAdmin(request):
    nxt = request.GET.get("next", None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            fill_check = UserExam.objects.filter(username=username)
            if fill_check:
                fill = UserExam.objects.get(username=username)
            else:
                return render(request, 'registration/login.html', context)
            if fill.is_admin_exam == 1:
                if account is not None:
                    login(request, account)
                    if nxt:
                        return redirect(nxt)
                    else:
                        return redirect(reverse('exam-list'))
                else:
                    return render(request, 'registration/login.html', context)
            else:
                return render(request, 'registration/login.html', context)
        else:
            return render(request, 'registration/login.html', context)
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, 'registration/login.html', context)

@never_cache
@csrf_exempt
def LogoutUserExam(request,pk):
    auth.logout(request)
    return redirect(reverse('quiz-list-exam',args=[pk]))

@never_cache
@csrf_exempt
def LogoutAdminExam(request):
    auth.logout(request)
    return redirect('login-admin-exam')

@never_cache
@csrf_exempt
def loginAdmin(request):
    nxt = request.GET.get("next", None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            fill = UserExam.objects.get(username=username)
            if fill.is_superuser == 1:
                if account is not None:
                    login(request, account)
                    if nxt:
                        return redirect(nxt)
                    else:
                        return redirect(reverse('admin_dashboard'))
                else:
                    return render(request, 'registration/admin-login.html', context)
            else:
                return render(request, 'registration/admin-login.html', context)
        else:
            return render(request, 'registration/admin-login.html', context)
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, 'registration/admin-login.html', context)

@never_cache
@csrf_exempt
def LogoutAdmin(request):
    auth.logout(request)
    return redirect('login-admin')