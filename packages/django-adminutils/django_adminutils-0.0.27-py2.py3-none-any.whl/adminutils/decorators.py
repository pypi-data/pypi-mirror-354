import functools

from django.template.loader import render_to_string
from django.template.response import SimpleTemplateResponse


def options(**kwargs):
    map = {
        "desc": "short_description",
        "order": "admin_order_field",
    }

    def wrapper(func):
        for k, v in kwargs.items():
            setattr(func, map.get(k, k), v)
        return func

    return wrapper


def rendered_field(template):
    def processor(func):
        @functools.wraps(func)
        def renderer(self, obj):
            context = func(self, obj)
            return render_to_string(template, context)

        return renderer

    return processor


def save_request(func):
    from . import ModelAdmin

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            self = func.__wrapped__.__self__
        except AttributeError:
            pass
        else:
            if isinstance(self, ModelAdmin):
                self.set_request(request)
                try:
                    res = func(request, *args, **kwargs)
                except:
                    self._locals.request = None
                    raise

                def unset(*args):
                    self.unset_request()

                if isinstance(res, SimpleTemplateResponse):
                    res.add_post_render_callback(unset)
                else:
                    unset()
                return res
        return func(request, *args, **kwargs)

    return wrapper
