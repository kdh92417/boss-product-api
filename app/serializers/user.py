import phonenumbers
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import User


class SignupSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label="핸드폰 번호", write_only=True)
    password = serializers.CharField(write_only=True)

    def save(self):
        phone_number = self.validated_data.get("phone_number")
        password = self.validated_data.get("password")

        user = User.objects.create_user(phone_number=phone_number, password=password)
        return user

    def validate_phone_number(self, phone_number):
        parsed_phone_number = phonenumbers.parse(phone_number, "KR")
        if not phonenumbers.is_valid_number(parsed_phone_number):
            raise serializers.ValidationError(detail="전화번호 형식이 올바르지 않습니다.")

        return phone_number


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label="핸드폰 번호", write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        user = User.objects.filter(phone_number=phone_number).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError(detail="아이디 또는 비밀번호가 올바르지 않습니다.")

        token = TokenObtainPairSerializer.get_token(user)
        attrs["token"] = token

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data.get("refresh_token").blacklist())

        except TokenError as ex:
            raise AuthenticationFailed(ex)
