from django.shortcuts import render
from .models import MasterProducts
from django.http import JsonResponse
from firebase_admin import firestore


# Create your views here.
def main(request):
    return render(request, "main.html")


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
