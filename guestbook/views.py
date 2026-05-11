from django.db.models import Count, OuterRef, Subquery, Value, CharField
from django.db.models.functions import Concat, Cast

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Entry, User
from .pagination import EntryPagination
from .serializers import CreateEntrySerializer, EntrySerializer, UserDataSerializer


# Create a new guestbook entry and create user if not exists.
class CreateEntryView(APIView):

    def post(self, request):
        serializer = CreateEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        subject = serializer.validated_data["subject"]
        message = serializer.validated_data["message"]

        user, _ = User.objects.get_or_create(name=name)

        entry = Entry.objects.create(
            user=user,
            subject=subject,
            message=message,
        )

        return Response(
            {"id": entry.id, "message": "Entry created successfully."},
            status=status.HTTP_201_CREATED,
        )


# Return paginated guestbook entries ordered by latest created date.
class EntryListView(generics.ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = EntryPagination
    queryset = Entry.objects.select_related("user").order_by("-created_date")


# Return aggregated user data without pagination.
class UserDataView(APIView):

    def get(self, request):
        latest_entry = Entry.objects.filter(user=OuterRef("pk")).order_by(
            "-created_date"
        )
        # Annotate users with total message count and latest entry information.
        users = User.objects.annotate(
            total_messages=Count("entries"),
            last_entry=Concat(
                Subquery(latest_entry.values("subject")[:1]),
                Value(" | "),
                Cast(
                    Subquery(latest_entry.values("message")[:1]),
                    output_field=CharField(),
                ),
                output_field=CharField(),
            ),
        )

        data = [
            {
                "username": user.name,
                "total_messages": user.total_messages,
                "last_entry": user.last_entry,
            }
            for user in users
        ]

        serializer = UserDataSerializer(data, many=True)

        return Response({"users": serializer.data})
