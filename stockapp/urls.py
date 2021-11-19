from django.contrib import auth
from django.urls import path
from . import views

urlpatterns = [
    path('signin',views.signin, name='signin'),
    path('signup',views.signup,name='signup'),
    path('signout',views.signout, name= 'signout'),
    path('stockpicker/',views.stockPicker,name= 'stockpicker'),
    path('stocktracker/',views.stockTracker, name= 'stocktracker'),
]