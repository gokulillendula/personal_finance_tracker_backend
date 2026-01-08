from django.http import HttpResponse, JsonResponse
import json
from .models import User,Spent,Earned
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveAPIView,CreateAPIView
from .serializers import EarnedSerializer,SpentSerializer,UserSerializer,UserDetailsSerializer,RegisterSerializer



def greet(request):
    return HttpResponse("Hello, welcome to the Finance Tracker!")




class Users(ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    def get_permissions(self):
        if self.request.method=='GET':
            self.permission_classes=[IsAdminUser]
        self.permission_classes=[AllowAny]
        return super().get_permissions()


@csrf_exempt
def user_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)


    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")
    

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)
    user = authenticate(request, username=email, password=password)
    

    if user is None:
        return JsonResponse({"error": "Invalid email or password"}, status=401)


    auth_login(request, user)

    return JsonResponse({
        "message": "Login successful",
        "email": user.email
    })




class UserSummary(RetrieveAPIView):
    serializer_class=UserDetailsSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]
    def get_object(self):
        return self.request.user




class spent(ListCreateAPIView):
    serializer_class=SpentSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def get_queryset(self):
        return Spent.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Earned(ListCreateAPIView):
    serializer_class=EarnedSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]
    def get_queryset(self):
        return Earned.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

