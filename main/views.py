from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib import messages 
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F, Func, Value
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import hashlib
from django.contrib import auth
from django.utils import timezone
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.hashers import check_password, make_password
from .models import ImageExam, ChoiceArchive, Choice, Question, Review, Templates, ContactUs, Choice, Answer, Question, Quiz, SubsCategory, SubCategory, Category, Exam, UserExam
from .forms import ImageForm, ChoiceForm, AnswerForm, QuestionForm, QuizForm, ContactUsForm, TemplateForm, ExamForm, ExamEditForm, CategoryForm, SubCategoryForm, SubsCategoryForm
import datetime
from django.http import JsonResponse
import time

def clock():
    while True:
        print(datetime.datetime.now().strftime("%H:%M:%S"), end="\r")
        time.sleep(1)

@never_cache
def Index(request):
    exams = Exam.objects.filter(confirmed = 1).order_by('id')
    return render (request,'user/list-exam.html',{'exams':exams})

@never_cache
def AgreeAdmin(request):
    return render (request,'agree-admin.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def Dashboard(request):
    count_category = Category.objects.filter(user_id = request.user.pk).count()
    count_subcategory = SubCategory.objects.filter(user_id = request.user.pk).count()
    count_subscategory = SubsCategory.objects.filter(user_id = request.user.pk).count()
    count_quiz = Quiz.objects.filter(user_id = request.user.pk).count()
    count_user = UserExam.objects.filter(exam_id = request.user.exam_id,is_user_exam = 1).count()
    return render (request,'dashboard.html',{'count_quiz':count_quiz,'count_user':count_user,'count_category':count_category,'count_subcategory':count_subcategory,'count_subscategory':count_subscategory})

@never_cache
@login_required(login_url='/accounts/LoginUserStore/')
def DashboardUser(request):
    quiz_list = ChoiceArchive.objects.filter(user_id = request.user.id).values_list('quiz_id',flat=True)
    count_review = Quiz.objects.filter(pk__in = quiz_list).count()
    return render (request,'user/screen/dashboard.html',{'count_review':count_review})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ExamListView(request):
    exams = Exam.objects.filter(user_id = request.user.id)
    if exams:
        exam = Exam.objects.get(user_id = request.user.id)
    else:
        return redirect(reverse('exam_create'))
    return render(request, 'screen/ExamListScreen.html',{'exam':exam})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ExamCreateView(request):
    if request.user.is_admin_exam == 1:
        exams = Exam.objects.filter(user_id = request.user.id)
        if exams:
            messages.error(request,'کاربر عزیز شما وبلاگ خود را ایجاد کرده اید.')
            return redirect(reverse('exam-details'))
        else:
            form = ExamForm
            if request.method == 'POST':
                form = ExamForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    exam = Exam.objects.get(user_id = request.user.id)
                    UserExam.objects.filter(pk = request.user.id).update(exam_id = exam.pk)
                    return redirect(reverse('exam-details'))
                else:
                    messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    else:
        return redirect(reverse('login-admin-exam'))
    return render(request, 'screen/ExamCreateScreen.html',{'form':form})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ExamEditView(request, pk): 
    exam = Exam.objects.get(pk = pk)
    context ={'exam':exam} 
    obj = get_object_or_404(Exam, pk = pk) 
    form = ExamEditForm(request.POST or None, request.FILES or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        Exam.objects.filter(pk=pk).update(confirmed = 0)
        return redirect(reverse('exam-list'))
    context["form"] = form 
    return render(request, "screen/ExamEditScreen.html", context) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ExamDetailsView(request):
    exams = Exam.objects.filter(user_id = request.user.id)
    if exams:
        exam = Exam.objects.get(user_id = request.user.id)
        cate = Category.objects.filter(exam_id = exam.pk)
        if not cate:
            categ = 0
        else:
            categ = 1
    else:
        return redirect(reverse('exam_create'))
    return render(request, 'screen/ExamDetailsScreen.html',{'exam':exam,'categ':categ})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def CategoryCreateView(request,pk):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('category-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('category-create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/CategoryCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def CategoryListView(request):
    category = Category.objects.filter(user = request.user.id)
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    context = {'category':category,'subcategory':subcategory}
    return render(request, 'screen/CategoryListScreen.html',context)

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def CategoryDeleteView(request,pk):
    pro = Quiz.objects.filter(category_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = Category.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('category-list'))
    return render(request, 'screen/CategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def CategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(Category, pk = pk) 
    form = CategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('category-list'))
    context["form"] = form 
    return render(request, "screen/CategoryEditScreen.html", context) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubCategoryCreateView(request,pk,exam_id):
    form = SubCategoryForm
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('subcategory-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('subcategory-create', args=[pk,exam_id]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/SubCategoryCreateScreen.html',{'form':form,'pk':pk,'exam_id': exam_id})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubCategoryListView(request):
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/SubCategoryListScreen.html',{'subcategory':subcategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubCategoryDeleteView(request,pk):
    pro = Quiz.objects.filter(subcategory_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = SubCategory.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('subcategory-list'))
    return render(request, 'screen/SubCategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubCategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(SubCategory, pk = pk) 
    form = SubCategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('subcategory-list'))
    context["form"] = form 
    return render(request, "screen/SubCategoryEditScreen.html", context) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubsCategoryCreateView(request,pk,exam_id):
    form = SubsCategoryForm
    if request.method == 'POST':
        form = SubsCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('subscategory-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('subscategory-create', args=[pk,exam_id]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/SubsCategoryCreateScreen.html',{'form':form,'pk':pk,'exam_id': exam_id})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubsCategoryListView(request):
    subscategory = SubsCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/SubsCategoryListScreen.html',{'subscategory':subscategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubsCategoryDeleteView(request,pk):
    pro = Quiz.objects.filter(subscategory_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = SubsCategory.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('subscategory-list'))
    return render(request, 'screen/SubsCategoryListScreen.html',{'delete_cat':delete_cat})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def SubsCategoryEditView(request, pk): 
    context ={} 
    obj = get_object_or_404(SubsCategory, pk = pk) 
    form = SubsCategoryForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('subscategory-list'))
    context["form"] = form 
    return render(request, "screen/SubsCategoryEditScreen.html", context) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuizCreateView(request,pk):
    cat = Category.objects.filter(exam_id = request.user.exam_id)
    form = QuizForm(request=request)
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('quiz-list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('quiz-create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/QuizCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuizListView(request):
    quiz = Quiz.objects.filter(user_id = request.user.id)
    subcategory = SubCategory.objects.filter(user_id = request.user.id)
    return render(request, 'screen/QuizListScreen.html',{'quiz':quiz,'subcategory':subcategory})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuizDeleteView(request,pk):
    pro = Question.objects.filter(quiz_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = Quiz.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('quiz-list'))
    return render(request, 'screen/QuizListScreen.html',{'delete_cat':delete_cat})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuizEditView(request, pk): 
    quiz = Quiz.objects.get(pk = pk)
    context ={'quiz':quiz} 
    form = QuizForm(request=request)
    obj = get_object_or_404(Quiz, pk = pk) 
    form = QuizForm(request.POST or None,request.FILES or None, instance = obj, request=request)     
    if form.is_valid(): 
        form.save() 
        Quiz.objects.filter(pk=pk).update(confirmed = 0)
        return redirect(reverse('quiz-list'))
    context["form"] = form 
    return render(request, "screen/QuizEditScreen.html", context) 

@never_cache
def load_subcategorys(request):
    category_id = request.GET.get('category_id')
    subcategory = SubCategory.objects.filter(category_id=category_id,exam_id = request.user.exam_id).all()
    return render(request, 'subcategory_dropdown_list_options.html', {'subcategory': subcategory})

@never_cache
def load_subscaegorys(request):
    subcategory_id = request.GET.get('subcategory_id')
    subscategory = SubsCategory.objects.filter(subcategory_id=subcategory_id,exam_id = request.user.exam_id).all()
    return render(request, 'subscategory_dropdown_list_options.html', {'subscategory': subscategory})

@never_cache
def QuizListExamView(request,pk):
    search = request.POST.get('search')
    if search:
        quizs = Quiz.objects.filter(exam = pk,name__contains = search,confirmed = 1)
        exam = Exam.objects.get(pk = pk)
        category = Category.objects.filter(exam = pk)
        subcategory = SubCategory.objects.filter(exam = pk)
        subscategory = SubsCategory.objects.filter(exam = pk)
    else:
        quizs = Quiz.objects.filter(exam = pk,confirmed = 1)
        exam = Exam.objects.get(pk = pk)
        category = Category.objects.filter(exam = pk)
        subcategory = SubCategory.objects.filter(exam = pk)
        subscategory = SubsCategory.objects.filter(exam = pk)
    return render(request, 'user/index.html',{'quizs':quizs,'category':category,'exam':exam,'subcategory':subcategory,'subscategory':subscategory})

@never_cache
def QuizStartView(request,pk,slug):
    quizs = Quiz.objects.get(pk = pk)
    question_count = Question.objects.filter(quiz_id = pk).count()
    return render(request, 'user/screen/start-quiz-screen.html',{'quizs':quizs,'question_count':question_count})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ReviewListView(request):
    review_list = Review.objects.filter(exam_id=request.user.exam_id)
    return render(request, 'screen/ReviewListScreen.html',{'review_list':review_list})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ReviewDeleteView(request,pk):
    review_delete = Review.objects.filter(pk=pk).delete()
    if review_delete:
        return redirect(reverse('review_list'))
    return render(request, 'screen/ReviewListScreen.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def TemplateCreateView(request):
    form = TemplateForm
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('template_list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('template_create'))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'admin/TemplateCreateScreen.html',{'form':form})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def TemplateListView(request):
    template = Templates.objects.all()
    return render(request, 'admin/TemplateListScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def TemplateCardView(request):
    template = Templates.objects.all()
    return render(request, 'screen/TemplateCardScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def TemplateDetailsView(request,pk):
    template = Templates.objects.get(pk=pk)
    template_pk = request.POST.get('template')
    if template_pk:
        Exam.objects.filter(pk = request.user.exam_id).update(templates_id = template_pk)
        return redirect(reverse('template_card'))
    return render(request, 'screen/TemplateDetailsScreen.html',{'template':template})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ContactUsCreateView(request,pk):
    contactus = ContactUs.objects.filter(exam_id = pk)
    if contactus:
        return redirect(reverse('contactus_edit', args=[pk]))
    else:
        form = ContactUsForm
        if request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('dashboard'))
            else:
                messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/ContactUsCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def ContactUsEditView(request, pk): 
    exam = Exam.objects.get(pk = pk)
    context ={'exam':exam} 
    obj = get_object_or_404(ContactUs, exam_id = pk) 
    form = ContactUsForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('dashboard'))
    context["form"] = form 
    return render(request, "screen/ContactUsEditScreen.html", context) 

@never_cache
def ContactUsView(request,pk):
    contactus_fil = ContactUs.objects.filter(exam_id = pk)
    if contactus_fil:
        contactus = ContactUs.objects.get(exam_id = pk)
        exam = Exam.objects.get(pk = pk)
    else:
        return redirect(reverse('quiz-list-exam', args=[pk]))
    return render(request, 'user/screen/ContactUsScreen.html',{'contactus':contactus,'exam':exam})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def UserListView(request):
    user_list = UserExam.objects.filter(exam_id=request.user.exam_id,is_user_exam = 1)
    return render(request, 'screen/UserListScreen.html',{'user_list':user_list})

@never_cache
@csrf_exempt
def QuizCategoryExamView(request,pk,exam_id,slug):
    list_quiz_category = Quiz.objects.filter(category_id = pk,confirmed = 1)
    fill_quiz_category = Quiz.objects.filter(category_id = pk,confirmed = 1).last()
    if fill_quiz_category:
        exam = Exam.objects.get(pk = fill_quiz_category.exam_id)
    else:
        return redirect(reverse('quiz-list-exam', args=[exam_id]))
    return render(request, 'user/screen/card-category.html',{'list_quiz_category':list_quiz_category,'exam':exam})

@never_cache
@csrf_exempt
def QuizSubCategoryExamView(request,pk,exam_id,slug):
    list_quiz_category = Quiz.objects.filter(subcategory_id = pk,confirmed = 1)
    fill_quiz_category = Quiz.objects.filter(subcategory_id = pk,confirmed = 1).last()
    if fill_quiz_category:
        exam = Exam.objects.get(pk = fill_quiz_category.exam_id)
    else:
        return redirect(reverse('quiz-list-exam', args=[exam_id]))
    return render(request, 'user/screen/card-category.html',{'list_quiz_category':list_quiz_category,'exam':exam})

@never_cache
@csrf_exempt
def QuizSubsCategoryExamView(request,pk,exam_id,slug):
    list_quiz_category = Quiz.objects.filter(subscategory_id = pk,confirmed = 1)
    fill_quiz_category = Quiz.objects.filter(subscategory_id = pk,confirmed = 1).last()
    if fill_quiz_category:
        exam = Exam.objects.get(pk = fill_quiz_category.exam_id)
    else:
        return redirect(reverse('quiz-list-exam', args=[exam_id]))
    return render(request, 'user/screen/card-category.html',{'list_quiz_category':list_quiz_category,'exam':exam})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuestionCreateView(request,pk):
    form = QuestionForm
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('question_list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('question_create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/QuestionCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuestionListView(request):
    question = Question.objects.filter(user_id = request.user.id)
    return render(request, 'screen/QuestionListScreen.html',{'question':question})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuestionEditView(request, pk): 
    form = QuestionForm
    obj = get_object_or_404(Question, pk = pk) 
    form = QuestionForm(request.POST or None, instance = obj)     
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('question_list'))
    return render(request, "screen/QuestionEditScreen.html", {'form':form}) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def QuestionDeleteView(request,pk):
    pro = Answer.objects.filter(question_id = pk)
    if pro:
        delete_cat = 1
    else:
        delete_cat = 0
        delete = Question.objects.filter(pk=pk).delete()
        if delete:
            return redirect(reverse('question_list'))
    return render(request, 'screen/QuestionListScreen.html',{'delete_cat':delete_cat})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def AnswerCreateView(request,pk):
    answer = Answer.objects.filter(question_id = pk,correct_question = 1)
    form = AnswerForm
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            correct_question = form.cleaned_data['correct_question']
            if answer and correct_question == True:
                messages.error(request,'شما در یکی از گزینه ها، جواب را انتخاب کرده اید، اگر میخواهید تغییر دهید، به لیست جوابها بروید و اصلاح کنید.')
            else:
                form.save()
                if 'Save_list' in request.POST:
                    return redirect(reverse('answer_list'))
                elif 'Save_and_add' in request.POST:
                    return redirect(reverse('answer_create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/AnswerCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def AnswerListView(request):
    answer = Answer.objects.filter(user_id = request.user.id)
    return render(request, 'screen/AnswerListScreen.html',{'answer':answer})

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def AnswerEditView(request, pk):
    ques = Answer.objects.get(pk = pk)
    answer = Answer.objects.filter(question_id = ques.question_id,correct_questuion = 1).count() 
    form = AnswerForm
    obj = get_object_or_404(Answer, pk = pk) 
    form = AnswerForm(request.POST or None, instance = obj)     
    if form.is_valid(): 
        correct_questuion = form.cleaned_data['correct_questuion']
        if answer > 0 and correct_questuion == True:
            messages.error(request,'شما در یکی از گزینه ها، جواب را انتخاب کرده اید، اگر میخواهید تغییر دهید، به لیست جوابها بروید و اصلاح کنید.')
        else:
            form.save() 
            return redirect(reverse('answer_list'))
    return render(request, "screen/AnswerEditScreen.html", {'form':form}) 

@never_cache
@login_required(login_url='/accounts/LoginAdminExam/')
def AnswerDeleteView(request,pk):
    delete = Answer.objects.filter(pk=pk).delete()
    if delete:
        return redirect(reverse('answer_list'))
    return render(request, 'screen/AnswerListScreen.html')

@never_cache
@csrf_exempt
def WhileQuizView(request,pk,exam_id):
    nxt = request.GET.get("next", None)
    if nxt:
        return redirect(nxt)    
    if request.user.id and request.user.is_user_exam == 1:
        choice_fill = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('question_id',flat=True)
        question = Question.objects.filter(quiz_id = pk).exclude(pk__in = choice_fill)[:1]
        question_count_limit = Question.objects.filter(quiz_id = pk).exclude(pk__in = choice_fill).count()
        if question_count_limit < 1:
            pk_delete = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('pk',flat=True)
            quiz = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('quiz',flat=True)
            question = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('question',flat=True)
            answer = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('answer',flat=True)
            datecreate = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('datecreate',flat=True)
            datecreatealt = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('datecreatealt',flat=True)
            timespent_s = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('timespent_s',flat=True)
            timespent_m = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('timespent_m',flat=True)
            timespent_h = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('timespent_h',flat=True)
            user_id = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('user',flat=True)
            repeads = ChoiceArchive.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('repeat_quiz', flat=True).last()
            if not repeads:
                repeads = 1
            else:
                repeads += 1
            if quiz:
                for q,ques,a,dc,dca,ts,tm,th,u in zip(quiz,question,answer,datecreate,datecreatealt,timespent_s,timespent_m,timespent_h,user_id):
                    ChoiceArchive.objects.create(repeat_quiz = repeads,quiz_id = q,question_id = ques,answer_id = a,datecreate=dc,datecreatealt = dca,timespent_m = tm,timespent_s = ts,timespent_h = th,user_id = u)
                    for d in pk_delete:
                        Choice.objects.filter(pk = d).delete()
            return redirect(reverse('quiz_result', args=[pk,repeads]))
        question_count = Choice.objects.filter(quiz_id = pk,user_id = request.user.id).count()
        if question_count == 0:
            question_count = 1
        else:
            question_count += 1
        question_count_all = Question.objects.filter(quiz_id = pk).count()
        choice_ques = Choice.objects.filter(quiz_id = pk).values_list('question_id', flat=True)
        question_set = Question.objects.filter(quiz_id = pk).exclude(pk__in = choice_ques).values_list('pk',flat=True)[:1]
        answer = Answer.objects.filter(question_id = question_set)
        quiz = request.POST.get('quiz')
        questions = request.POST.get('question')
        datecreate = request.POST.get('datecreate', None)
        datecreatealt = request.POST.get('datecreatealt')
        timespent_s = request.POST.get('timespent_s')
        timespent_m = request.POST.get('timespent_m')
        timespent_h = request.POST.get('timespent_h')
        user = request.user.id
        answers = request.POST.get('answer')
        form = ChoiceForm
        if request.method == 'POST':
            if answers:
                form = ChoiceForm(request.POST)
                Choice.objects.create(quiz_id = quiz,question_id = questions,datecreate = datecreate,datecreatealt = datecreatealt,user_id = user,answer_id = answers,timespent_s = timespent_s,timespent_m = timespent_m,timespent_h = timespent_h)
                return redirect(reverse('quiz_while', args=[pk,exam_id]))
            else:
                messages.error(request,'جواب سوال را انتخاب کنید.')
    else:
        auth.logout(request)
        return redirect(reverse('login-user-exam', args=[exam_id]))
    return render(request, 'user/screen/while-quiz-screen.html',{'question':question,'answer':answer,'form': form,'question_count': question_count,'question_count_all': question_count_all})

@never_cache
@login_required(login_url='/accounts/LoginUserExam/')
def ResultQuizView(request,pk,repead_id):
    quiz = Quiz.objects.get(pk = pk)
    answer = Answer.objects.filter(question__quiz_id = pk,correct_question = 1).values_list('pk',flat=True)
    answer_correct_count = ChoiceArchive.objects.filter(answer_id__in = answer,repeat_quiz = repead_id,user_id = request.user.id).values_list('answer_id',flat=True).count()
    questions = ChoiceArchive.objects.filter(quiz_id = pk,repeat_quiz = repead_id,user_id = request.user.id).values_list('question_id',flat=True)
    answers = ChoiceArchive.objects.filter(quiz_id = pk,repeat_quiz = repead_id,user_id = request.user.id).values_list('answer_id',flat=True)
    correct_questions = Answer.objects.filter(pk__in = answers).values_list('correct_question',flat=True)
    count_question = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).count()
    percent_correct = answer_correct_count / count_question * 100
    sum_time_s = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_s=Sum('timespent_s'))
    sum_time_m = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_m=Sum('timespent_m'))
    sum_time_h = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_h=Sum('timespent_h'))
    return render(request, 'user/screen/result-quiz-screen.html',{'repead_id':repead_id,'percent_correct':percent_correct,'answer_correct_count':answer_correct_count,'count_question':count_question,'quiz':quiz,'sum_time_s':sum_time_s,'sum_time_m':sum_time_m,'sum_time_h':sum_time_h})

@never_cache
def ResultCheckAnswerView(request,pk,repead_id):
    quiz = Quiz.objects.get(pk = pk)
    answer = Answer.objects.filter(question__quiz_id = pk,correct_question = 1).values_list('pk',flat=True)
    answer_correct_count = ChoiceArchive.objects.filter(answer_id__in = answer,repeat_quiz = repead_id,user_id = request.user.id).values_list('answer_id',flat=True).count()
    questions = ChoiceArchive.objects.filter(quiz_id = pk,repeat_quiz = repead_id,user_id = request.user.id).values_list('question_id',flat=True)
    answers = Question.objects.filter(quiz_id = pk).all()
    correct_questions = Answer.objects.filter(pk__in = answers).values_list('correct_question',flat=True)
    count_question = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).count()
    percent_correct = answer_correct_count / count_question * 100
    repead_id_list = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).all()
    sum_time_s = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_s=Sum('timespent_s'))
    sum_time_m = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_m=Sum('timespent_m'))
    sum_time_h = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id,repeat_quiz = repead_id).aggregate(time_h=Sum('timespent_h'))
    return render(request, 'user/screen/result-check-answer-screen.html',{'repead_id_list':repead_id_list,'answers':answers,'percent_correct':percent_correct,'answer_correct_count':answer_correct_count,'count_question':count_question,'quiz':quiz,'sum_time_s':sum_time_s,'sum_time_m':sum_time_m,'sum_time_h':sum_time_h})

@never_cache
@login_required(login_url='/accounts/LoginUserExam/')
def ResultListUserView(request):
    list_quizs = ChoiceArchive.objects.filter(user_id = request.user.id).values_list('quiz_id', flat=True)
    list_quiz = Quiz.objects.filter(pk__in = list_quizs).all()
    sum_time_s = ChoiceArchive.objects.filter(user_id = request.user.id).values('user_id').aggregate(time_s=Sum('timespent_s'))
    sum_time_m = ChoiceArchive.objects.filter(user_id = request.user.id).values('user_id').aggregate(time_m=Sum('timespent_m'))
    sum_time_h = ChoiceArchive.objects.filter(user_id = request.user.id).values('user_id').aggregate(time_h=Sum('timespent_h'))
    return render(request, 'user/screen/list-result-screen.html',{'list_quiz':list_quiz,'sum_time_s':sum_time_s,'sum_time_m':sum_time_m,'sum_time_h':sum_time_h})

@never_cache
@login_required(login_url='/accounts/LoginUserExam/')
def ResultDetailsUserView(request,pk):
    choice_details = ChoiceArchive.objects.filter(quiz_id = pk,user_id = request.user.id).all()
    quiz = Quiz.objects.get(pk = pk)
    answer = Answer.objects.filter(question__quiz_id = pk,correct_question = 1).values_list('pk',flat=True)
    fill_repeat_quiz = ChoiceArchive.objects.filter(answer_id__in = answer,user_id = request.user.id).values_list('repeat_quiz',flat=True)
    for a in fill_repeat_quiz:
         answer_correct_count_repead = ChoiceArchive.objects.filter(answer_id__in = answer,user_id = request.user.id,repeat_quiz = a).values_list('answer_id',flat=True).count()
    else:
        answer_correct_count_repead = 0
    answer_correct_count = ChoiceArchive.objects.filter(answer_id__in = answer,user_id = request.user.id).values_list('answer_id',flat=True).count()
    questions = ChoiceArchive.objects.filter(quiz_id = pk,user_id = request.user.id).values_list('question_id',flat=True)
    answers = Question.objects.filter(quiz_id = pk).all()
    correct_questions = Answer.objects.filter(pk__in = answers).values_list('correct_question',flat=True)
    count_question = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id).count()
    percent_correct = answer_correct_count / count_question * 100
    repead_id_list = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id).all()
    sum_time_s = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id).aggregate(time_s=Sum('timespent_s'))
    sum_time_m = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id).aggregate(time_m=Sum('timespent_m'))
    sum_time_h = ChoiceArchive.objects.filter(quiz_id=pk,user_id = request.user.id).aggregate(time_h=Sum('timespent_h'))
    return render(request, 'user/screen/details-result-screen.html',{'answer_correct_count_repead':answer_correct_count_repead,'repead_id_list':repead_id_list,'answers':answers,'percent_correct':percent_correct,'answer_correct_count':answer_correct_count,'count_question':count_question,'quiz':quiz,'sum_time_s':sum_time_s,'sum_time_m':sum_time_m,'sum_time_h':sum_time_h,'choice_details':choice_details})

@never_cache
@login_required(login_url='/accounts/LoginUserExam/')
def AnswerResultListUserView(request):
    return render(request, 'screen/answer-list-result-screen.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageCreateView(request,pk):
    form = ImageForm
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'Save_list' in request.POST:
                return redirect(reverse('image_list'))
            elif 'Save_and_add' in request.POST:
                return redirect(reverse('image_create', args=[pk]))
        else:
            messages.error(request,'اطلاعات مورد نظر را کامل کنید.')
    return render(request, 'screen/ImageCreateScreen.html',{'form':form,'pk':pk})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageListView(request):
    images = ImageExam.objects.filter(user_id = request.user.id)
    return render(request, 'screen/ImageListScreen.html',{'images':images})

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageDeleteView(request,pk):
    delete = ImageExam.objects.filter(pk=pk).delete()
    if delete:
        return redirect(reverse('image_list'))
    return render(request, 'screen/ImageListScreen.html')

@never_cache
@login_required(login_url='/accounts/LoginAdminStore/')
def ImageEditView(request, pk): 
    image = ImageExam.objects.get(pk = pk)
    context ={'image':image} 
    form = ImageForm
    obj = get_object_or_404(ImageExam, pk = pk) 
    form = ImageForm(request.POST or None,request.FILES or None, instance = obj)     
    if form.is_valid(): 
        form.save() 
        return redirect(reverse('image_list'))
    context["form"] = form 
    return render(request, "screen/ImageEditScreen.html", context) 