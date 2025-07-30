import copy
import threading

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.postgres.fields import DateRangeField
from django_object_actions import DjangoObjectActions

from .actions import form_processing_action, object_action, queryset_action
from .decorators import options, rendered_field, save_request
from .widgets import (
    AdminDateRangeWidget,
    admin_detail_link,
    boolean_icon_with_text,
    formatted_json,
    html_list,
    simple_code_block,
)

__version__ = "0.0.28"
__url__ = "https://github.com/GaretJax/django-adminutils"
__author__ = "Jonathan Stoppani"
__email__ = "jonathan@stoppani.name"
__license__ = "MIT"
__all__ = [
    "boolean_icon_with_text",
    "formatted_json",
    "form_processing_action",
    "html_list",
    "ModelAdmin",
    "object_action",
    "options",
    "queryset_action",
    "save_request",
    "simple_code_block",
    "rendered_field",
]


def linked_relation(attribute_name, label_attribute=None, short_description=None):
    def getter(self, obj):
        for attr in attribute_name.split("__"):
            obj = getattr(obj, attr)
            if obj is None:
                # Allow None values at any point in the chain
                return None

        return admin_detail_link(
            obj,
            text=(getattr(obj, label_attribute) if obj and label_attribute else None),
        )

    if short_description is None:
        short_description = attribute_name.replace("__", " ").replace("_", " ")
    getter.short_description = short_description
    getter.admin_order_field = attribute_name
    getter.allow_tags = True
    return getter


def linked_inline(attribute_name, short_description=None):
    def getter(self, obj):
        return admin_detail_link(obj, getattr(obj, attribute_name), bold=True)

    if short_description is None:
        short_description = attribute_name.replace("_", " ")
    getter.short_description = short_description
    getter.admin_order_field = attribute_name
    getter.allow_tags = True
    return getter


def pop_fields(fieldsets, fields):
    if not fields:
        return fieldsets
    fieldsets = copy.deepcopy(fieldsets)
    for label, spec in fieldsets:
        spec["fields"] = [f for f in spec["fields"] if f not in fields]
    return [spec for spec in fieldsets if spec[1]["fields"]]


class CreationFormAdminMixin(object):
    creation_fieldsets = None
    creation_readonly_fields = None
    creation_form = None

    def get_fieldsets(self, request, obj=None):
        if obj is None and self.creation_fieldsets is not None:
            return self.creation_fieldsets
        return super(CreationFormAdminMixin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj is None and self.creation_readonly_fields is not None:
            return self.creation_readonly_fields
        return super(CreationFormAdminMixin, self).get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None and self.creation_form is not None:
            kwargs["form"] = self.creation_form
        return super(CreationFormAdminMixin, self).get_form(request, obj, **kwargs)


class EditOnlyInlineMixin:
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class DefaultThreadLocal(threading.local):
    def __init__(self, /, **kwargs):
        self.__dict__.update(kwargs)


class ModelAdmin(DjangoObjectActions, admin.ModelAdmin):
    formfield_overrides = {
        DateRangeField: {"widget": AdminDateRangeWidget},
    }

    def __init__(self, *args, **kwargs):
        self._locals = DefaultThreadLocal(request=None)
        super().__init__(*args, **kwargs)

    @property
    def request(self):
        return self._locals.request

    def set_request(self, request):
        old_request, self._locals.request = self._locals.request, request
        return old_request

    def unset_request(self):
        return self.set_request(None)

    def get_filtered_queryset(self, request):
        from urllib.parse import parse_qsl

        from django.http import HttpRequest, QueryDict
        from django.urls import reverse

        preserved_filters = self.get_preserved_filters(request)

        changelist_url = reverse(
            f"admin:{self.opts.app_label}_{self.opts.model_name}_changelist",
            current_app=self.admin_site.name,
        )
        querystring = dict(parse_qsl(preserved_filters)).get("_changelist_filters")

        req = HttpRequest()
        req.method = "GET"
        req.path = req.path_info = changelist_url
        req.META = request.META.copy()
        req.META["QUERY_STRING"] = querystring
        req.GET = QueryDict(querystring, encoding=req.encoding)
        req.user = request.user

        return self.get_changelist_instance(req).get_queryset(req)

    def add_preserved_filters(self, request, url, preserve_others=False):
        preserved_filters = self.get_preserved_filters(request)
        if preserve_others:
            preserved_qsl = self._get_preserved_qsl(request, preserved_filters)
        else:
            preserved_qsl = []
        return add_preserved_filters(
            {
                "preserved_filters": preserved_filters,
                "preserved_qsl": preserved_qsl,
                "opts": self.opts,
            },
            url,
        )

    class Media:
        css = {
            "all": ("admin/css/overrides.css",),
        }
