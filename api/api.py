from pydantic.config import JsonDict
from api.models import Volunteer
from ninja import NinjaAPI, Schema
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

api = NinjaAPI()

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
def register(request: HttpRequest, data: Register):
  user = User.objects.filter(username=data.username, email=data.email)

  if user.exists():
    return JsonResponse({"User already exists"}, status=409)

  user = User.objects.create(
    username=data.username,
    first_name=data.first_name,
    last_name=data.last_name,
    email=data.email,
  )

  user.set_password(data.password)
  user.save()

  return JsonResponse(data, status=200)

@api.post("/login")
def log_in(request: HttpRequest, data: Login):
  user = authenticate(request, username=data.username, password=data.password)
  if user is not None:
    login(request, user)
    return JsonResponse(data, status=200)
  else:
    return JsonResponse({"Invalid username or password"}, status=406)

@api.post("/donate/{amount}")
def donate(request: HttpRequest, amount: int):
  if request.user.is_authenticated:
    request.user.volunteer.pounds += amount
    request.user.volunteer.save()
    return JsonResponse({amount}, status=200)
  else:
    return JsonResponse({"You must be logged in"}, status=401)

@api.get("/donate")
def get_donation_amount(request: HttpRequest):
  if request.user.is_authenticated:
    if not hasattr(request.user, "volunteer"):
      volunteer = Volunteer(user=request.user, pounds=0)
      volunteer.save()
    return JsonResponse({request.user.volunteer.pounds}, status=200)
  else:
    return JsonResponse({"You must be logged in"}, status=401)
