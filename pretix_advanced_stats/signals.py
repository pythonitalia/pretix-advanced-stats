from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.signals import order_paid, order_placed
from pretix.control.signals import nav_event


@receiver(nav_event, dispatch_uid="pretix_advanced_stats_nav")
def control_nav_import(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_view_orders", request=request
    ):
        return []

    return [
        {
            "label": _("Advanced Stats"),
            "url": reverse(
                "plugins:pretix_advanced_stats:advanced_stats",
                kwargs={
                    "organizer": request.event.organizer.slug,
                    "event": request.event.slug,
                },
            ),
            "parent": reverse(
                "control:event.orders",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.event.organizer.slug,
                },
            ),
            "active": (url.namespace == "plugins:pretix_advanced_stats"),
            "icon": "bar-chart",
            "position": 999900,
        }
    ]


def clear_cache(sender, *args, **kwargs):
    cache = sender.cache
    cache.delete("statistics_obd_data")
    cache.delete("statistics_obp_data")
    cache.delete("statistics_rev_data")


order_placed.connect(clear_cache)
order_paid.connect(clear_cache)
