from django.contrib import admin
from django.urls import path, include

from responses.views import UserResponsesListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/surveys/', include('surveys.urls')),
    path('api/responses/', UserResponsesListView.as_view())
]
