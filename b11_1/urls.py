from django.views.i18n import JavaScriptCatalog
from django.urls import include
from django.urls import path
from . import views
from .views import UserLogin, UserLogout, ListMaterial_View, ListMaterial_IL_View, AddMaterial_IL
from django.contrib.auth.decorators import login_required

# urlpatterns += [
#     path('mgmt/', include('mgmt.urls')),
# ]

urlpatterns = [
    path(r'', views.home, name='home'),
    path('login_user', UserLogin.as_view(), name='login-user'),
    path('logout_user', UserLogout.as_view(), name='logout-user'),
    path('list_material', login_required(ListMaterial_View.as_view()), name='list-material'),
    path('list_material_il', login_required(ListMaterial_IL_View.as_view()), name='list-material-il'),
    path('add_material_il', login_required(AddMaterial_IL.as_view()), name='add-material-il'),
]
