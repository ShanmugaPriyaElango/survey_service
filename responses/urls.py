from django.urls import path
from .views import ResponseListCreateView, ResponseReadView


urlpatterns = [
    path('', ResponseListCreateView.as_view()),
    path('<pk>', ResponseReadView.as_view()),
]
