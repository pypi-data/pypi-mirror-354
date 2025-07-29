from datetime import datetime
import hashlib
import os, sys
import django
from django.utils.text import slugify


def sparta_8542592f4e():
    """
    
    """
    currentPath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(currentPath).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(oneLevelUpPath).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(oneLevelUpPath).replace('\\', '/')
    sys.path.append(oneLevelUpPath)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
    django.setup()


def sparta_e0f3104ab4():
    """

    """
    from django.contrib.auth.models import User
    from project.models import UserProfile, PlotDBChart
    plot_chart_set = PlotDBChart.objects.all()
    for plot_chart_obj in plot_chart_set:
        if plot_chart_obj.slug is None:
            slug = plot_chart_obj.name
            base_slug = slugify(slug)
            slug = base_slug
            counter = 1
            while PlotDBChart.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            plot_chart_obj.slug = slug
            plot_chart_obj.save()


if __name__ == '__main__':
    sparta_8542592f4e()
    qube_2292c62178()

#END OF QUBE
