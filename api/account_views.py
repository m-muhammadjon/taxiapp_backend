import json
import random
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from taxi.models import SMSToken

from .account_serializer import UserSerializer, UserUpdateSerializer, UserPasswordUpdateSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    print(user, email, password)
    status = 'error'
    token = ''
    if user is not None:
        if user.is_verified:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            status = 'ok'
        else:
            status = 'not verified'
    res = {
        'token': token,
        'status': status
    }
    return Response(res)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    # email = request.data.get('email') != ''
    serializer = UserUpdateSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        # if email:
        #     Verification.objects.get_or_create(user=request.user)
        #     email_sender(user.id)
        #     user.is_verified = False
        #     user.save()
        #     return Response({'message': 'We Will Send verification to your New Email'}, status=status.HTTP_200_OK)
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UserPasswordUpdateSerializer(data=request.data)
    if serializer.is_valid():
        old_password = request.data.get('old_password')
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')
        match_password = check_password(old_password, request.user.password)
        if match_password:
            if password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                return Response({'status': 'ok', 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Passwords don\'t match'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    print(serializer.errors)
    return Response({'status': 'error', 'message': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)


def sms_code_send(num):
    url = "http://notify.eskiz.uz/api/message/sms/send"
    code = random.randint(1000, 9999)
    payload = {'mobile_phone': f"{num}",
               'message': f'Tasdiqlash kodi {code}',
               'from': '4546'}
    headers = {
        'Authorization': f'Bearer {SMSToken.objects.first().token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code, code


@api_view(['POST'])
def send_code(request):
    st_code, code = sms_code_send(request.data.get('phone_number'))
    print(st_code)
    while not st_code == 200:
        print('while')
        url = "http://notify.eskiz.uz/api/auth/login"

        payload = {'email': 'test@eskiz.uz',
                   'password': 'j6DWtQjjpLDNjWEk74Sx'}

        response = requests.request("POST", url, data=payload)
        token = json.loads(response.text)['data']['token']
        token_obj = SMSToken.objects.first()
        token_obj.token = token
        token_obj.save()

        st_code, code = sms_code_send(request.data.get('phone_number'))
    return Response({'code': code})
