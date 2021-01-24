# Core Django imports.
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from lms.models.user_role_model import Role


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages



from django.core.mail import send_mail
from django.http import HttpResponse
from lms.token import account_activation_token

# from lms.models.enrollment_model import Group, Enrollment
from lms.models.course_model import StudentCourse

# Blog application imports.
from lms.models.course_model import Course, Group


#EMail imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# LMS app imports
from lms.forms.course.group_creation_request_form import GroupCreationRequestForm
from lms.forms.course.mail_to_admin_form import MailToAdminForm



class GroupCreationRequestView(LoginRequiredMixin, View):
    """
    Group Creation Request To another Student
    Implementation : This view is for the student who creates groups and request memebers to join the group. 
    The person who created the group is like the admin, he can only request members to join. 
    He should atleast request 1 member to join the group at the time of group creation and later he can request more.
    

    #TODO : Add the max limit of members for group creation
    """
    template_name = 'lms/course/group_creation_request.html'

    home_template = 'dashboard/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        role = Role.objects.filter(user=request.user)
        if role and role[0].is_student:
        
            pk = self.kwargs['pk']
     
            self.context_object = {"group_creation_form": GroupCreationRequestForm(user_id = request.user.id, pk = pk),'pk' : pk}

            return render(request, self.template_name, self.context_object)
        
        else:
            messages.error(request, "Only Student can view this!!")
            return redirect('lms:logout')

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user_id = request.user.id
        request_form = GroupCreationRequestForm(data=request.POST, user_id = user_id, pk = pk)
        
        if request_form.is_valid():
            current_site = get_current_site(request)
            student_emails =  request_form.cleaned_data['student_email']
            group_name = request_form.cleaned_data['name']
            try : 
                is_group_exists = Group.objects.get(name = group_name )
            except :
                is_group_exists = None
            try :
                course_enrolled = StudentCourse.objects.get(courses_id =pk, user_id = user_id)
                
            except : 
                print("error")
                course_enrolled = None

            if(not(is_group_exists) and course_enrolled and not(course_enrolled.group) ):
                group = Group(group_name = group_name, course = Course.objects.get(id = pk), user = request.user )
                group.save()
                course_enrolled.group = group
                course_enrolled.save()
            
            elif(is_group_exists and course_enrolled and course_enrolled.group == 'group_name'):
                pass


            else : 
                print("Either you are already in a group nor the group name already exists")
                


            for item in student_emails : 
                mail, username = item.split(',')
                user = User.objects.get(username = username)
                message = render_to_string('lms/course/group_creation_request_email.html',
                {
                    'user':user ,
                    'course_id' : kwargs['pk'],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(str(user.pk)+"+"+group_name)),
                    'token': account_activation_token.make_token(user),
                    'from_user' : request.user
                })
            
                subject = "Request to create Group"
                res = send_mail(subject=subject, message=message, from_email= request.user.email,recipient_list= [mail] )
            
            return render(request,self.home_template)

            

class GroupCreationRequestSentView(LoginRequiredMixin, View):

    """
    View for the students who recives the email invitation to join the group.
    After the user clicks the link, he is checked whether he is already part of a group or he is added to the group.
    """

    def get(self, request, ck, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        role = Role.objects.filter(user=request.user)
        if role and role[0].is_student:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                
                print(uid)
                pk = int(uid.split("+")[0])

                group_name = uid.split("+")[-1]
                print(pk, group_name, request.user.id)
    
                user = User.objects.get(pk=pk)
                
                    
            except (TypeError, ValueError, OverflowError):
                user = None
                print(TypeError, ValueError, OverflowError)
            
            
            if user is not None and group_name is not None and account_activation_token.check_token(user,token):
            
                if( request.user == user):
                    
                    
                    try :

                        course_enrolled = StudentCourse.objects.get(courses_id =ck, user = user)
                        print(course_enrolled)
                        group = Group.objects.get(group_name = group_name)
                        print(course_enrolled.group, group)
                        
                    except : 
                       
                        course_enrolled = None
                        messages.error(request, f"You are not enrolled in any course or Group doesn't exist"
                                )
                    if(course_enrolled  and  not(course_enrolled.group)):
                        course_enrolled.group = group
                        course_enrolled.save()
                        print("enrolled successfully!")

                    
                        messages.success(request, f"Congratulations {user.username} !!! "
                                        f"Now you are part of {group_name}"
                                )
                    else :
                        messages.error(request, f"You may be already in a group. Check out!!! "
                                        
                                )

                else : 

                    messages.error(request, f"You are not the one whom the request is sent to or you may be already existed in some group"
                                )

           

            

            

                return redirect('lms:dashboard_home')
            else:
                messages.error(request, f"This link is not for you!!!"
                                )
        else: 
            messages.error(request, f"Only Students can Login to this!!!"
                                )
            return redirect('lms:logout')

class ViewGroupsView(LoginRequiredMixin, View):

    """
    To View All the groups.All the authenticated users can see the groups formed despite of teacher or student
    """
    
    def get(self, request, *args, **kwargs):
         course_id = kwargs['pk']
         groups_student_dict = {}
         groups = Group.objects.filter(course_id =course_id) 
         for group in groups:
            students = [student.user.username for student in StudentCourse.objects.filter(group = group)]
            groups_student_dict[group.group_name] = students

         self.context_object = {"groups": groups_student_dict}

         return render(request, 'lms/course/view_groups.html', self.context_object ) 