from django import template
from django.forms import SplitDateTimeField

register = template.Library()
def css_classes_for_field(field, custom_classes):
    orig_class = field.field.widget.attrs.get('class', '')

    required = 'required' if field.field.required else ''
    classes = field.css_classes(' '.join([orig_class, custom_classes, required]))
    return classes
    
@register.filter()
# css_classes_for_field
def add_class(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    is_datetime_field = (isinstance(field.field, SplitDateTimeField))

    if is_datetime_field:
        return field
    else:
        try:
            # For widgets like SelectMultiple, checkboxselectmultiple
            field.field.widget.widget.attrs.update({'class': classes})
        except:
            field.field.widget.attrs.update({'class': classes})
        return field