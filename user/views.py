from rest_framework.response import Response
import random
from rest_framework.decorators import api_view
from .serializer import UserSerializer, LoginSerializer
from walletApp.serializer import AccountSerializer
from user.models import User
from walletApp.models import Account
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


def generate_account_number():
    return random.randint(2004, 5000)


@swagger_auto_schema(method="post", request_body=UserSerializer, responses={"200": 'Success'},
                     operation_id="user signup", )
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # user signup login it will create user from this API
    try:
        serializer = UserSerializer(data=request.data)
        # username = serializer.validated_data('username')
        # password = serializer.validated_data('password')
        # if not username and not password:
        #     return Response({'msg': 'Username and Password required'})
        # if User.objects.filter(username=username).exists():
        #     return Response({'msg': 'username taken'})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({'msg': 'username taken'})
            else:
                user = serializer.save()
                user.save()
                Account.objects.create(user=user, account_no=generate_account_number(), balance=0.00)
                return Response("Data created")
        else:
            return Response(serializer.errors)
    except Exception:
        return Response("An error occurred while signing up.")


# only use serializer here in request body and response
@swagger_auto_schema(method="post", request_body=LoginSerializer,
                     responses={"200": 'Success'}, operation_id="user Login", )
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # user can sign_in through this API
    # try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user_obj = User.objects.get(username=username, password=password)
                refresh = RefreshToken.for_user(user_obj)
                return Response({'msg': 'Logged In', 'refresh': str(refresh), 'access': str(refresh.access_token)})
            except Exception:
                return Response({'msg': 'Username or Password is Incorrect'})
        # else:
        return Response(serializer.errors)
    # except Exception:
    #     return Response({'msg': 'Username does not exist. Please Signup'})
