from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    Country,
    State,
    City,
    AreaVillage,
    Category,
    Wallpaper,
    UserProfile,
    UserActivityLog,
    PermissionRecord,
    AIWallpaperStyle,
    AIWallpaperGeneration,
    ChatSession,
    ChatbotLog,
    Order,
    OrderItem,
    Payment,
    ProfitLoss,
    Notification,
    AdminSetting,
)


# ============================================================
# LOCATIONS
# ============================================================

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "country",
        "continent",
        "ranking",
        "country_type",
        "products",
        "state_count",
    )
    search_fields = ("country", "continent")
    list_filter = ("continent", "country_type")
    ordering = ("ranking",)

    def state_count(self, obj):
        return obj.states.count()

    state_count.short_description = "States"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "country",
        "city_count",
        "slug",
    )
    search_fields = (
        "name",
        "country__country",
        "slug",
    )
    list_filter = ("country",)
    ordering = ("name",)

    def city_count(self, obj):
        return obj.cities.count()

    city_count.short_description = "Cities"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "state",
        "country",
        "coordinates",
        "area_count",
        "tile_hub",
    )
    search_fields = (
        "name",
        "state__name",
        "country__country",
    )
    list_filter = (
        "country",
        "state",
        "tile_hub",
    )
    ordering = ("name",)

    def area_count(self, obj):
        return obj.area_villages.count()

    area_count.short_description = "Areas"


@admin.register(AreaVillage)
class AreaVillageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "city",
        "state",
        "country",
        "area_type",
        "pincode",
        "showrooms",
    )
    search_fields = (
        "name",
        "city__name",
        "state__name",
        "country__country",
        "pincode",
    )
    list_filter = (
        "country",
        "state",
        "city",
        "area_type",
    )
    ordering = ("name",)


# ============================================================
# WALLPAPERS
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "preview",
        "title",
        "category",
        "downloads",
        "country",
        "uploaded_at",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "category",
        "country",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "country",
        "category__name",
    )

    ordering = ("-uploaded_at",)

    readonly_fields = (
        "uploaded_at",
        "admin_image_preview",
    )

    fields = (
        "title",
        "category",
        "downloads",
        "country",
        "image",
        "admin_image_preview",
        "uploaded_at",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" '
                'style="width:60px;height:60px;'
                'object-fit:cover;border-radius:5px;" />',
                obj.image.url
            )
        return "No Image"

    preview.short_description = "Image"

    def admin_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" '
                'style="max-width:300px;'
                'max-height:300px;'
                'object-fit:contain;" />',
                obj.image.url
            )
        return "No Image"

    admin_image_preview.short_description = "Image Preview"


# ============================================================
# USERS
# ============================================================

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "date_joined",
        "last_login",
        "order_count",
        "generated_wallpaper_count",
        "role",
    )

    list_display_links = (
        "id",
        "username",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-date_joined",)

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    def order_count(self, obj):
        return Order.objects.filter(
            user=obj.username
        ).count()

    order_count.short_description = "Orders"

    def generated_wallpaper_count(self, obj):
        return AIWallpaperGeneration.objects.filter(
            user=obj.username
        ).count()

    generated_wallpaper_count.short_description = "AI Wallpapers"

    def role(self, obj):
        if obj.is_superuser:
            return "Super Admin"

        if obj.is_staff:
            return "Admin"

        return "User"

    role.short_description = "Role"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "phone",
        "country",
        "city",
        "created",
    )

    list_display_links = (
        "id",
        "full_name",
    )

    search_fields = (
        "full_name",
        "phone",
        "country",
        "city",
        "user__username",
        "user__email",
    )

    list_filter = (
        "country",
        "city",
        "created",
    )

    ordering = ("-created",)


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "action",
        "ip_address",
        "timestamp",
    )

    list_display_links = (
        "id",
        "username",
    )

    search_fields = (
        "username",
        "action",
        "ip_address",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    ordering = ("-timestamp",)


@admin.register(PermissionRecord)
class PermissionRecordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "can_manage_users",
        "can_manage_wallpapers",
        "can_manage_ai",
        "can_manage_orders",
        "can_view_analytics",
        "created",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "can_manage_users",
        "can_manage_wallpapers",
        "can_manage_ai",
        "can_manage_orders",
        "can_view_analytics",
    )


# ============================================================
# AI WALLPAPER GENERATOR
# ============================================================

@admin.register(AIWallpaperStyle)
class AIWallpaperStyleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "icon",
        "title",
        "description",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "is_active",
    )

    ordering = ("id",)


@admin.register(AIWallpaperGeneration)
class AIWallpaperGenerationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "image_preview",
        "user",
        "style",
        "aspect_ratio",
        "status",
        "created_at",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = (
        "style",
        "aspect_ratio",
        "status",
        "created_at",
    )

    search_fields = (
        "user",
        "prompt",
        "negative_prompt",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "preview_large",
        "created_at",
    )

    fields = (
        "user",
        "style",
        "prompt",
        "negative_prompt",
        "aspect_ratio",
        "generated_image",
        "preview_large",
        "status",
        "created_at",
    )

    def image_preview(self, obj):
        if obj.generated_image:
            try:
                return format_html(
                    '<img src="{}" '
                    'style="width:60px;height:60px;'
                    'object-fit:cover;'
                    'border-radius:5px;'
                    'border:1px solid #ccc;" />',
                    obj.generated_image.url
                )
            except ValueError:
                pass

        return "No Image"

    image_preview.short_description = "Image"

    def preview_large(self, obj):
        if obj.generated_image:
            try:
                return format_html(
                    '<img src="{}" '
                    'style="max-width:300px;'
                    'max-height:300px;'
                    'object-fit:contain;'
                    'border-radius:6px;'
                    'border:1px solid #ccc;" />',
                    obj.generated_image.url
                )
            except ValueError:
                pass

        return "No Image"

    preview_large.short_description = "Image Preview"


# ============================================================
# CHAT
# ============================================================

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "session_id",
        "user",
        "started_at",
        "ended_at",
    )

    search_fields = (
        "session_id",
        "user",
    )

    list_filter = (
        "started_at",
    )

    ordering = ("-started_at",)


@admin.register(ChatbotLog)
class ChatbotLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "session",
        "user",
        "message_short",
        "created_at",
    )

    search_fields = (
        "user",
        "message",
        "response",
    )

    list_filter = (
        "created_at",
    )

    ordering = ("-created_at",)

    def message_short(self, obj):
        return obj.message[:60] if obj.message else ""

    message_short.short_description = "Message"


# ============================================================
# COMMERCE
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order_number",
        "user",
        "total_amount",
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user",
    )

    list_filter = (
        "status",
        "created_at",
    )

    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "product",
        "order__order_number",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "payment_id",
        "amount",
        "status",
        "paid_at",
    )

    search_fields = (
        "payment_id",
        "order__order_number",
    )

    list_filter = (
        "status",
        "paid_at",
    )


@admin.register(ProfitLoss)
class ProfitLossAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "date",
        "revenue",
        "expense",
        "profit",
    )

    list_filter = (
        "date",
    )

    ordering = ("-date",)


# ============================================================
# SYSTEM
# ============================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    ordering = ("-created_at",)


@admin.register(AdminSetting)
class AdminSettingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "setting_name",
        "setting_value",
        "updated_at",
    )

    search_fields = (
        "setting_name",
        "setting_value",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = ("setting_name",)