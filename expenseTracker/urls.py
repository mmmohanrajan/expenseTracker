from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="expenseTracker API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

urlpatterns += [
   url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
   url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
   url(r'^docs1/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
