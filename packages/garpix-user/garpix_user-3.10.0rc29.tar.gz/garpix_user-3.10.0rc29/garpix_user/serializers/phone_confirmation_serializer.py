from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=False)


class PhonePreConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class PhoneConfirmCheckCodeSerializer(serializers.Serializer):
    phone_confirmation_code = serializers.CharField(max_length=15)
