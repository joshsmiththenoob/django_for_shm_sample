from django.urls import path
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
                                            TokenObtainPairView,
                                            TokenRefreshView,
                                            )
from .view.login_view import LoginView
from .view.registration_view import RegistrationView
from .view.refresh_token_view import CookieTokenRefreshView
from .view.logout_view import LogoutView
from .view.group_urls_view import GroupUrlsView


schema_view = get_schema_view(
    openapi.Info(
        title="Bridge Health Monitoring System API",
        default_version='v1',
        description="API documentation for Bridge Health Monitoring System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path("login/", obtain_auth_token, name = "login"),
    path("register/", RegistrationView.as_view(), name = "register"),
    # path("logout/", LogoutView.as_view(), name = "logout"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name= "logout"),
    path("group-link/", GroupUrlsView.as_view(), name= "group_url"),
] 