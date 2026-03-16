from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
   openapi.Info(
      title="Whiteboard API",
      default_version='v1',
      description="Whiteboard loyiha API dokumentatsiyasi",

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),
    path('api/token/', obtain_auth_token),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
]