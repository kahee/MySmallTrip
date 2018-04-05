from django.urls import path

from .apis import FrequentQuestionView

urlpatterns = [
    path('', FrequentQuestionView.as_view(), name='frequentquestion'),

]
