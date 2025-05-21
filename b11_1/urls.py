# b11_1/urls.py

from django.views.i18n import JavaScriptCatalog
from django.urls import include, path
from . import views
from .views import (CustomLoginView, UserLogout, CustomPasswordChangeView, CustomPasswordResetConfirmView, ListMaterial_IL_View, ShowMaterial_IL_View, AddMaterial_IL_View, UpdateMaterial_IL_View, ListMaterial_GD_View, ListMaterialArchived_GD_View, UpdateMaterial_GD_View, ShowMaterial_GD_View, ListMaterial_SMDA_View, ListMaterialArchived_SMDA_View, UpdateMaterial_SMDA_View, ShowMaterial_SMDA_View, ListMaterial_LBA_View, ListMaterialArchived_LBA_View, UpdateMaterial_LBA_View, ShowMaterial_LBA_View, Logging_View, ExcelImportView, RegisterView, CompleteRegistrationView, PendingRegistrationsView, ApproveRegistrationView, RejectRegistrationView, ExportLogsView, PreRegisterView, VerifyEmailView)
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403
from b11_1.views import custom_permission_denied_view
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

handler403 = custom_permission_denied_view

urlpatterns = [
    # Add JavaScript translations catalog
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    
    # Existing URL patterns
    path('', views.home, name='home'),
    path('admin/logging', Logging_View.as_view(), name='logging'),
    path('admin/import-excel', ExcelImportView.as_view(), name='import_excel'),
    path('admin/export-logs/', ExportLogsView.as_view(), name='export_logs'),
    path('login_user', CustomLoginView.as_view(), name='login_user'),
    path('logout_user', UserLogout.as_view(), name='logout_user'),
    path('password_change', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', 
         TemplateView.as_view(template_name='admin/password_change_done.html'),
         name='password_change_done'),
    path('password_reset',
         PasswordResetView.as_view(template_name='admin/password_reset.html'),
         name='password_reset'),
    path('reset/<uidb64>/<token>',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done',
         PasswordResetCompleteView.as_view(template_name='admin/password_reset_complete.html'),
         name='password_reset_complete'),

    # Material IL paths
    path('list_material_il',
         login_required(ListMaterial_IL_View.as_view()),
         name='list_material_il'),
    path('add_material_il',
         login_required(AddMaterial_IL_View.as_view()),
         name='add_material_il'),
    path('update_material_il/<int:pk>',
         login_required(UpdateMaterial_IL_View.as_view()),
         name='update_material_il'),
    path('show_material_il/<int:pk>', login_required(ShowMaterial_IL_View.as_view()), name='show_material_il'),

    # Material GD paths
    path('list_material_gd',
         login_required(ListMaterial_GD_View.as_view()),
         name='list_material_gd'),
    path('list_material_gd_archived',
         login_required(ListMaterialArchived_GD_View.as_view()),
         name='list_material_gd_archived'),
    path('update_material_gd/<int:pk>',
         login_required(UpdateMaterial_GD_View.as_view()),
         name='update_material_gd'),
    path('show_material_gd/<int:pk>', login_required(ShowMaterial_GD_View.as_view()), name='show_material_gd'),

    # Material SMDA paths
    path('list_material_smda',
         login_required(ListMaterial_SMDA_View.as_view()),
         name='list_material_smda'),
    path('list_material_smda_archived',
         login_required(ListMaterialArchived_SMDA_View.as_view()),
         name='list_material_smda_archived'),
    path('update_material_smda/<int:pk>',
         login_required(UpdateMaterial_SMDA_View.as_view()),
         name='update_material_smda'),
    path('show_material_smda/<int:pk>', login_required(ShowMaterial_SMDA_View.as_view()), name='show_material_smda'),

    # Material LBA paths
    path('list_material_lba',
         login_required(ListMaterial_LBA_View.as_view()),
         name='list_material_lba'),
    path('list_material_lba_archived',
         login_required(ListMaterialArchived_LBA_View.as_view()),
         name='list_material_lba_archived'),
    path('update_material_lba/<int:pk>',
         login_required(UpdateMaterial_LBA_View.as_view()),
         name='update_material_lba'),
    path('show_material_lba/<int:pk>', login_required(ShowMaterial_LBA_View.as_view()), name='show_material_lba'),

    # Registration paths
    path('registration/register/', RegisterView.as_view(), name='register'),
    path('registration/pre-register/', PreRegisterView.as_view(), name='pre_register'),
    path('registration/email/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('registration/complete-registration/<str:token>/', CompleteRegistrationView.as_view(), name='complete_registration'),

    # Admin registration management
    path('admin/pending-registrations/', PendingRegistrationsView.as_view(), name='pending_registrations'),
    path('admin/approve-registration/<int:profile_id>/', ApproveRegistrationView.as_view(), name='approve_registration'),
    path('admin/reject-registration/<int:profile_id>/', RejectRegistrationView.as_view(), name='reject_registration'),
]
