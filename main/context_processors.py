import exam
from main.models import Exam


def AllExams(request):
    from .models import UserExam
    if request.user.id and request.user.is_user_exam == 1:
       exam = Exam.objects.get(pk = request.user.exam_id)
    else:
        exam = 0
    return {'exam':exam}
