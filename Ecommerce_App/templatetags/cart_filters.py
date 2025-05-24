from django import template

# If you want to do any calculations directly in the template, use Custom Template Filter Concept

register = template.Library()

@register.filter(name='get_quantity')
def get_quantity(cart_quantities, product_id):
    """Custom filter to fetch the quantity in products page for a specific product ID"""
    return cart_quantities.get(product_id, 0)


# @register.filter
# def multiply(value, arg):
#     return value * arg