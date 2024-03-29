from django.urls import path

from .views import (
    firebase_test,
    login,
    main,
    register,
    send_email_to_user,
    test,
    upload_profile,
)

urlpatterns = [
    path("", main),
    path("apis/register", register),
    path("apis/login", login),
    path("apis/upload-profile", upload_profile),
    # test urls.
    path("apis/test", test),
    path("apis/firebase_test", firebase_test),
    path("apis/send_email_to_user", send_email_to_user),
]
