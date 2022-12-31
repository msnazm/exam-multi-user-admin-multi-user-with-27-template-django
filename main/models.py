from django.db import models
from django.db.models.deletion import SET_NULL
from ckeditor.fields import RichTextField
from django.db.models.fields import CharField
from django.http import request
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F
from exam import settings

class UserExam(AbstractUser):
    exam_id = models.IntegerField(null=True, blank=True)
    is_user_exam = models.BooleanField(default=False)
    is_admin_exam = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    meli = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    agree = models.BooleanField(null=True, blank=True)

class Templates(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='image/',blank=True)

class Exam(models.Model):
    name = models.CharField(max_length=255)
    templates = models.ForeignKey(Templates,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField(max_length=255,allow_unicode=True,default=0)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    descreption = models.TextField()
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    confirmed = models.IntegerField(default=0,null=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Exam, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    category = models.ForeignKey(Category,related_name='sub',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubsCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    subcategory = models.ForeignKey(SubCategory,related_name='subs',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubsCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class ContactUs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    descreption = RichTextField()

    def __str__(self):
        return str(self.descreption)

class Quiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    subscategory = models.ForeignKey(SubsCategory,on_delete=models.SET_NULL,null=True,blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    descreption = RichTextField()
    slug = models.SlugField(max_length=255,allow_unicode=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    confirmed = models.IntegerField(default=0,null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Quiz, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
 
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("quiz_start", kwargs={"pk": self.pk,"slug": self.slug})   

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.SET_NULL,null=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    descreption = RichTextField()

    def __str__(self):
        return self.descreption
 
class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    question = models.ForeignKey(Question,related_name='answer_related',on_delete=models.SET_NULL,null=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    descreption = RichTextField()
    correct_question = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.descreption

class Choice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    question = models.ForeignKey(Question,on_delete=models.SET_NULL,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.SET_NULL,null=True)
    answer = models.ForeignKey(Answer,on_delete=models.SET_NULL,null=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    timespent_s = models.IntegerField()
    timespent_m = models.IntegerField()
    timespent_h = models.IntegerField()

    def __str__(self):
        return self.user

class ChoiceArchive(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    question = models.ForeignKey(Question,related_name='choice_related',on_delete=models.SET_NULL,null=True)
    quiz = models.ForeignKey(Quiz,on_delete=models.SET_NULL,null=True)
    answer = models.ForeignKey(Answer,on_delete=models.SET_NULL,null=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    timespent_s = models.IntegerField()
    timespent_m = models.IntegerField()
    timespent_h = models.IntegerField()
    repeat_quiz = models.IntegerField()

    def __str__(self):
        return self.user

class Review(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    comment = models.TextField(null=True, blank=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    confirmed = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return str(self.rating)

class ImageExam(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    name = models.CharField(max_length=255)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name