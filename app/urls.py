from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from app.views import ProductView,ProductDetailView,CustomerRegistrationView
from django.contrib.auth import views as auth_views
from app.forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordResetDoneView

urlpatterns = [
    path('',ProductView.as_view(),name = 'home'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('account/login/',LoginView.as_view(template_name = 'app/login.html',
                                            authentication_form = LoginForm),
                                            name = 'login'),
    path('logout/',LogoutView.as_view(next_page = 'home'),name = 'logout'),
    path('passwordchange/',PasswordChangeView.as_view(template_name = 'app/passwordchange.html',
                                                    form_class = MyPasswordChangeForm,
                                                    success_url = '/passwordchangedone/'),
                                                    name = 'passwordchange'),
    path('passwordchangedone/',PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'),
         name = 'passwordchangedone'),
    path('password-reset/',PasswordResetView.as_view(template_name = 'app/password_reset.html',form_class = MyPasswordResetForm),name = 'password_reset'),
    path('password-reset-done/',PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),name = 'password_reset_done'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name = 'password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html', form_class = MySetPasswordForm),name = 'password_reset_confirm'),
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
