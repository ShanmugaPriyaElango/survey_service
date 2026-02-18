from .views import UsersListCreateAPIView
from django.urls import path

urlpatterns = [
    path('', UsersListCreateAPIView.as_view())
]
