from django.contrib import admin
from django.urls import include, path

from accounts.views import CustomRegisterView, FacebookLogin, GoogleLogin
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('register/', CustomRegisterView.as_view(), name='rest_register'),
    # path('register/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    # path('allauth/', include('allauth.urls'))
    path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]


