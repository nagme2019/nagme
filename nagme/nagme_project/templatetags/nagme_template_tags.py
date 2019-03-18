from django import template
from nagme_app.models import Category


register = template.Library()


@register.inclusion_tag('nagme/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}
