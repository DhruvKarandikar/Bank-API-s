from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('')

urlpatterns = [
    path('transaction/', views.transaction, name='balance-func'),
    path('get_balance/', views.get_balance, name='show-balance'),
]
