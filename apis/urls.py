from django.urls import path
from .views import *


urlpatterns = [
    path("", main),
    path("apis/test", test),
    path("apis/firebase_test", firebase_test),
]
