from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import firestore
from .models import MasterProducts, User
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.
def main(request):
    return render(request, "main.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            body = parse_body(request.body)
            username, password = body.get("username"), body.get("password")

            # email validation
            EmailValidator()(username)

            # check if a user already exists with these credentials.
            try:
                User.objects.get(username=username)
                return get_error_response("USER ALREADY EXISTS")
            except ObjectDoesNotExist:
                # now we can create a new user in db and firebase
                db = firestore.client()

                user = User(**body)
                user.set_password(password)
                collection_ref = db.collection("users")
                new_user = {"uuid": str(user.id), "profile": ""}
                document = collection_ref.add(new_user)[1]
                user.fb_doc_id = document.id
                user.save()

                # send a welcome email to user.

                # create access and refresh token to user.
                return get_success_response(generate_tokens(user))

        except Exception as ex:
            return get_error_response(ex.args)
    else:
        return get_method_error(request, "POST")


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            body = parse_body(request.body)
            username, password = body.get("username"), body.get("password")

            # email validation
            EmailValidator()(username)

            # check if a user exists with these credentials.
            user = authenticate(username=username, password=password)
            if user is None:
                return get_error_response("USER NOT FOUND")

            payload = generate_tokens(user)
            payload["profile_picture"] = user.profile_picture
            payload["dob"] = user.birth_date
            return get_success_response(payload)

        except Exception as ex:
            return get_error_response(ex.args)
    else:
        return get_method_error(request, "POST")


# TODO has to be removed later
def test(req):
    objects = MasterProducts.objects.all()
    b = True
    for row in objects:
        if row.gender == "M" or row.gender == "F":
            row.gender = "M" if b else "F"
            b = not b
            row.save()
    return JsonResponse("Done", safe=False)


# TODO has to be removed later
def firebase_test(req):
    """

    get doc using .get() and run .to_dict()

    """
    db = firestore.client()
    collection_ref = db.collection("users")
    new_user = {"uuid": "397730e4-b0fe-49e0-bdbb-7bb892cc2864", "profile": ""}
    res = collection_ref.add(new_user)
    return JsonResponse(
        {"data": res[1].get().to_dict(), "doc_id": res[1].id}, safe=False
    )


# TODO has to be removed test email sender.
def send_email_to_user(request):
    recipient_email = "codewithruppu@gmail.com"
    recipient_name = "Rupesh"

    # Load the HTML template
    email_template_path = "email_template.html"
    email_html_message = render_to_string(
        email_template_path, {"recipient_name": recipient_name}
    )

    # Create an EmailMessage object
    email = EmailMessage(
        "This is a test email message.",
        email_html_message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
    )
    email.content_subtype = "html"  # Set the content type to HTML

    # Send the email
    email.send()

    return JsonResponse("email sent", safe=False)
