from django.urls import path
from . import views


urlpatterns = [

    path('sent/code/', views.SentCodeToPhoneNumberView.as_view(), name='sent_code'),
    path('verify/', views.VerifyCodeView.as_view(), name='verify'),

]
