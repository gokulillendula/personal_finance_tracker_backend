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
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveAPIView
from .serializers import EarnedSerializer,SpentSerializer,UserSerializer



def greet(request):
    return HttpResponse("Hello, welcome to the Finance Tracker!")


class UserList(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAdminUser]



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method!='POST':
        return JsonResponse({"error": "POST method required"}, status=405)
    data=json.loads(request.body)
    email=data.get('email')
    password=data.get("password")
    
    if not all([email,password]):
        return JsonResponse({"error":"All required fields should be filled"},status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error":"user with email already exisits"},status=400)
    
    user=User.objects.create_user(
        email=email,
        password=password
    )
    return JsonResponse({"success":"user created successfully",
                         "email":user.email},status=201)
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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user=request.user
    return Response({
        'email':user.email,
        'balance':user.balance,
        'earned': EarnedSerializer(user.earned.all(), many=True).data,
        'Spent':SpentSerializer(user.spent.all(),many=True).data,
    })


class Addspent(ListCreateAPIView):
    serializer_class=SpentSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def get_queryset(self):
        return Spent.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddEarned(ListCreateAPIView):
    serializer_class=EarnedSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]
    def get_queryset(self):
        return Earned.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

