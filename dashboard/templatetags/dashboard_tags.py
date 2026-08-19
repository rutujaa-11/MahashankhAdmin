from django import template
from django.db.models import Sum
from dashboard.models import Category, Wallpaper, UserActivityLog

register = template.Library()


@register.simple_tag
def category_count():
    return Category.objects.count()


@register.simple_tag
def wallpaper_count():
    return Wallpaper.objects.count()


@register.simple_tag
def activity_count():
    return UserActivityLog.objects.count()


@register.simple_tag
def total_downloads():
    return Wallpaper.objects.aggregate(
        total=Sum("downloads")
    )["total"] or 0
@register.simple_tag
def recent_activities():
    return UserActivityLog.objects.order_by("-timestamp")[:5]