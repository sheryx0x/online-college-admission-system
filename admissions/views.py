from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,  ApplicationStatusForm,AdminSignupForm, ProfileForm,MeritListForm,AnnouncementForm,FAApplicationForm,FSCApplicationForm,BSApplicationForm
from .models import  Profile,MeritList,Program,Announcement,FAApplication, FSCApplication, BSApplication,AdmissionStatus
from asgiref.sync import async_to_sync
from .email_utils import send_announcement_email
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from itertools import chain
from django.db.models import F, ExpressionWrapper, FloatField
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import os


def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('admin_dashboard')  
    else:
        form = AdminSignupForm()
    return render(request, 'admissions/admin_signup.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        form = AuthenticationForm()
    return render(request, 'admissions/admin_login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def landingpage(request):
    return render (request, 'admissions/landingpage.html')



def home(request):
    programs = Program.objects.all()
    context = {'programs': programs}
    return render(request, 'admissions/home.html', context)

def signup(request):
    form = SignUpForm(request.POST or None) 
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('complete_profile')
    return render(request, 'admissions/signup.html', {'form': form})



def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)  
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            
            pass
    return render(request, 'admissions/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def is_admission_open():
    status = AdmissionStatus.objects.first()  
    return status.is_open if status else False  

@login_required
def fa_apply(request):
    if not is_admission_open():
        messages.error(request, "Admissions are currently closed. Please check back later.")
        return redirect('home')

    
    profile = request.user.profile
    if not profile.father_name or not profile.date_of_birth or not profile.address or not profile.phone_number:
        messages.error(request, "Please complete your profile before applying for a program.")
        return redirect('complete_profile')

    if request.method == 'POST':
        form = FAApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            fa_application = form.save(commit=False)
            fa_application.user = request.user
            fa_application.status = 'submitted'
            fa_application.save()
            return redirect('application_status')
    else:
        form = FAApplicationForm()

    context = {'form': form, 'profile': profile}
    return render(request, 'admissions/fa_apply.html', context)

@login_required
def fsc_apply(request):
    if not is_admission_open():
        messages.error(request, "Admissions are currently closed. Please check back later.")
        return redirect('home')

    profile = request.user.profile
    if not profile.father_name or not profile.date_of_birth or not profile.address or not profile.phone_number:
        messages.error(request, "Please complete your profile before applying for a program.")
        return redirect('complete_profile')

    if request.method == 'POST':
        form = FSCApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            fsc_application = form.save(commit=False)
            fsc_application.user = request.user
            fsc_application.status = 'submitted'
            fsc_application.save()
            return redirect('application_status')
    else:
        form = FSCApplicationForm()

    context = {'form': form, 'profile': profile}
    return render(request, 'admissions/fsc_apply.html', context)

@login_required
def bs_apply(request):
    if not is_admission_open():
        messages.error(request, "Admissions are currently closed. Please check back later.")
        return redirect('home')

    profile = request.user.profile
    if not profile.father_name or not profile.date_of_birth or not profile.address or not profile.phone_number:
        messages.error(request, "Please complete your profile before applying for a program.")
        return redirect('complete_profile')

    if request.method == 'POST':
        form = BSApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            bs_application = form.save(commit=False)
            bs_application.user = request.user
            bs_application.status = 'submitted'
            bs_application.save()
            return redirect('application_status')
    else:
        form = BSApplicationForm()

    context = {'form': form, 'profile': profile}
    return render(request, 'admissions/bs_apply.html', context)


@login_required
def application_status(request):
    user = request.user

    
    program = request.GET.get('program')

    
    all_applications = []

    
    if program == 'FA':
        all_applications = FAApplication.objects.filter(user=user).order_by('-id')  
    elif program == 'FSC':
        all_applications = FSCApplication.objects.filter(user=user).order_by('-id')  
    elif program == 'BS':
        all_applications = BSApplication.objects.filter(user=user).order_by('-id') 
    else:
        
        fa_apps = FAApplication.objects.filter(user=user).order_by('-id')
        fsc_apps = FSCApplication.objects.filter(user=user).order_by('-id')
        bs_apps = BSApplication.objects.filter(user=user).order_by('-id')

        
        all_applications = sorted(
            list(fa_apps) + list(fsc_apps) + list(bs_apps), 
            key=lambda app: app.id, reverse=True  
        )

    return render(request, 'admissions/application_status.html', {
        'all_applications': all_applications,
    })





@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    
    program_id = request.GET.get('program')
    status, _ = AdmissionStatus.objects.get_or_create(id=1)
    if program_id:
        fa_applications = FAApplication.objects.filter(program_selection=program_id, status='submitted')
        fsc_applications = FSCApplication.objects.filter(program_selection=program_id, status='submitted')
        bs_applications = BSApplication.objects.filter(program_selection=program_id, status='submitted')
    else:
        fa_applications = FAApplication.objects.filter(status='submitted')
        fsc_applications = FSCApplication.objects.filter(status='submitted')
        bs_applications = BSApplication.objects.filter(status='submitted')

    programs = Program.objects.all()
    
    return render(request, 'admissions/admin_dashboard.html', {
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
        'programs': programs,
        'status': status
    })




@login_required
def all_applications(request):
    if not request.user.is_staff:
        return redirect('home')

    
    program = request.GET.get('program')

    
    fa_applications = FAApplication.objects.none()
    fsc_applications = FSCApplication.objects.none()
    bs_applications = BSApplication.objects.none()

    
    if program == 'FA':
        fa_applications = FAApplication.objects.all().order_by('-id')  
    elif program == 'FSC':
        fsc_applications = FSCApplication.objects.all().order_by('-id')  
    elif program == 'BS':
        bs_applications = BSApplication.objects.all().order_by('-id')  
    else:
        
        fa_applications = FAApplication.objects.all().order_by('-id')
        fsc_applications = FSCApplication.objects.all().order_by('-id')
        bs_applications = BSApplication.objects.all().order_by('-id')

    return render(request, 'admissions/all_applications.html', {
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
    })



@login_required
def accepted_applications(request):
    if not request.user.is_staff:
        return redirect('home')

    program = request.GET.get('program')

    fa_applications = FAApplication.objects.filter(status='accepted')
    fsc_applications = FSCApplication.objects.filter(status='accepted')
    bs_applications = BSApplication.objects.filter(status='accepted')

    if program == 'FA':
        fsc_applications = FSCApplication.objects.none()
        bs_applications = BSApplication.objects.none()
    elif program == 'FSC':
        fa_applications = FAApplication.objects.none()
        bs_applications = BSApplication.objects.none()
    elif program == 'BS':
        fa_applications = FAApplication.objects.none()
        fsc_applications = FSCApplication.objects.none()

    return render(request, 'admissions/accepted_applications.html', {
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
    })

@login_required
def rejected_applications(request):
    if not request.user.is_staff:
        return redirect('home')

    program = request.GET.get('program')

    fa_applications = FAApplication.objects.filter(status='rejected')
    fsc_applications = FSCApplication.objects.filter(status='rejected')
    bs_applications = BSApplication.objects.filter(status='rejected')

    if program == 'FA':
        fsc_applications = FSCApplication.objects.none()
        bs_applications = BSApplication.objects.none()
    elif program == 'FSC':
        fa_applications = FAApplication.objects.none()
        bs_applications = BSApplication.objects.none()
    elif program == 'BS':
        fa_applications = FAApplication.objects.none()
        fsc_applications = FSCApplication.objects.none()

    return render(request, 'admissions/rejected_applications.html', {
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
    })
    
    
    
def quota_based_applications(request):
    program = request.GET.get('program')
    subject = request.GET.get('subject')
    quota = request.GET.get('quota')

    
    fa_applications = []
    fsc_applications = []
    bs_applications = []

    
    if program or subject or quota:
        if program == 'FA':
            fa_applications = FAApplication.objects.filter(
                program_selection=subject if subject else '',
                quota=quota if quota else ''
            )
        elif program == 'FSC':
            fsc_applications = FSCApplication.objects.filter(
                program_selection=subject if subject else '',
                quota=quota if quota else ''
            )
        elif program == 'BS':
            bs_applications = BSApplication.objects.filter(
                program_selection=subject if subject else '',
                quota=quota if quota else ''
            )
    else:
        
        fa_applications = FAApplication.objects.all().order_by('-id')
        fsc_applications = FSCApplication.objects.all().order_by('-id')
        bs_applications = BSApplication.objects.all().order_by('-id')

    
    applications = list(fa_applications) + list(fsc_applications) + list(bs_applications)

    print("Applications found: ", applications)  
    context = {
        'applications': applications,
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
    }

    return render(request, 'admissions/quota_based_applications.html', context)

    

@login_required
def application_detail(request, app_id, app_type):
    
    if not request.user.is_staff:
        return redirect('home')

    
    if app_type == 'FA':
        application = get_object_or_404(FAApplication, id=app_id)
    elif app_type == 'FSC':
        application = get_object_or_404(FSCApplication, id=app_id)
    elif app_type == 'BS':
        application = get_object_or_404(BSApplication, id=app_id)
    else:
        return redirect('home')

    
    return render(request, 'admissions/application_detail.html', {
        'application': application,
        'app_type': app_type
    })



@login_required
def admin_update_application(request, app_id, app_type):
    if not request.user.is_staff:
        return redirect('home')

    status = request.GET.get('status')

    if app_type == 'FA':
        application = get_object_or_404(FAApplication, id=app_id)
    elif app_type == 'FSC':
        application = get_object_or_404(FSCApplication, id=app_id)
    elif app_type == 'BS':
        application = get_object_or_404(BSApplication, id=app_id)
    else:
        return redirect('home')

    if status in ['accepted', 'rejected']:
        application.status = status
        application.save()

        
        send_application_update_email(application, status)

        
        if status == 'accepted':
            messages.success(request, f'Application accepted successfully, and an email has been sent to the student.')
        elif status == 'rejected':
            messages.success(request, f'Application has been rejected and an email has been sent to the student.')

    return redirect('admin_dashboard')





def send_application_update_email(application, status):
    subject = 'Your Application Status Update'
    message = f'Your application has been {status}. Thank you for your application!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [application.user.email]  
    
    send_mail(subject, message, from_email, recipient_list)

def send_application_accepted_email(application):
    """
    Sends an email to the student notifying them that their application has been accepted.
    """
    student_email = application.user.email  
    subject = "Application Accepted"
    message = f"Dear {application.user.first_name},\n\nYour application for the {application.program_selection} program has been accepted.\n\nCongratulations!\n\nBest Regards,\nYour College Admissions Team"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student_email],  
        fail_silently=False,
    )


from django.db.models import F, ExpressionWrapper, FloatField, Q

@login_required
def create_merit_list(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        program = request.POST.get('program')
        subject = request.POST.get('subject')
        list_type = request.POST.get('list_type')
        quota = request.POST.get('quota') if list_type == 'quota' else None
        percentage_cutoff = float(request.POST.get('percentage_cutoff'))
        available_seats = int(request.POST.get('available_seats'))

        def send_email_to_students(applications):
            for application in applications:
                send_mail(
                    subject='New Merit List Published',
                    message=(
                        f'Hello {application.user.username},\n\n'
                        f'Congratulations! You have been selected in the {list_type} merit list for '
                        f'{program} ({subject}). Please visit the portal for more details.'
                    ),
                    from_email='sherykhx@gmail.com',
                    recipient_list=[application.user.email],
                )

        if program == 'FA':
            model = FAApplication
            obtained_field = 'marks_obtained'
            max_field = 'max_marks'
        elif program == 'FSC':
            model = FSCApplication
            obtained_field = 'marks_obtained'
            max_field = 'max_marks'
        elif program == 'BS':
            model = BSApplication
            obtained_field = 'marks_obtained'
            max_field = 'max_marks'
        else:
            messages.error(request, 'Invalid program selected.')
            return redirect('create_merit_list')

        previous_merit_lists = MeritList.objects.filter(program=program)
        previous_applications = set()
        for merit_list in previous_merit_lists:
            if program == 'FA':
                previous_applications.update(merit_list.fa_applications.all())
            elif program == 'FSC':
                previous_applications.update(merit_list.fsc_applications.all())
            elif program == 'BS':
                previous_applications.update(merit_list.bs_applications.all())

        applications = model.objects.annotate(
    percentage=ExpressionWrapper(
        F(obtained_field) * 100.0 / F(max_field), output_field=FloatField()
    )
).filter(
    percentage=percentage_cutoff,
    status='accepted'  
).exclude(
    id__in=[app.id for app in previous_applications]
)


        if list_type == 'quota' and quota:
            applications = applications.filter(quota=quota)

        selected_applications = applications.order_by('-percentage')[:available_seats]

        if selected_applications.exists():
            merit_list = MeritList.objects.create(
                program=program,
                subject=subject,
                list_type=list_type,
                quota=quota,
                percentage_cutoff=percentage_cutoff,
                available_seats=available_seats
            )

            if program == 'FA':
                merit_list.fa_applications.add(*selected_applications)
            elif program == 'FSC':
                merit_list.fsc_applications.add(*selected_applications)
            elif program == 'BS':
                merit_list.bs_applications.add(*selected_applications)

            merit_list.save()
            send_email_to_students(selected_applications)

            
            context = {
                'merit_list': merit_list,
                'applications': selected_applications,
                'program': program,
                'subject': subject,
                'list_type': list_type,
                'quota': quota,
                'percentage_cutoff': percentage_cutoff,
            }
            pdf = generate_pdf('admissions/merit_list_pdf.html', context)

            
            pdf_directory = os.path.join('media', 'merit_lists')
            os.makedirs(pdf_directory, exist_ok=True)

            
            pdf_filename = f"{program}_{subject}_merit_list.pdf"
            pdf_path = os.path.join(pdf_directory, pdf_filename)
            with open(pdf_path, 'wb') as f:
                f.write(pdf.getvalue())

            messages.success(
                request,
                f'{list_type.capitalize()} merit list created for {program} ({subject}) and exported as PDF. '
                f'Students have been notified.'
            )
        else:
            messages.warning(request, 'No eligible applications found for this merit list.')

        return redirect('admin_dashboard')

    return render(request, 'admissions/create_merit_list.html')


def generate_pdf(template_src, context_dict):
    """
    Generates a PDF file from an HTML template and context data.
    """
    template = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return result
    return None



@login_required
def toggle_admission_status(request, program_id):
    if not request.user.is_staff:
        return redirect('home')

    
    program = get_object_or_404(Program, id=program_id)
    program.is_open = not program.is_open 
    program.save()

    messages.success(request, f"Admissions for {program.name} {'opened' if program.is_open else 'closed'} successfully.")
    return redirect('admin_dashboard')



@login_required
def open_merit_lists(request):
    program = request.GET.get('program')
    subject = request.GET.get('subject')

    merit_lists = MeritList.objects.filter(list_type='open')
    if program:
        merit_lists = merit_lists.filter(program=program)
    if subject:
        merit_lists = merit_lists.filter(subject=subject) 

    return render(request, 'admissions/open_merit_list.html', {'merit_lists': merit_lists})


@login_required
def quota_merit_lists(request):
    program = request.GET.get('program')
    subject = request.GET.get('subject')
    quota = request.GET.get('quota')

    merit_lists = MeritList.objects.filter(list_type='quota')
    
    if program:
        merit_lists = merit_lists.filter(program=program)
    if subject:
        merit_lists = merit_lists.filter(subject=subject)  
    if quota:
        merit_lists = merit_lists.filter(quota=quota)

    return render(request, 'admissions/quota_merit_list.html', {'merit_lists': merit_lists})




@login_required
def check_new_applications(request):
    program = request.GET.get('program')
    subject = request.GET.get('subject')

    if program and subject:
        if program == 'FA':
            applications = FAApplication.objects.filter(status='accepted')
        elif program == 'FSC':
            applications = FSCApplication.objects.filter(status='accepted')
        elif program == 'BS':
            applications = BSApplication.objects.filter(status='accepted')

        previous_merit_lists = MeritList.objects.filter(program=program, subject=subject)
        previous_applications = []
        for merit in previous_merit_lists:
            previous_applications += list(merit.fa_applications.all() if program == 'FA' else merit.fsc_applications.all() if program == 'FSC' else merit.bs_applications.all())

        
        new_applications = [app for app in applications if app not in previous_applications]
        
        
        print(f"Program: {program}, Subject: {subject}, New Applications: {new_applications}")

        return JsonResponse({'new_applications_exist': bool(new_applications)})

    return JsonResponse({'new_applications_exist': False})




@login_required
def merit_list_detail(request, pk):
    merit_list = get_object_or_404(MeritList, pk=pk)

    return render(request, 'admissions/merit_list_detail.html', {
        'merit_list': merit_list,
        'fa_applications': merit_list.fa_applications.all(),
        'fsc_applications': merit_list.fsc_applications.all(),
        'bs_applications': merit_list.bs_applications.all(),
    })


@login_required
def merit_lists(request):
    program = request.GET.get('program')
    subject = request.GET.get('subject')

    
    if program and subject:
        merit_lists = MeritList.objects.filter(program=program, subject=subject)
    elif program:
        merit_lists = MeritList.objects.filter(program=program)
    else:
        merit_lists = MeritList.objects.all()

    subjects = []
    if program == 'BS':
        subjects = ['Computer Science', 'BBA Hons', 'Political Science']
    elif program == 'FSC':
        subjects = ['Medical', 'Humanities']
    elif program == 'FA':
        subjects = ['Arts']

    return render(request, 'admissions/merit_lists.html', {
        'merit_lists': merit_lists,
        'subjects': subjects,
    })


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    fa_applications = FAApplication.objects.filter(user=request.user)
    fsc_applications = FSCApplication.objects.filter(user=request.user)
    bs_applications = BSApplication.objects.filter(user=request.user)

    return render(request, 'admissions/profile.html', {
        'profile': profile,
        'fa_applications': fa_applications,
        'fsc_applications': fsc_applications,
        'bs_applications': bs_applications,
    })


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Verify this URL name matches your profile view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'admissions/edit_profile.html', {'form': form})




@login_required
def complete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'admissions/complete_profile.html', {'form': form})




def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            print("Announcement created:", announcement) 
            send_announcement_email(announcement)  
            return redirect('announcement_list')  
        else:
            print("Form errors:", form.errors) 
    else:
        form = AnnouncementForm()

    return render(request, 'admissions/create_announcement.html', {'form': form})



@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'admissions/edit_announcement.html', {'form': form, 'announcement': announcement})



@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement_list')

    return render(request, 'admissions/delete_announcement.html', {'announcement': announcement})


@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    return render(request, 'admissions/announcement_list.html', {'announcements': announcements})




@login_required
def student_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    return render(request, 'admissions/student_announcements.html', {'announcements': announcements})



