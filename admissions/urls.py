from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('super-secret-admin/signup/', views.admin_signup, name='admin_signup'),  
    path('super-secret-admin/login/', views.admin_login, name='admin_login'),     
    path('super-secret-admin/logout/', views.admin_logout, name='admin_logout'),  
    path('', views.landingpage, name='landingpage'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('apply/fa/', views.fa_apply, name='fa_apply'),
    path('apply/fsc/', views.fsc_apply, name='fsc_apply'),
    path('apply/bs/', views.bs_apply, name='bs_apply'),
    path('quota-based-applications/', views.quota_based_applications, name='quota_based_applications'),
    path('application_status/', views.application_status, name='application_status'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('application/update/<int:app_id>/<str:app_type>/', views.admin_update_application, name='admin_update_application'),
    path('create-merit-list/', views.create_merit_list, name='create_merit_list'),
    path('admin_dashboard/all_applications/', views.all_applications, name='all_applications'),
    path('admin_dashboard/accepted_applications/', views.accepted_applications, name='accepted_applications'),
    path('admin_dashboard/rejected_applications/', views.rejected_applications, name='rejected_applications'),
    path('merit-lists/<int:merit_list_id>/', views.merit_list_detail, name='merit_list_detail'),
    path('application/<int:app_id>/<str:app_type>/detail/', views.application_detail, name='application_detail'),
    path('merit-lists/', views.merit_lists, name='merit_lists'),
    path('open-merit-lists/', views.open_merit_lists, name='open_merit_lists'),
    path('quota-merit-lists/', views.quota_merit_lists, name='quota_merit_lists'),
    path('toggle-admission-status/<int:program_id>/', views.toggle_admission_status, name='toggle_admission_status'),
    path('student_announcements/', views.student_announcements, name='student_announcements'),
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcements/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="admissions/password_reset_form.html"),
        name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="admissions/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="admissions/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="admissions/password_reset_complete.html"), name='password_reset_complete'),
    path('check-new-applications/', views.check_new_applications, name='check_new_applications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
