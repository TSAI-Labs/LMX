from django.shortcuts import render
from django.http import HttpResponse
from lms.models.quiz_student_model import Quiz_Questions
from lms.models.quiz_student_model import session
from lms.models.quiz_student_model import QuizDetails
from lms.models.quiz_student_model import studentdetails
from lms.models.quiz_student_model import studentquizdetails
from lms.models.quiz_student_model import Quiz_Questions
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import json 




anslist = []
# for i in answers:
#     anslist.append(i.answer)



def index(request):
    print("request...",request,request.GET['session'])
    if request.GET['session'] is not None:
        session_name = str(request.GET['session'])
    return render(request, 'quiz/quiz_student/landingPage.html', {'sessionName': session_name})

def quiz(request):
    #obj = Quiz_Questions.objects.all()
    #count = Quiz_Questions.objects.all().count()
    session_name = ''
    if request.GET['sessName'] is not None:
        session_name = str(request.GET['sessName'])
        print("in quiz page...",session_name)
    
    obj=None
    count=0
    questions = []
    questions = getQUizQuestionAnswers(session_name)
    count = len(questions)
    return render(request,'quiz/quiz_student/index.html',{'obj':obj,'questions':questions,'count':count})


def GetSessionDetails(request):
    context = {
        'session':session
    }
    print("prin1")

    context = session.objects.all()
    print("context details....",context)

    
    #return render(request,'sessionpage.html',context)
    return render(request,'quiz/quiz_student/QuizAll.html',{'context':context})



def getQUizQuestionAnswers(session_name):
    print("in get ques",session_name)
    session_details = session.objects.all()
    #session_name=None
    sessionId=None
    quizId = None
    student_quiz_answers = None
    quiz_question_answers = []
    quiestions_list_final = []
    studentquizdetailslist = []

    for item in session_details:
        
        if(str(item.name) == str(session_name)):
            sessionId = item.sessionid
            break
    
    if(sessionId is not None):
        quizdetailslist = QuizDetails.objects.all()
        for item_quiz in quizdetailslist:
            
            if(item_quiz.sessionid.sessionid==sessionId):
                quizId = item_quiz.quizid
                break


    if(quizId is not None):
        studentquizdetailslist = studentquizdetails.objects.all()
        for studentquizdetails_quiz in studentquizdetailslist:

            if(studentquizdetails_quiz.quizid.quizid==quizId):
                student_quiz_answers = studentquizdetails_quiz.quiz_answers
                break

    if(quizId is not None):
        Quiz_Questionslist = Quiz_Questions.objects.all()

        for item_Quiz_Questions in Quiz_Questionslist:
            if(item_Quiz_Questions.quizid.quizid==quizId):
                #print(item_Quiz_Questions.quiz_question_answers)
                quiz_question_answers.append(item_Quiz_Questions.quiz_question_answers)

    

    print(student_quiz_answers)
    print(quiz_question_answers)

    
    # for item in quiz_question_answers:
    #     for student_item_key in student_quiz_answers.keys():
    #         if (student_item_key in item.keys()):
    #             json_obj = {"Question":student_item_key}
    #             for ans_option,ans_value in item[student_item_key].items():
    #                 json_obj[ans_option] = ans_value
    #             quiestions_list_final.append(json_obj)

    count = 0
    if(student_quiz_answers is not None):    
        count = len(student_quiz_answers)
        
    for item in quiz_question_answers:
        if(count > 0):
            for student_item_key,value in student_quiz_answers.items():
                if (student_item_key in item.keys()):
                    json_obj = {"Question":student_item_key,"user_answer":value}
                    for ans_option,ans_value in item[student_item_key].items():
                        json_obj[ans_option] = ans_value
                    quiestions_list_final.append(json_obj)
        else:
            for ans_option,ans_value in item.items():
                json_obj = {"Question":str(ans_option)}
                for option,answer in ans_value.items():
                    json_obj[option]= answer
                quiestions_list_final.append(json_obj)



    print(quiestions_list_final)

    return quiestions_list_final

# def user_search_from_group(request):
#     print("POST call....")
#     if request.method == 'POST':
#         print(dir(request))
#         print(dir(request.POST))
#         print(request.POST.values)
#         #username3 = request.POST.get('username3')
#         #gname = request.POST.get('groupname')
#         print("post cal====================")
#         print(request.POST.get('myform1'))
#     return render(request, 'landingPage.html', {})



# def quiz(request):
#     #quiz = get_object_or_404(Quiz, quiz_id)
#     questions = getQUizQuestionAnswers()
#     form = QuizForm(questions=questions)
#     # if request.method == "POST":
#     #     form = QuizForm(request.POST, questions=quiz.question_set.all())
#     #     if form.is_valid(): ## Will only ensure the option exists, not correctness.
#     #         attempt = form.save()
#     #         return redirect(attempt)
#     #return render_to_response('quiz.html', {"form": form})
#     print("form is...",form)
#     return render(request,'index.html',{"form": form})

@csrf_protect
def SaveQuizAnswers(request):
    #csrfContext = RequestContext(request)
    #print("POST call....",csrfContext,request.POST['answers'])
    if request.method == 'POST':
        print("post call happned...",type(request.POST['answers']))
        answers = json.loads(request.POST['answers'])
        print(type(answers),answers)
        new_model = studentquizdetails()
        new_model.quizid = QuizDetails.objects.get(quizid="Quiz2")
        new_model.studentid = studentdetails.objects.get(studentid = 10002)
        new_model.quiz_status = True
        new_model.quiz_answers = answers
        #print("new model..",new_model)
        new_model.save()

    return render(request,'index.html',{})