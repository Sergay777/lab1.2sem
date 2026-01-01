from django import template

register = template.Library()

@register.filter
def has_attribute(obj, attr_name):
    """Проверяет, есть ли у объекта атрибут с указанным именем."""
    return hasattr(obj, attr_name)