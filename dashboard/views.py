from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Category, Wallpaper, UserActivityLog, AIWallpaperStyle, AIWallpaperGeneration


@login_required(login_url='/admin/login/')
def dashboard_view(request):

    total_users = User.objects.count()

    total_categories = Category.objects.count()

    total_wallpapers = Wallpaper.objects.count()

    total_downloads = (
        Wallpaper.objects.aggregate(
            total=Sum('downloads')
        )['total'] or 0
    )

    categories = Category.objects.all().order_by('name')

    category_chart_data = []

    for category in categories:

        wallpaper_count = Wallpaper.objects.filter(
            category=category
        ).count()

        category_chart_data.append({
            'name': category.name,
            'count': wallpaper_count,
        })

    country_chart_data = []

    countries = (
        Wallpaper.objects
        .values('country')
        .annotate(
            total_downloads=Sum('downloads')
        )
        .order_by('country')
    )

    for item in countries:

        country = item['country'] or 'Unknown'

        downloads = item['total_downloads'] or 0

        country_chart_data.append({
            'name': country,
            'downloads': downloads,
        })

    recent_activities = (
        UserActivityLog.objects
        .order_by('-timestamp')[:5]
    )

    context = {
        'total_users': total_users,
        'total_categories': total_categories,
        'total_wallpapers': total_wallpapers,
        'total_downloads': total_downloads,

        'category_chart_data': category_chart_data,

        'country_chart_data': country_chart_data,

        'recent_activities': recent_activities,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@login_required(login_url='/admin/login/')
def wallpapers_view(request):

    wallpapers = (
        Wallpaper.objects
        .select_related('category')
        .order_by('-uploaded_at')
    )

    return render(
        request,
        'dashboard/wallpapers.html',
        {
            'wallpapers': wallpapers
        }
    )


@login_required(login_url='/admin/login/')
def user_list_view(request):

    users = (
        User.objects
        .all()
        .order_by('-date_joined')
    )

    return render(
        request,
        'dashboard/users.html',
        {
            'users': users
        }
    )


@login_required(login_url='/admin/login/')
def user_activities_view(request):

    activities = (
        UserActivityLog.objects
        .order_by('-timestamp')
    )

    return render(
        request,
        'dashboard/user_activities.html',
        {
            'activities': activities
        }
    )


@login_required(login_url='/admin/login/')
def ai_generations_view(request):

    generations = (
        AIWallpaperGeneration.objects
        .select_related('style')
        .order_by('-created_at')
    )

    styles = AIWallpaperStyle.objects.all()

    return render(
        request,
        'dashboard/ai_generations.html',
        {
            'generations': generations,
            'styles': styles,
        }
    )


@login_required(login_url='/admin/login/')
def chatbot_logs_view(request):

    return render(
        request,
        'dashboard/chatbot_logs.html',
        {}
    )


@login_required(login_url='/admin/login/')
def product_list_view(request):

    wallpapers = (
        Wallpaper.objects
        .select_related('category')
        .order_by('-uploaded_at')
    )

    return render(
        request,
        'dashboard/products.html',
        {
            'wallpapers': wallpapers
        }
    )


@login_required(login_url='/admin/login/')
def order_list_view(request):

    return render(
        request,
        'dashboard/orders.html',
        {}
    )