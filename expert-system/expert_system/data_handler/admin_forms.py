from data_handler.models import Request
from django import forms
from django.core.exceptions import ValidationError


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = "__all__"

    def clean_request(self):
        request = self.cleaned_data.get("request")
        if Request.objects.filter(request__iexact=request.lower()).exists():
            raise ValidationError("Такой запрос уже существует")
        return request
