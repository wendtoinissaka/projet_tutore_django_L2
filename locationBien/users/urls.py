from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
# from .views import register, activate
from django.contrib.auth import views as auth_view
from django.conf.urls import handler404
from .views import error_404_view, create_product, user_update, EditBienView, DeleteBienView,  \
    process_payment, execute_payment, cancel_payment, activate

# handler404 = error_404_view
handler404 = 'users.views.error_404_view'


urlpatterns = [
    path('', views.home_without_filter, name='home_without_filter'),
    # path('filter/', views.home_with_filter, name='home_with_filter'),
    path('reservation_status_chart/', views.reservation_status_chart, name='reservation_status_chart'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('request_new_token/', views.request_new_token, name='demande_nouveau_token'),
    # # reinitialiser password
path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # path('password_reset/', views.request_password_reset, name='password_reset'),
    # # path('password_reset/', views.custom_password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # path('reset/', views.request_password_reset, name='password_reset'),
    # path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # # ...

    # path('users/', views.user_list, name='user_list'),
    # path('users/create/', views.user_create, name='user_create'),

    path('registration_confirmation/', views.registration_confirmation, name='registration_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('contactUs/', views.contactUs, name='contactUs'),
    # path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),

    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    # path('logout/', custom_logout, name="logout"),
    path('bien/<int:bien_id>/', views.detail_bien, name='detail_bien'),
    # path('reservation/<int:bien_id>/', views.do_reservation, name='do_reservation'),
    path('erreur/', views.erreur, name='erreur'),
    path('404/', views.error_404_view, name='handler404'),
    path('create_product/', views.create_product, name='create_product'),
    path('user_update/', views.user_update, name='user_update'),
    path('header/', views.header, name='header'),
    path('detail/', views.detail_bien, name='detail_bien'),
    path('list_user_bien/', views.list_user_bien, name='list_user_bien'),
    path('list_user_bien1/', views.list_user_bien1, name='list_user_bien1'),
    path('<int:pk>/edit/', EditBienView.as_view(), name='edit_bien'),
    path('<int:pk>/supprimer/', DeleteBienView.as_view(), name='delete_bien'),
    path('ajouter_avis/<int:bien_id>/', views.ajouter_avis, name='ajouter_avis'),

    #reservations

    path('reservation_page/', views.reservation_page, name='reservation_page'),
    path('reservations_sur_mes_biens/', views.reservations_sur_mes_biens, name='reservations_sur_mes_biens'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation,name='cancel_reservation'),
    path('reservations/cancel/<int:reservation_id>/', views.confirm_cancel_reservation, name='confirm_cancel_reservation'),
    # path('reservations/make_payment/<int:pk>/', PaymentCreateView.as_view(), name='make_payment'),
    path('reservation/<int:bien_id>/', views.do_reservation, name='do_reservation'),
    path('reservation/detail/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/validate/<int:reservation_id>/', views.validate_reservation, name='validate_reservation'),

    # #paiements
    # path('process/', process_payment, name='process_payment'),
    path('process/<int:reservation_id>/', views.process_payment, name='process_payment'),
    path('execute/', execute_payment, name='execute_payment'),
    path('execute-stripe/<int:reservation_id>/', views.execute_payment1, name='execute_payment1'),
    path('cancel/', cancel_payment, name='cancel_payment'),
    # path('cancel-payment-stripe/<int:reservation_id>/', views.cancel_payment_stripe, name='cancel_payment_stripe'),
    path('cancel-payment/<int:reservation_id>/', views.cancel_payment, name='cancel_payment1'),
    path('reservation/payment/success/', views.payment_success, name='payment_success'),

    # stripe integration
    path('stripe/', views.stripeHome ,name="stripe_home"),
    path('stripe-confirm-payment/', views.stripe_confirm_payment, name='stripe_confirm_payment'),
    path('stripe-checkout/', views.checkout ,name="stripe_checkout"),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

