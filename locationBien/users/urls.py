from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

# from .views import register, activate
from django.contrib.auth import views as auth_view
from django.conf.urls import handler404
from .views import error_404_view, create_product, user_update, EditBienView, DeleteBienView,  \
    process_payment, execute_payment, cancel_payment, activate

# handler404 = error_404_view
handler404 = 'users.views.error_404_view'


urlpatterns = [
    path('', views.home_without_filter, name='home_without_filter'),
    path('filter/', views.home_with_filter, name='home_with_filter'),



    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
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
    path('<int:pk>/edit/', EditBienView.as_view(), name='edit_bien'),
    path('<int:pk>/supprimer/', DeleteBienView.as_view(), name='delete_bien'),
    path('ajouter_avis/<int:bien_id>/', views.ajouter_avis, name='ajouter_avis'),

    #reservations

    path('reservation_page/', views.reservation_page, name='reservation_page'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation,name='cancel_reservation'),
    path('reservations/cancel/<int:reservation_id>/', views.confirm_cancel_reservation, name='confirm_cancel_reservation'),
    # path('reservations/make_payment/<int:pk>/', PaymentCreateView.as_view(), name='make_payment'),
    path('reservation/<int:bien_id>/', views.do_reservation, name='do_reservation'),
    path('reservation/detail/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/validate/<int:reservation_id>/', views.validate_reservation, name='validate_reservation'),

    # #paiements
    # path('process_payment/', views.payment_init, name='process_payment'),
    # path('execute_payment/', views.payment_return, name='execute_payment'),
    # path('cancel_payment/', views.payment_cancel, name='cancel_payment'),

                  # path('process/', process_payment, name='process_payment'),
                  path('process/<int:reservation_id>/', views.process_payment, name='process_payment'),
                  path('execute/', execute_payment, name='execute_payment'),
                  path('cancel/', cancel_payment, name='cancel_payment'),
                  path('reservation/payment/success/', views.payment_success, name='payment_success'),
    # Autres itinéraires…
    # ##encore test paiement
    # path('encorePai/', views.encoreHome, name='encoreHome'),
    # path('encoresuccessful/', views.encoreSuccess, name='encoreSuccess'),
    # path('encorecancelled/', views.encoreCancel, name='encoreCancel'),
    # path('encorePaypal/', include('paypal_standard.ipn.urls')),

    # stripe integration
    path('stripe/', views.stripeHome ,name="stripe_home"),
                  path('stripe-confirm-payment/', views.stripe_confirm_payment, name='stripe_confirm_payment'),
    path('stripe-checkout/', views.checkout ,name="stripe_checkout"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

