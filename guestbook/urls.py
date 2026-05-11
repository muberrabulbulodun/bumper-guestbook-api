from django.urls import path
from .views import CreateEntryView, EntryListView, UserDataView

urlpatterns = [
    path("entries/", EntryListView.as_view()),
    path("entries/create/", CreateEntryView.as_view()),
    path("users/", UserDataView.as_view()),
]
