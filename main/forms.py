from django.db import models
from django import forms
from django.db.models import fields
from .models import ImageExam, Choice, Answer, Question, Quiz, Exam, Category, SubCategory, SubsCategory, Templates, ContactUs
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages 
from ckeditor.widgets import CKEditorWidget

class ExamForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    descreption = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'class': 'form-control'}))

    class Meta:
        model = Exam
        fields = ['id','name','slug','image','descreption','datecreate','datecreatealt','user']

class ExamEditForm(forms.ModelForm):
    descreption = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'class': 'form-control'}))

    class Meta:
        model = Exam
        fields = ['id','image','descreption']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = '__all__'

class SubCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubCategory
        fields = '__all__'

class SubsCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubsCategory
        fields = '__all__'

class QuizForm(forms.ModelForm):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    descreption = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField(required=True, content_types=['image/png', 'image/jpeg'],max_upload_size=1)
        raise ValidationError('msn')
    def __init__(self, *args, **kwargs):
        super(QuizForm,self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.subcategory.subcategory_set.order_by('name')
    def __init__(self, *args, **kwargs):
        super(QuizForm,self).__init__(*args, **kwargs)
        self.fields['subscategory'].queryset = SubsCategory.objects.none()
        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['subscategory'].queryset = SubsCategory.objects.filter(subcategory_id=subcategory_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subscategory'].queryset = self.instance.subscategory.subscategory_set.order_by('name')
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(QuizForm,self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(exam_id = self.request.user.exam_id)
        self.fields['subcategory'].queryset = SubCategory.objects.filter(exam_id = self.request.user.exam_id)
        self.fields['subscategory'].queryset = SubsCategory.objects.filter(exam_id = self.request.user.exam_id)
        self.fields['category'].empty_label = 'دسته اصلی را انتخاب کنید'
    class Meta:
        model = Quiz
        fields = '__all__'

class TemplateForm(forms.ModelForm):

    class Meta:
        model = Templates
        fields = '__all__'

class ContactUsForm(forms.ModelForm):
    descreption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ContactUs
        fields = '__all__'

class QuestionForm(forms.ModelForm):
    descreption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = '__all__'

class AnswerForm(forms.ModelForm):
    descreption = forms.CharField(widget=CKEditorWidget())
    correct_question = forms.BooleanField(required=False)

    class Meta:
        model = Answer
        fields = '__all__'

class ChoiceForm(forms.ModelForm):
    descreption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Choice
        fields = '__all__'

class ImageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    image = forms.ImageField(required=True)
    
    class Meta:
        model = ImageExam
        fields = '__all__'
