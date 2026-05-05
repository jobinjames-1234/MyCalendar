from datetime import date

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        if year and month:
            queryset = queryset.filter(date__year=year, date__month=month)
        return queryset.order_by("date")

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        return Response({"message": "Note saved successfully.", "note": NoteSerializer(note).data}, status=201)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        return Response({"message": "Note updated successfully.", "note": NoteSerializer(note).data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Note deleted successfully."}, status=status.HTTP_200_OK)


class NoteByDateView(APIView):
    def get(self, request):
        target_date = request.query_params.get("date")
        if not target_date:
            return Response({"message": "date query param is required (YYYY-MM-DD)."}, status=400)
        try:
            parsed = date.fromisoformat(target_date)
        except ValueError:
            return Response({"message": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        note = Note.objects.filter(user=request.user, date=parsed).first()
        return Response({"note": NoteSerializer(note).data if note else None})
