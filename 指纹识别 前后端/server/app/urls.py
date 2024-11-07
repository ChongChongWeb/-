import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('users/<str:module>/', app.views.UserView.as_view()),
    path('apps/<str:module>/', app.views.AppView.as_view()),
    path('fingers/<str:module>/', app.views.FingerView.as_view()),
    path('scan/<str:module>/', app.views.ScanView.as_view()),
]