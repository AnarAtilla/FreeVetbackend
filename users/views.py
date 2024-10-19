from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Profile
from .serializers import RegisterSerializer, LoginSerializer, SMSVerificationSerializer
from .utils import send_sms
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView

def custom_login_redirect(request):
    redirect_url = request.session.get('redirect_url', '/default-url')
    return redirect(redirect_url)

def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/users/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)

def facebook_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/users/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer  # Указываем сериализатор

    def post(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None  # Пропускаем выполнение кода при генерации Swagger

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            photo = request.FILES.get('photo', None)
            profile = Profile.objects.create(
                name=serializer.validated_data['name'],
                phone=serializer.validated_data['phone'],
                photo=photo
            )
            profile.generate_sms_code()
            send_sms(profile.phone, f"Your code is {profile.sms_code}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None  # Пропускаем выполнение кода при генерации Swagger

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            profile = Profile.objects.get(phone=phone_number)
            profile.generate_sms_code()
            send_sms(phone_number, f"Your code is {profile.sms_code}")

            if profile.user is None:
                user = User.objects.create(username=profile.phone)
                profile.user = user
                profile.save()

            refresh = RefreshToken.for_user(profile.user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Logged in"
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class VerifyCodeView(generics.GenericAPIView):
    serializer_class = SMSVerificationSerializer

    def post(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None  # Пропускаем выполнение кода при генерации Swagger

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            profile = Profile.objects.get(phone=phone_number, sms_code=code)

            if profile.code_sent_time < timezone.now() - timedelta(seconds=90):
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

            profile.last_login_time = timezone.now()

            if profile.user is None:
                user = User.objects.create(username=profile.phone)
                profile.user = user
                profile.save()

            refresh = RefreshToken.for_user(profile.user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Logged in"
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
