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
    path('profile/', views.Profile.as_view(), name='profile'),

    path('domains/register/', views.RegisterDomainAPIView.as_view(), name='domain-create'),
    path('user/domains/', views.UserDomains.as_view(), name='user-domains'),

    path('domains/search/', views.DomainSearch.as_view(), name='domain-search'),
    path('whois/', views.WhoisLookupView.as_view(), name='whois_lookup'),

]
