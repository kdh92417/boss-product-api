import phonenumbers
from rest_framework import serializers

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
