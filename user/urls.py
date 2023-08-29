from django.urls import path, include
from . import views


urlpatterns = [
    # path('', include(router.urls)),
    path('signup/', views.signup, name='signup-user'),
    path('login/', views.login, name='login-user'),
]
