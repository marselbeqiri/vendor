from django.contrib import admin
from django.urls import path, include

from project import settings

api_patterns = [
    path('auth/', include('applications.authentication.urls'), name="Authentication"),
    path('', include('applications.vending_machine.urls'), name="Authentication"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]

if settings.DEBUG:
    from project.swagger_urls import swagger_urlpatterns

    urlpatterns += swagger_urlpatterns

admin.site.site_header = "Vending Machine 2022"
admin.site.site_title = "Vending Machine Admin Panel"
admin.site.index_title = "Vending Machine administration area"
