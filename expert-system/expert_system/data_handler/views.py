from api.serializers import ButtonSerializer, ButtonSlugSerializer, RequestSerializer, TextSerializer, UserSerializer
from data_handler.models import ButtonSlug, ButtonUrl, Request, TelegarmUser, Text
from django.http import Http404
from expert_system.utils import find_closest_request
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class TextView(generics.RetrieveAPIView):
    queryset = Text.objects.prefetch_related("button_slug")
    serializer_class = TextSerializer


class TextSlug(TextView):
    lookup_field = "slug"


class Buttons(generics.ListAPIView):
    def get_queryset(self):
        return dict(
            ButtonSlug=ButtonSlug.objects.all().prefetch_related("slug"),
            ButtonUrl=ButtonUrl.objects.all(),
        )

    def get(self, request):
        serializer = ButtonSerializer(self.get_queryset())
        return Response(serializer.data)


class Button(generics.RetrieveAPIView):
    queryset = ButtonSlug.objects.all()
    serializer_class = ButtonSlugSerializer


class ButtonBySlug(generics.RetrieveAPIView):
    queryset = ButtonSlug.objects.all()
    serializer_class = ButtonSlugSerializer

    def get_object(self):
        slug = self.kwargs.get("slug")
        text_instance = Text.objects.get(slug=slug)
        return self.queryset.get(slug=text_instance)


class RequestList(generics.ListCreateAPIView):
    queryset = Request.objects.all().prefetch_related("requestuser")
    serializer_class = RequestSerializer


class RequestRetrieve(generics.RetrieveAPIView):
    lookup_field = "request"
    queryset = Request.objects.select_related("text")
    serializer_class = RequestSerializer

    def get_object(self):
        user_request = self.kwargs.get("name", "")
        obj = find_closest_request(user_request)

        if obj is None:
            raise Http404("No closest request found for the provided input.")

        self.check_object_permissions(self.request, obj)
        return obj


class RequestPatch(generics.UpdateAPIView):
    queryset = Request.objects.select_related("text")
    serializer_class = RequestSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter = {field: self.kwargs["request_id"] for field in [self.lookup_field]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, *args, **kwargs):
        request_ = self.get_object()
        request_.counter += 1
        request_.save()
        serializer = RequestSerializer(request_)
        return Response(serializer.data)


class UserList(generics.ListCreateAPIView):
    queryset = TelegarmUser.objects.all()
    serializer_class = UserSerializer


class User(generics.RetrieveUpdateAPIView):
    lookup_field = "user_id"
    queryset = TelegarmUser.objects.prefetch_related("requests")
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data["requests"]
        print(data)
        user.requests.add(data)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
