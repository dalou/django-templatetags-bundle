from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def get_object(l, index):
    return l[index]


@register.filter
def get_item(d, key, default=None):
    if default:
        d.get(key, None)
    return d.get(key)

@register.simple_tag
def post_user_like(request, post):
    is_like = post.likes.get_rating_for_user(request.user, request.META['REMOTE_ADDR'], request.COOKIES)
    return 'active' if is_like else ''

@register.filter
def divideby(value, arg): return int(arg) / int(value)