import json
from django.db.models import Case, CharField, Count, F, Value, When
from django.db.models.functions import ExtractMonth
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from pretix.base.models import Event, OrderPosition
from pretix.control.permissions import EventPermissionRequiredMixin


class AdvancedStatisticsView(EventPermissionRequiredMixin, TemplateView):
    template_name = "pretix_advanced_stats/advanced_stats.html"
    permission = "can_view_orders"

    @staticmethod
    def _get_event_by_slug(slug):
        """Retrieve event by slug, returning None if not found."""
        try:
            return Event.objects.get(slug=slug)
        except Event.DoesNotExist:
            return None

    @staticmethod
    def fill_missing_months(data_list):
        """Ensure all months are represented in the dataset with zero values if missing."""
        ordered_months = [
            "October",
            "November",
            "December",
            "January",
            "February",
            "March",
            "April",
            "May",
        ]

        all_months = {
            month: {"month_name": month, "ticket_count": 0} for month in ordered_months
        }
        event_name = None

        for entry in data_list:
            all_months[entry["month_name"]].update(entry)
            event_name = entry["event_name"]

        return [
            {**{"event_name": event_name}, **all_months[month]}
            for month in ordered_months
        ]

    @staticmethod
    def _retrieve_ticket_from_event(event):
        """Retrieve ticket count grouped by month for a given event."""
        month_name_case = Case(
            *[
                When(month=i, then=Value(name))
                for i, name in enumerate(
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ],
                    start=1,
                )
            ],
            output_field=CharField()
        )

        return (
            OrderPosition.objects.filter(
                order__event=event, order__status="p", item__admission=True
            )
            .annotate(
                month=ExtractMonth("order__datetime"),
                month_name=month_name_case,
                event_name=F("order__event__name"),
            )
            .values("event_name", "month", "month_name")
            .annotate(ticket_count=Count("id"))
            .order_by("month")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.request.event
        comparison_event = self._get_event_by_slug(
            self.request.GET.get("comparing-event", "")
        )

        tickets_current_event = self.fill_missing_months(
            self._retrieve_ticket_from_event(event)
        )
        ticket_previous_event = (
            self.fill_missing_months(self._retrieve_ticket_from_event(comparison_event))
            if comparison_event
            else None
        )

        ctx.update(
            {
                "events": [
                    (e.slug, e.name) for e in Event.objects.exclude(id=event.id)
                ],
                "selected_slug": self.request.GET.get("comparing-event", ""),
                "has_orders": event.orders.exists(),
                "sellout_comparison_data": json.dumps(
                    {
                        "labels": [d["month_name"] for d in tickets_current_event],
                        "datasets": [
                            {
                                "label": str(event.name),
                                "data": [
                                    d["ticket_count"] for d in tickets_current_event
                                ],
                                "backgroundColor": "#50A167",
                            },
                            *(
                                [
                                    {
                                        "label": str(comparison_event.name),
                                        "data": [
                                            d["ticket_count"]
                                            for d in ticket_previous_event
                                        ],
                                        "backgroundColor": "#3C1C4A",
                                    }
                                ]
                                if comparison_event
                                else []
                            ),
                        ],
                    }
                ),
            }
        )

        return ctx
