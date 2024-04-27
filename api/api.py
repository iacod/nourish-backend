from api.models import Volunteer
from ninja import NinjaAPI, Schema
from django.http import HttpRequest
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
    return "User already exists!"

  user = User.objects.create(
    username=data.username,
    first_name=data.first_name,
    last_name=data.last_name,
    email=data.email,
  )

  user.set_password(data.password)
  user.save()

  return data

@api.post("/login")
def log_in(request: HttpRequest, data: Login):
  user = authenticate(request, username=data.username, password=data.password)
  if user is not None:
    login(request, user)
    return data
  else:
    return "Invalid username or password!"

@api.post("/donate/{amount}")
def donate(request: HttpRequest, amount: int):
  if request.user.is_authenticated:
    request.user.volunteer.pounds += amount
    request.user.volunteer.save()
    return request.user.volunteer.pounds 
  else:
    return "You must be logged in to donate!"

@api.get("/donate")
def get_donation_amount(request: HttpRequest):
  if request.user.is_authenticated:
    if not hasattr(request.user, "volunteer"):
      volunteer = Volunteer(user=request.user, pounds=0)
      volunteer.save()
    return request.user.volunteer.pounds 
  else:
    return "You must be logged in to donate!"
