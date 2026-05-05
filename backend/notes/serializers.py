from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    last_edited_display = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "date",
            "content",
            "created_at",
            "updated_at",
            "last_edited_at",
            "last_edited_display",
        ]
        read_only_fields = ["created_at", "updated_at", "last_edited_at", "last_edited_display"]

    def get_last_edited_display(self, obj):
        return obj.last_edited_at.isoformat() if obj.last_edited_at else "---"

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Note content cannot be empty.")
        return value.strip()

    def create(self, validated_data):
        request = self.context["request"]
        note, created = Note.objects.get_or_create(
            user=request.user,
            date=validated_data["date"],
            defaults={"content": validated_data["content"]},
        )
        if not created:
            note.content = validated_data["content"]
            note.save()
        return note
