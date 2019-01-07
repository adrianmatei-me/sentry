from __future__ import absolute_import, print_function

from django.db import models
from django.utils import timezone
from enum import Enum
from jsonfield import JSONField

from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr


class WidgetDisplayTypes(Enum):
    LINE_CHART = 'line-chart'
    MAP = 'map'
    HORIZONATAL_BAR_CHART = 'horizontal-bar-chart'
    TIMELINE = 'timeline'
    STACKED_AREA = 'stacked-area'


class WidgetDataSource(Model):
    """
    A dashboard widget.
    """
    __core__ = True

    widget_id = FlexibleForeignKey('sentry.Widget')
    type = BoundedPositiveIntegerField()
    name = models.CharField(max_length=128)
    data = JSONField(default={})
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_widgetdatasource'
        unique_together = (('widget_id', 'type', 'name'), )

    __repr__ = sane_repr('widget_id', 'type', 'name')


class Widget(Model):
    """
    A dashboard widget.
    """
    __core__ = True

    dashboard_id = FlexibleForeignKey('sentry.Dashboard')
    dashboard_order = BoundedPositiveIntegerField()
    title = models.CharField(max_length=128)
    display_type = BoundedPositiveIntegerField(choices=WidgetDisplayTypes)
    organization_id = FlexibleForeignKey('sentry.Organization')
    data = JSONField(default={})
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_widget'
        unique_together = (('organization_id', 'dashboard_id', 'dashboard_order', 'title'), )

    __repr__ = sane_repr('organization_id', 'dashboard_id', 'title')
