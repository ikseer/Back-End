# myproject/urls.py
from django.urls import path

from .views import PredictView

urlpatterns = [
    # path('predict/',predict),
        # path('predict/', PredictView.as_view(), name='predict'),
    path('predict/', PredictView.as_view(), name='predict'),

]
