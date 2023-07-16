from data_handler.models import ButtonSlug, ButtonUrl, Request, TelegarmUser, Text, TextButtonSlug, TextButtonUrl
from rest_framework import serializers


class ButtonSlugSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = ButtonSlug
        fields = ("id", "cover_text", "slug")


class ButtonUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonUrl
        fields = ("id", "cover_text", "url")


class ButtonSerializer(serializers.Serializer):
    ButtonSlug = ButtonSlugSerializer(many=True)
    ButtonUrl = ButtonUrlSerializer(many=True)


class TextButtonSlugSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="button.id")
    cover_text = serializers.ReadOnlyField(source="button.cover_text")
    slug = serializers.SlugRelatedField(source="button.slug", slug_field="slug", read_only=True)

    class Meta:
        model = TextButtonSlug
        fields = ("id", "cover_text", "slug", "order")


class TextButtonUrlSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="button.id")
    cover_text = serializers.ReadOnlyField(source="button.cover_text")
    url = serializers.ReadOnlyField(source="button.url")

    class Meta:
        model = TextButtonUrl
        fields = ("id", "cover_text", "url", "order")


class TextSerializer(serializers.ModelSerializer):
    button_slug = TextButtonSlugSerializer(
        source="buttonslug_list.all",
        many=True,
    )
    button_url = TextButtonUrlSerializer(
        source="buttonurl_list.all",
        many=True,
    )

    class Meta:
        model = Text
        fields = "__all__"


class RequestSerializer(serializers.ModelSerializer):
    text = TextSerializer(required=False)

    class Meta:
        model = Request
        fields = ("id", "text", "request", "processing_status", "counter", "created_at", "requestuser")

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if Request.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegarmUser
        fields = "__all__"

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            return attrs
        if TelegarmUser.objects.filter(**attrs).exists():
            raise serializers.ValidationError("This object already exists")
        return attrs
