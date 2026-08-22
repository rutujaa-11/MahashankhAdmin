from django.db import models
from django.utils import timezone


# ============================================================
# LOCATIONS
# ============================================================

class Country(models.Model):

    TYPE_CHOICES = [
        ("Producer", "Producer"),
        ("Consumer", "Consumer"),
        ("Producer, Consumer", "Producer, Consumer"),
    ]

    country = models.CharField(
        max_length=100,
        default=""
    )

    continent = models.CharField(
        max_length=100,
        default=""
    )

    ranking = models.PositiveIntegerField(
        default=0
    )

    country_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default="Consumer"
    )

    products = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.country

    class Meta:
        ordering = ["ranking"]


class State(models.Model):

    name = models.CharField(
        max_length=100,
        default=""
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states",
        null=True,
        blank=True
    )

    slug = models.SlugField(
        max_length=120,
        blank=True,
        default=""
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(models.Model):

    name = models.CharField(
        max_length=100,
        default=""
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="cities",
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        null=True,
        blank=True
    )

    coordinates = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    areas = models.PositiveIntegerField(
        default=0
    )

    tile_hub = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class AreaVillage(models.Model):

    TYPE_CHOICES = [
        ("Area", "Area"),
        ("Village", "Village"),
    ]

    name = models.CharField(
        max_length=150,
        default=""
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="area_villages",
        null=True,
        blank=True
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="area_villages",
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="area_villages",
        null=True,
        blank=True
    )

    area_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="Area"
    )

    pincode = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    showrooms = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# ============================================================
# WALLPAPERS
# ============================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        default=""
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Wallpaper(models.Model):

    title = models.CharField(
        max_length=200,
        default=""
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    downloads = models.IntegerField(
        default=0
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    image = models.ImageField(
        upload_to="wallpapers/",
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-uploaded_at"]


# ============================================================
# USERS
# ============================================================

class UserProfile(models.Model):

    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    created = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.full_name or self.user.username


class UserActivityLog(models.Model):

    username = models.CharField(
        max_length=150,
        default=""
    )

    action = models.CharField(
        max_length=255,
        default=""
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.action}"

    class Meta:
        ordering = ["-timestamp"]


class PermissionRecord(models.Model):

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="permission_records"
    )

    can_manage_users = models.BooleanField(
        default=False
    )

    can_manage_wallpapers = models.BooleanField(
        default=False
    )

    can_manage_ai = models.BooleanField(
        default=False
    )

    can_manage_orders = models.BooleanField(
        default=False
    )

    can_view_analytics = models.BooleanField(
        default=False
    )

    created = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.user.username} Permissions"


# ============================================================
# AI WALLPAPER GENERATOR
# ============================================================

class AIWallpaperStyle(models.Model):

    title = models.CharField(
        max_length=100,
        default=""
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]


class AIWallpaperGeneration(models.Model):

    ASPECT_RATIO_CHOICES = [
        ("Square", "Square"),
        ("Landscape", "Landscape"),
        ("Portrait", "Portrait"),
    ]

    user = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    style = models.ForeignKey(
        AIWallpaperStyle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generations"
    )

    prompt = models.TextField(
        blank=True,
        default=""
    )

    negative_prompt = models.TextField(
        blank=True,
        default=""
    )

    aspect_ratio = models.CharField(
        max_length=20,
        choices=ASPECT_RATIO_CHOICES,
        default="Square"
    )

    generated_image = models.ImageField(
        upload_to="ai_wallpapers/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        default="Completed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.prompt[:30]}"

    class Meta:
        ordering = ["-created_at"]


class ChatSession(models.Model):

    user = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    session_id = models.CharField(
        max_length=150,
        default=""
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.session_id

    class Meta:
        ordering = ["-started_at"]


class ChatbotLog(models.Model):

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="logs",
        null=True,
        blank=True
    )

    user = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    message = models.TextField(
        blank=True,
        default=""
    )

    response = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message[:50]

    class Meta:
        ordering = ["-created_at"]


# ============================================================
# COMMERCE
# ============================================================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    order_number = models.CharField(
        max_length=100,
        unique=True,
        default=""
    )

    user = models.CharField(
        max_length=150,
        default=""
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.order_number

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.CharField(
        max_length=200,
        default=""
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.product} - {self.order.order_number}"


class Payment(models.Model):

    PAYMENT_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_id = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default="Pending"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.payment_id or f"Payment {self.id}"


class ProfitLoss(models.Model):

    date = models.DateField(
        default=timezone.now
    )

    revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    expense = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ["-date"]


# ============================================================
# SYSTEM
# ============================================================

class Notification(models.Model):

    title = models.CharField(
        max_length=200,
        default=""
    )

    message = models.TextField(
        blank=True,
        default=""
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class AdminSetting(models.Model):

    setting_name = models.CharField(
        max_length=150,
        unique=True,
        default=""
    )

    setting_value = models.TextField(
        blank=True,
        default=""
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.setting_name