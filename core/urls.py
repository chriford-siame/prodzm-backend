from django.contrib import admin
from django.urls import path, re_path, include

from drf_yasg2 import openapi
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="ProdZM",
        default_version="v3",
        description="API interface",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="prodzm@support.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('', include('prodzm.routers')),
    
    path('token/get/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
]
