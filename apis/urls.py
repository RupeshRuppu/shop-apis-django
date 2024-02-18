from django.urls import path
from .views import *


urlpatterns = [
    path("", main),
    path("apis/register", register),
    path("apis/login", login),
    # test urls.
    path("apis/test", test),
    path("apis/firebase_test", firebase_test),
    path("apis/send_email_to_user", send_email_to_user),
]
