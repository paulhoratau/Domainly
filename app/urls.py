from django.urls import path, include
from app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.CreateUserView.as_view(), name='register'),

    path('domain-create/', views.DomainCreate.as_view(), name='domain-create'),
    path('domain-detailed/', views.DomainCreate.as_view(), name='domain-detailed'),
    path('search/', views.DomainSearch.as_view(), name='domain-search'),

]
