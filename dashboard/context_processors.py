from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import (
    Wallpaper,
    Category,
    UserProfile,
    UserActivityLog,
    AIWallpaperStyle,
    AIWallpaperGeneration,
    ChatSession,
    ChatbotLog,
    Order,
    Payment,
    ProfitLoss,
    Country,
)


def admin_dashboard_data(request):
    """
    Dynamic data provider for the main Django/Jazzmin admin dashboard.
    Existing admin functionality is not changed.
    """

    # ============================================================
    # BASIC COUNTS
    # ============================================================

    total_users = User.objects.count()

    active_users = User.objects.filter(
        is_active=True
    ).count()

    total_wallpapers = Wallpaper.objects.count()

    total_categories = Category.objects.count()

    total_ai_styles = AIWallpaperStyle.objects.count()

    total_ai_generations = AIWallpaperGeneration.objects.count()

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()

    completed_orders = Order.objects.filter(
        status="Completed"
    ).count()

    total_countries = Country.objects.count()

    unread_notifications = 0

    # ============================================================
    # REVENUE
    # ============================================================

    total_revenue = (
        Payment.objects
        .filter(status="Paid")
        .aggregate(total=Sum("amount"))
        .get("total")
        or 0
    )

    total_expense = (
        ProfitLoss.objects
        .aggregate(total=Sum("expense"))
        .get("total")
        or 0
    )

    total_profit = (
        ProfitLoss.objects
        .aggregate(total=Sum("profit"))
        .get("total")
        or 0
    )

    # ============================================================
    # MONTHLY GROWTH
    # ============================================================

    today = timezone.localdate()

    monthly_wallpapers = (
        Wallpaper.objects
        .filter(uploaded_at__date__lte=today)
        .annotate(month=TruncMonth("uploaded_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    monthly_orders = (
        Order.objects
        .filter(created_at__date__lte=today)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    monthly_ai = (
        AIWallpaperGeneration.objects
        .filter(created_at__date__lte=today)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    monthly_users = (
        User.objects
        .filter(date_joined__date__lte=today)
        .annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    # ============================================================
    # BUILD LAST 7 MONTHS
    # ============================================================

    months = []

    year = today.year
    month = today.month

    for _ in range(7):

        months.append((year, month))

        month -= 1

        if month == 0:
            month = 12
            year -= 1

    months.reverse()

    wallpaper_month_map = {
        (
            item["month"].year,
            item["month"].month,
        ): item["total"]
        for item in monthly_wallpapers
        if item["month"]
    }

    order_month_map = {
        (
            item["month"].year,
            item["month"].month,
        ): item["total"]
        for item in monthly_orders
        if item["month"]
    }

    ai_month_map = {
        (
            item["month"].year,
            item["month"].month,
        ): item["total"]
        for item in monthly_ai
        if item["month"]
    }

    user_month_map = {
        (
            item["month"].year,
            item["month"].month,
        ): item["total"]
        for item in monthly_users
        if item["month"]
    }

    growth_labels = []

    wallpaper_growth = []

    order_growth = []

    ai_growth = []

    user_growth = []

    for year_value, month_value in months:

        month_name = timezone.datetime(
            year_value,
            month_value,
            1
        ).strftime("%b")

        growth_labels.append(month_name)

        wallpaper_growth.append(
            wallpaper_month_map.get(
                (year_value, month_value),
                0
            )
        )

        order_growth.append(
            order_month_map.get(
                (year_value, month_value),
                0
            )
        )

        ai_growth.append(
            ai_month_map.get(
                (year_value, month_value),
                0
            )
        )

        user_growth.append(
            user_month_map.get(
                (year_value, month_value),
                0
            )
        )

    # ============================================================
    # CATEGORY ANALYTICS
    # ============================================================

    category_rows = (
        Category.objects
        .annotate(
            wallpaper_total=Count("wallpaper")
        )
        .order_by("-wallpaper_total", "name")
    )

    category_labels = [
        item.name
        for item in category_rows
    ]

    category_values = [
        item.wallpaper_total
        for item in category_rows
    ]

    # ============================================================
    # COUNTRY ANALYTICS
    # ============================================================

    wallpaper_country_rows = (
        Wallpaper.objects
        .exclude(country="")
        .values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    wallpaper_country_labels = [
        item["country"]
        for item in wallpaper_country_rows
    ]

    wallpaper_country_values = [
        item["total"]
        for item in wallpaper_country_rows
    ]

    # ============================================================
    # USER COUNTRY ANALYTICS
    # ============================================================

    user_country_rows = (
        UserProfile.objects
        .exclude(country="")
        .values("country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    user_country_labels = [
        item["country"]
        for item in user_country_rows
    ]

    user_country_values = [
        item["total"]
        for item in user_country_rows
    ]

    # ============================================================
    # TOP COUNTRIES
    # ============================================================

    top_countries = []

    country_names = set(
        wallpaper_country_labels
        + user_country_labels
    )

    for country_name in country_names:

        wallpaper_count = (
            Wallpaper.objects
            .filter(country=country_name)
            .count()
        )

        user_count = (
            UserProfile.objects
            .filter(country=country_name)
            .count()
        )

        top_countries.append(
            {
                "name": country_name,
                "wallpapers": wallpaper_count,
                "users": user_count,
                "total": wallpaper_count + user_count,
            }
        )

    top_countries = sorted(
        top_countries,
        key=lambda x: x["total"],
        reverse=True
    )[:8]

    # ============================================================
    # RECENT WALLPAPERS
    # ============================================================

    recent_wallpapers = (
        Wallpaper.objects
        .select_related("category")
        .order_by("-uploaded_at")[:6]
    )

    # ============================================================
    # RECENT AI ACTIVITY
    # ============================================================

    recent_ai = (
        AIWallpaperGeneration.objects
        .order_by("-created_at")[:6]
    )

    # ============================================================
    # RECENT USER ACTIVITY
    # ============================================================

    recent_activity = (
        UserActivityLog.objects
        .order_by("-timestamp")[:6]
    )

    # ============================================================
    # RECENT ORDERS
    # ============================================================

    recent_orders = (
        Order.objects
        .order_by("-created_at")[:6]
    )

    # ============================================================
    # PROFIT / LOSS DATA
    # ============================================================

    profit_loss_rows = (
        ProfitLoss.objects
        .order_by("date")[:12]
    )

    profit_labels = [
        item.date.strftime("%d %b")
        for item in profit_loss_rows
    ]

    revenue_values = [
        float(item.revenue)
        for item in profit_loss_rows
    ]

    expense_values = [
        float(item.expense)
        for item in profit_loss_rows
    ]

    profit_values = [
        float(item.profit)
        for item in profit_loss_rows
    ]

    # ============================================================
    # ORDER STATUS
    # ============================================================

    order_status_labels = [
        "Pending",
        "Processing",
        "Completed",
        "Cancelled",
    ]

    order_status_values = [
        Order.objects.filter(status=status).count()
        for status in order_status_labels
    ]

    # ============================================================
    # PAYMENT STATUS
    # ============================================================

    payment_status_labels = [
        "Pending",
        "Paid",
        "Failed",
        "Refunded",
    ]

    payment_status_values = [
        Payment.objects.filter(status=status).count()
        for status in payment_status_labels
    ]

    # ============================================================
    # DASHBOARD CONTEXT
    # ============================================================

    return {

        "dashboard_total_users":
            total_users,

        "dashboard_active_users":
            active_users,

        "dashboard_total_wallpapers":
            total_wallpapers,

        "dashboard_total_categories":
            total_categories,

        "dashboard_total_ai_styles":
            total_ai_styles,

        "dashboard_total_ai":
            total_ai_generations,

        "dashboard_total_orders":
            total_orders,

        "dashboard_pending_orders":
            pending_orders,

        "dashboard_completed_orders":
            completed_orders,

        "dashboard_total_countries":
            total_countries,

        "dashboard_total_revenue":
            total_revenue,

        "dashboard_total_expense":
            total_expense,

        "dashboard_total_profit":
            total_profit,

        "growth_labels":
            growth_labels,

        "wallpaper_growth":
            wallpaper_growth,

        "order_growth":
            order_growth,

        "ai_growth":
            ai_growth,

        "user_growth":
            user_growth,

        "category_labels":
            category_labels,

        "category_values":
            category_values,

        "wallpaper_country_labels":
            wallpaper_country_labels,

        "wallpaper_country_values":
            wallpaper_country_values,

        "user_country_labels":
            user_country_labels,

        "user_country_values":
            user_country_values,

        "top_countries":
            top_countries,

        "recent_wallpapers":
            recent_wallpapers,

        "recent_ai":
            recent_ai,

        "recent_activity":
            recent_activity,

        "recent_orders":
            recent_orders,

        "profit_labels":
            profit_labels,

        "revenue_values":
            revenue_values,

        "expense_values":
            expense_values,

        "profit_values":
            profit_values,

        "order_status_labels":
            order_status_labels,

        "order_status_values":
            order_status_values,

        "payment_status_labels":
            payment_status_labels,

        "payment_status_values":
            payment_status_values,
    }