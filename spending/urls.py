from django.urls import path
from spending.views import Signupview
from spending.views import GetMeView
from spending.views import ExpenseListCreateView
from spending.views import ExpenseRetrieveUpdateDeleteView

urlpatterns =[
    path("register/", Signupview.as_view()),
    path("me/",GetMeView.as_view()),
    path("expense/",ExpenseListCreateView.as_view()),
    path("expense/<int:pk>/",ExpenseRetrieveUpdateDeleteView.as_view()),

  ]