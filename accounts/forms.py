from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from main.models import UserExam
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),required=True)
    is_admin_exam = forms.BooleanField(required=False, initial=True)
    agree = forms.BooleanField(required=True)
    class Meta:
        model = UserExam
        fields = ('username', 'email', 'password1', 'password2','is_active','is_admin_exam','agree')
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserExam.objects.filter(email=email).exists():
            raise ValidationError("ایمیل دیگری وارد کنید، این ایمیل وجود دارد.")
        return email

class SignUpExamForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),required=True)
    agree = forms.BooleanField(required=True)
    class Meta:
        model = UserExam
        fields = ('username', 'email', 'password1', 'password2','is_active','is_user_exam','exam_id','agree')
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserExam.objects.filter(email=email).exists():
            raise ValidationError("ایمیل دیگری وارد کنید، این ایمیل وجود دارد.")
        return email

class UserUpdateForm(UserCreationForm):
    username = forms.CharField(disabled=True,label='نام کاربر')

    class Meta:
        model = UserExam
        fields = ('username', 'password1', 'password2')

class AddpermselectForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','style':'text-align:center;font-size:20px;'}),disabled=True,label='نام کاربر')
    #user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control','style':'height:100%;'}))
    #user_permissions = forms.ModelMultipleChoiceField(required=False,label='دسترسی های کاربر',queryset=Permission.objects.filter(name__contains = 'faza'),widget=forms.CheckboxSelectMultiple)
    #user_permissions = forms.ModelMultipleChoiceField(required=False,label='دسترسی های کاربر',queryset=Permission.objects.exclude(name__icontains = 'can'),widget=forms.CheckboxSelectMultiple)
    #groups = forms.ModelMultipleChoiceField(required=False,label='گروه ها',queryset=Group.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = UserExam
        fields = ('username','is_active')

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'Username'))
    password = forms.CharField(label=(u'Pasword'), widget=forms.PasswordInput(render_value=False))

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','style':'text-align:center;font-size:20px;'}),disabled=True,label='نام کاربر')
    first_name = forms.CharField(widget=forms.TextInput(),required=True)
    last_name = forms.CharField(widget=forms.TextInput(),required=True)
    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['meli'] = forms.CharField(required=False, min_length=10, max_length=10)
    class Meta:
        model = UserExam
        fields = ('username','first_name','last_name','meli','address')

class ProfileAdminForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','style':'text-align:center;font-size:20px;'}),disabled=True,label='نام کاربر')
    first_name = forms.CharField(widget=forms.TextInput(),required=True)
    last_name = forms.CharField(widget=forms.TextInput(),required=True)

    def __init__(self, *args, **kwargs):
        super(ProfileAdminForm, self).__init__(*args, **kwargs)
        self.fields['meli'] = forms.CharField(required=False, min_length=10, max_length=10)
        self.fields['mobile'] = forms.CharField(required=True, min_length=11, max_length=11)
    class Meta:
        model = UserExam
        fields = ('username','first_name','last_name','meli','address','mobile')
