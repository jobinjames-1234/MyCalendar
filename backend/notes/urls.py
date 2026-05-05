from django.urls import path

from .views import NoteByDateView, NoteDetailView, NoteListCreateView

urlpatterns = [
    path("", NoteListCreateView.as_view(), name="notes-list-create"),
    path("by-date/", NoteByDateView.as_view(), name="note-by-date"),
    path("<int:pk>/", NoteDetailView.as_view(), name="notes-detail"),
]
