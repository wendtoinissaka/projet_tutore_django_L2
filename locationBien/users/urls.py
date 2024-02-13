from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf.urls import handler404
from .views import error_404_view, create_product, user_update, EditBienView, DeleteBienView

# handler404 = error_404_view
handler404 = 'users.views.error_404_view'


urlpatterns = [
    path('', views.home_without_filter, name='home_without_filter'),
    path('filter/', views.home_with_filter, name='home_with_filter'),



    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    # path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),

                  path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    # path('logout/', custom_logout, name="logout"),
    path('bien/<int:bien_id>/', views.detail_bien, name='detail_bien'),
    path('reservation/<int:bien_id>/', views.do_reservation, name='do_reservation'),
    path('erreur/', views.erreur, name='erreur'),
    path('404/', views.error_404_view, name='handler404'),
    path('create_product/', views.create_product, name='create_product'),
    path('user_update/', views.user_update, name='user_update'),
    path('header/', views.header, name='header'),
    path('detail/', views.detail_bien, name='detail_bien'),
    path('list_user_bien/', views.list_user_bien, name='list_user_bien'),
    path('<int:pk>/edit/', EditBienView.as_view(), name='edit_bien'),
    path('<int:pk>/supprimer/', DeleteBienView.as_view(), name='delete_bien'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

