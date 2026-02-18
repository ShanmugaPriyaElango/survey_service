from django.urls import path, include
from .views import SurveyListCreateView, SurveyReadUpdateView


urlpatterns = [
    path('', SurveyListCreateView.as_view()),
    path('<pk>', SurveyReadUpdateView.as_view()),
    path('<survey_id>/responses/', include('responses.urls'))
]
