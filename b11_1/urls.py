from django.views.i18n import JavaScriptCatalog
from django.urls import include
from django.urls import path
from . import views
from .views import CustomLoginView, UserLogout, ListMaterial_View, ListMaterial_IL_View, AddMaterial_IL_View, UpdateMaterial_IL_View, ShowMaterial_IL_View, ListMaterial_GD_View, AddMaterial_GD_View, UpdateMaterial_GD_View, ShowMaterial_GD_View, ListMaterial_SMDA_View, AddMaterial_SMDA_View, UpdateMaterial_SMDA_View, ShowMaterial_SMDA_View
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403
from b11_1.views import custom_permission_denied_view

handler403 = custom_permission_denied_view

urlpatterns = [
    path(r'', views.home, name='home'),
    path('login_user', CustomLoginView.as_view(), name='login-user'),
    path('logout_user', UserLogout.as_view(), name='logout-user'),
    path('list_material', login_required(ListMaterial_View.as_view()), name='list-material'),

    path('list_material_il', login_required(ListMaterial_IL_View.as_view()), name='list-material-il'),
    path('add_material_il', login_required(AddMaterial_IL_View.as_view()), name='add-material-il'),
    path('update_material_il/<int:pk>', login_required(UpdateMaterial_IL_View.as_view()), name='update-material-il'),
    path('show_material_il/<int:pk>', login_required(ShowMaterial_IL_View.as_view()), name='show-material-il'),

    path('list_material_gd', login_required(ListMaterial_GD_View.as_view()), name='list-material-gd'),
    path('add_material_gd', login_required(AddMaterial_GD_View.as_view()), name='add-material-gd'),
    path('update_material_gd/<int:pk>', login_required(UpdateMaterial_GD_View.as_view()), name='update-material-gd'),
    path('show_material_gd/<int:pk>', login_required(ShowMaterial_GD_View.as_view()), name='show-material-gd'),

    path('list_material_smda', login_required(ListMaterial_SMDA_View.as_view()), name='list-material-smda'),
    path('add_material_smda', login_required(AddMaterial_SMDA_View.as_view()), name='add-material-smda'),
    path('update_material_smda/<int:pk>', login_required(UpdateMaterial_SMDA_View.as_view()), name='update-material-smda'),
    path('show_material_smda/<int:pk>', login_required(ShowMaterial_SMDA_View.as_view()), name='show-material-smda'),

]
