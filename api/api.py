from pydantic.config import JsonDict
from api.models import Volunteer
from ninja import NinjaAPI, Schema
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ninja.security import django_auth
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

api = NinjaAPI(csrf=True)

class Register(Schema):
  username: str
  first_name: str
  last_name: str
  email: str
  password: str

class Login(Schema):
  username: str
  password: str

@api.post("/register")
@csrf_exempt
def register(request: HttpRequest, data: Register):
  user = User.objects.filter(username=data.username, email=data.email)

  if user.exists():
    return JsonResponse({"message": "User already exists"}, status=409)

  user = User.objects.create(
    username=data.username,
    first_name=data.first_name,
    last_name=data.last_name,
    email=data.email,
  )

  user.set_password(data.password)
  user.save()

  return JsonResponse(data.dict(), status=200)

@api.post("/login")
@ensure_csrf_cookie
@csrf_exempt
def log_in(request: HttpRequest, data: Login):
  user = authenticate(request, username=data.username, password=data.password)
  if user is not None:
    login(request, user)
    return JsonResponse(data.dict(), status=200)
  else:
    return JsonResponse({"message": "Invalid username or password"}, status=406)

@api.post("/donate/{amount}", auth=django_auth)
def donate(request: HttpRequest, amount: int):
  request.user.volunteer.pounds += amount
  request.user.volunteer.save()
  return JsonResponse({"amount_donated": amount}, status=200)

@api.get("/donate", auth=django_auth)
def get_donation_amount(request: HttpRequest):
  if not hasattr(request.user, "volunteer"):
    volunteer = Volunteer(user=request.user, pounds=0)
    volunteer.save()
  return JsonResponse({"amount_donated": request.user.volunteer.pounds}, status=200)

@api.get("/user", auth=django_auth)
def get_user(request: HttpRequest):
  return JsonResponse(model_to_dict(request.user), status=200)