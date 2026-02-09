from django.urls import re_path

from .views import AdvancedStatisticsView

urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/advanced_stats/$",
        AdvancedStatisticsView.as_view(),
        name="advanced_stats",
    ),
]
