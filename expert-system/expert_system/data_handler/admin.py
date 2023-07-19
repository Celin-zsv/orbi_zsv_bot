from data_handler.admin_forms import RequestForm
from data_handler.models import (
    ButtonSlug,
    ButtonUrl,
    Request,
    TelegarmUser,
    Text,
    TextButtonSlug,
    TextButtonUrl,
    UserRequest,
)
from django.contrib import admin


class TextInlineSlug(admin.TabularInline):
    model = TextButtonSlug


class TextInlineUrl(admin.TabularInline):
    model = TextButtonUrl


class TelegarmUserInline(admin.TabularInline):
    model = UserRequest
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class RequestAdmin(admin.ModelAdmin):
    form = RequestForm
    list_display = (
        "pk",
        "request",
        "processing_status",
        "text",
        "counter",
        "created_at",
    )
    search_fields = ("request",)
    list_filter = ("processing_status", "text")
    empty_value_display = "-пусто-"
    readonly_fields = ["counter", "created_at"]
    exclude = ("tsv",)
    list_display_links = ("request",)

    def get_readonly_fields(self, request, obj=None):
        if obj and UserRequest.objects.filter(request_id=obj.id).exists():
            return ["request"] + self.readonly_fields
        return self.readonly_fields


class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "text_header", "text", "is_published")
    prepopulated_fields = {"slug": ("text_header",)}
    search_fields = ("text_header",)
    list_filter = ("text_header",)
    empty_value_display = "-пусто-"
    inlines = (TextInlineSlug, TextInlineUrl)
    list_display_links = ("text_header",)

    def has_delete_permission(self, request, obj=None):
        return False


class ButtonSlugAdmin(admin.ModelAdmin):
    list_display = ("pk", "cover_text", "slug")
    search_fields = ("cover_text", "slug")
    list_filter = ("cover_text",)
    empty_value_display = "-пусто-"
    list_display_links = ("cover_text",)


class ButtonUrlAdmin(admin.ModelAdmin):
    list_display = ("pk", "cover_text", "url")
    search_fields = ("cover_text", "url")
    list_filter = ("cover_text",)
    empty_value_display = "-пусто-"
    list_display_links = ("cover_text",)


class TelegarmUserAdmin(admin.ModelAdmin):
    list_display = ("pk", "user_id")
    search_fields = ("user_id",)
    list_filter = ("user_id",)
    empty_value_display = "-пусто-"
    inlines = (TelegarmUserInline,)
    list_display_links = ("user_id",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Request, RequestAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(ButtonSlug, ButtonSlugAdmin)
admin.site.register(ButtonUrl, ButtonUrlAdmin)
admin.site.register(TelegarmUser, TelegarmUserAdmin)
