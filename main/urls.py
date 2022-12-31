from django import contrib
from django.urls import path,re_path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^$',views.Index,name='index'),
    re_path(r'^AgreeAdmin/$',views.AgreeAdmin,name='agree_admin'),
    re_path(r'^Dashboard/$',views.Dashboard,name='dashboard'),
    re_path(r'^DashboardUser/$',views.DashboardUser,name='dashboard_user'),

    re_path(r'^ExamList/$',views.ExamListView,name='exam-list'),
    re_path(r'^ExamCreate/$',views.ExamCreateView,name='exam_create'),
    re_path(r'^ExamDetails/$',views.ExamDetailsView,name='exam-details'),
    re_path(r'^(?P<pk>\d+)/ExamEdit/$',views.ExamEditView,name='exam-edit'),

    re_path(r'^(?P<pk>\d+)/CategoryCreate/$',views.CategoryCreateView,name='category-create'),
    re_path(r'^CategoryList/$',views.CategoryListView,name='category-list'),
    re_path(r'^(?P<pk>\d+)/CategoryEdit/$',views.CategoryEditView,name='category-edit'),
    re_path(r'^(?P<pk>\d+)/CategoryDelete/$',views.CategoryDeleteView,name='category-delete'),

    re_path(r'^(?P<pk>\d+)/(?P<exam_id>\d+)/SubCategoryCreate/$',views.SubCategoryCreateView,name='subcategory-create'),
    re_path(r'^SubCategoryList/$',views.SubCategoryListView,name='subcategory-list'),
    re_path(r'^(?P<pk>\d+)/SubCategoryEdit/$',views.SubCategoryEditView,name='subcategory-edit'),
    re_path(r'^(?P<pk>\d+)/SubCategoryDelete/$',views.SubCategoryDeleteView,name='subcategory-delete'),

    re_path(r'^(?P<pk>\d+)/(?P<exam_id>\d+)/SubsCategoryCreate/$',views.SubsCategoryCreateView,name='subscategory-create'),
    re_path(r'^(?P<pk>\d+)/SubsCategoryEdit/$',views.SubsCategoryEditView,name='subscategory-edit'),
    re_path(r'^(?P<pk>\d+)/SubsCategoryDelete/$',views.SubsCategoryDeleteView,name='subscategory-delete'),
    re_path(r'^SubsCategoryList/$',views.SubsCategoryListView,name='subscategory-list'),

    re_path(r'^(?P<pk>\d+)/QuizCreate/$',views.QuizCreateView,name='quiz-create'),
    re_path(r'^QuizList/$',views.QuizListView,name='quiz-list'),
    re_path(r'^(?P<pk>\d+)/QuizEdit/$',views.QuizEditView,name='quiz-edit'),
    re_path(r'^(?P<pk>\d+)/QuizDelete/$',views.QuizDeleteView,name='quiz-delete'),
    path('ajax/load-subcategorys/', views.load_subcategorys, name='ajax_load_subcategorys'),
    path('ajax/load-subscategorys/', views.load_subscaegorys, name='ajax_load_subscategorys'),

    re_path(r'^QuizListExam/(?P<pk>\d+)/$',views.QuizListExamView,name='quiz-list-exam'),

    re_path(r'^(?P<pk>\d+)/(?P<exam_id>\d+)/QuizCategoryExam/(?P<slug>[\S-]+)/$',views.QuizCategoryExamView,name='quiz_category_exam'),
    re_path(r'^(?P<pk>\d+)/(?P<exam_id>\d+)/QuizubCategoryExam/(?P<slug>[\S-]+)/$',views.QuizSubCategoryExamView,name='quiz_subcategory_exam'),
    re_path(r'^(?P<pk>\d+)/(?P<exam_id>\d+)/QuizSubsCategoryExam/(?P<slug>[\S-]+)/$',views.QuizSubsCategoryExamView,name='quiz_subscategory_exam'),

    re_path(r'^ReviewList/$',views.ReviewListView,name='review_list'),
    re_path(r'^(?P<pk>\d+)/ReviewDelete/$',views.ReviewDeleteView,name='review_delete'),
    
    re_path(r'^UserList/$',views.UserListView,name='user_list'),

    re_path(r'^TemplateCreate/$',views.TemplateCreateView,name='template_create'),
    re_path(r'^TemplateList/$',views.TemplateListView,name='template_list'),
    re_path(r'^TemplateCard/$',views.TemplateCardView,name='template_card'),
    re_path(r'^(?P<pk>\d+)/TemplateDetails/$',views.TemplateDetailsView,name='template_details'),

    re_path(r'^(?P<pk>\d+)/ContactUsCreate/$',views.ContactUsCreateView,name='contactus_create'),
    re_path(r'^(?P<pk>\d+)/ContactUsEdit/$',views.ContactUsEditView,name='contactus_edit'),
    re_path(r'^(?P<pk>\d+)/ContactUs/$',views.ContactUsView,name='contactus'),

    re_path(r'^(?P<pk>\d+)/QuestionCreate/$',views.QuestionCreateView,name='question_create'),
    re_path(r'^(?P<pk>\d+)/QuestionEdit/$',views.QuestionEditView,name='question_edit'),
    re_path(r'^(?P<pk>\d+)/QuestionDelete/$',views.QuestionDeleteView,name='question_delete'),
    re_path(r'^QuestionList/$',views.QuestionListView,name='question_list'),

    re_path(r'^(?P<pk>\d+)/AnswerCreate/$',views.AnswerCreateView,name='answer_create'),
    re_path(r'^(?P<pk>\d+)/AnswerEdit/$',views.AnswerEditView,name='answer_edit'),
    re_path(r'^(?P<pk>\d+)/AnswerDelete/$',views.AnswerDeleteView,name='answer_delete'),
    re_path(r'^AnswerList/$',views.AnswerListView,name='answer_list'),

    re_path(r'^QuizStart/(?P<pk>\d+)/(?P<slug>[\S-]+)/$',views.QuizStartView,name='quiz_start'),
    re_path(r'^WhileQuiz/(?P<pk>\d+)/(?P<exam_id>\d+)/$',views.WhileQuizView,name='quiz_while'),
    re_path(r'^ResultQuiz/(?P<pk>\d+)/(?P<repead_id>\d+)/$',views.ResultQuizView,name='quiz_result'),
    re_path(r'^ResultCheckAnswer/(?P<pk>\d+)/(?P<repead_id>\d+)/$',views.ResultCheckAnswerView,name='check_answer_result'),

    re_path(r'^ResultListUser/$',views.ResultListUserView,name='list_result_user'),
    re_path(r'^ResultDetailsUser/(?P<pk>\d+)/$',views.ResultDetailsUserView,name='details_result_user'),

    re_path(r'^AnswerResultListUser/$',views.AnswerResultListUserView,name='answer_result_user_list'),

    re_path(r'^(?P<pk>\d+)/ImageCreate/$',views.ImageCreateView,name='image_create'),
    re_path(r'^ImageList$',views.ImageListView,name='image_list'),
    re_path(r'^(?P<pk>\d+)/ImageDelete$',views.ImageDeleteView,name='image_delete'),
    re_path(r'^(?P<pk>\d+)/ImageEdit$',views.ImageEditView,name='image_edit'),
]
