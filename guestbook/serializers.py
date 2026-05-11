from rest_framework import serializers
from .models import Entry, User


class CreateEntrySerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255, allow_blank=False, trim_whitespace=True
    )
    subject = serializers.CharField(
        max_length=255, allow_blank=False, trim_whitespace=True
    )
    message = serializers.CharField(allow_blank=False, trim_whitespace=True)

    def validate_name(self, value):
        return value.strip()

    def validate_subject(self, value):
        return value.strip()

    def validate_message(self, value):
        return value.strip()


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")

    class Meta:
        model = Entry
        fields = ["user", "subject", "message"]


class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    total_messages = serializers.IntegerField()
    last_entry = serializers.CharField()
