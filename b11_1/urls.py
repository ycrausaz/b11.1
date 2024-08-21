from django.views.i18n import JavaScriptCatalog
from django.urls import include
from django.urls import path
from . import views
from .views import CustomLoginView, UserLogout, CustomPasswordChangeView, CustomPasswordResetConfirmView, ListMaterial_IL_View, AddMaterial_IL_View, UpdateMaterial_IL_View, ShowMaterial_IL_View, ListMaterial_GD_View, ListMaterialArchived_GD_View, UpdateMaterial_GD_View, ShowMaterial_GD_View, ListMaterial_SMDA_View, ListMaterialArchived_SMDA_View, UpdateMaterial_SMDA_View, ShowMaterial_SMDA_View
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403
from b11_1.views import custom_permission_denied_view
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

handler403 = custom_permission_denied_view

urlpatterns = [
    path(r'', views.home, name='home'),
    path('login_user', CustomLoginView.as_view(), name='login_user'),
    path('logout_user', UserLogout.as_view(), name='logout_user'),
    path('password_change', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', TemplateView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('list_material_il', login_required(ListMaterial_IL_View.as_view()), name='list_material_il'),
    path('add_material_il', login_required(AddMaterial_IL_View.as_view()), name='add_material_il'),
    path('update_material_il/<int:pk>', login_required(UpdateMaterial_IL_View.as_view()), name='update_material_il'),
    path('show_material_il/<int:pk>', login_required(ShowMaterial_IL_View.as_view()), name='show_material_il'),

    path('list_material_gd', login_required(ListMaterial_GD_View.as_view()), name='list_material_gd'),
    path('list_material_archived_gd', login_required(ListMaterialArchived_GD_View.as_view()), name='list_material_archived_gd'),
    path('update_material_gd/<int:pk>', login_required(UpdateMaterial_GD_View.as_view()), name='update_material_gd'),
    path('show_material_gd/<int:pk>', login_required(ShowMaterial_GD_View.as_view()), name='show_material_gd'),

    path('list_material_smda', login_required(ListMaterial_SMDA_View.as_view()), name='list_material_smda'),
    path('list_material_archived_smda', login_required(ListMaterialArchived_SMDA_View.as_view()), name='list_material_archived_smda'),
    path('update_material_smda/<int:pk>', login_required(UpdateMaterial_SMDA_View.as_view()), name='update_material_smda'),
    path('show_material_smda/<int:pk>', login_required(ShowMaterial_SMDA_View.as_view()), name='show_material_smda'),

]
