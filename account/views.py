from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone
from datetime import timedelta

from .models import MyUser, Tasqidlash
from .serializers import MyUserSerializer, PhoneNumberSerializer, TasdiqlashSerializer
from .utils import generate_verification_code


class SentCodeToPhoneNumberView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = generate_verification_code()
            expires_at = timezone.now() + timedelta(minutes=5)
            Tasqidlash.objects.create(code=code,
                                    phone_number = phone_number,
                                    expires_at = expires_at
                                    )
            # send code to phone_number / eskiz.uz
            return Response({'message': 'Tasdiqlash kodi yuborildi :)'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = TasdiqlashSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            tasdiqlash = Tasqidlash.objects.filter(phone_number=phone_number,
                                                   code=code,
                                                   expires_at__gt=timezone.now()
                                                   ).first()
            if tasdiqlash:
                tasdiqlash.delete()
                user, created = MyUser.objects.get_or_create(phone_number=phone_number)
                if created:
                    refresh = RefreshToken.for_user(user)
                    user.refresh = str(refresh)
                    user.access = str(refresh.access_token)
                    user.save()
                serializer = MyUserSerializer(user)
                return Response({
                    'refresh': user.refresh,
                    'access': user.access,
                })
            else:
                return Response({'message': 'Tasdiqlash kodi xato'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
