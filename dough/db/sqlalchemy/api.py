"""
instances
load_balancers
floating_ips
external network IO


regions
items
item_types
payment_types
products
subscriptions
purchases
"""

# load_balancers

def load_balancer_get(context, load_balancer_id):
    pass

def load_balancer_get_all(context):
    pass

def load_balancer_get_all_by_project(context, project_id):
    pass

def load_balancer_get_by_uuid(context, load_balancer_uuid):
    pass

def load_balancer_create(context, values):
    pass

def load_balancer_delete(context, load_balancer_id):
    pass

# regions

def region_get(context, region_id):
    pass

def region_get_all(context):
    pass

def region_get_by_name(context, region_name):
    pass

def region_create(context, values):
    pass

def region_delete(context, region_id):
    pass

# items

def item_get(context, item_id):
    pass

def item_get_all(context):
    pass

def item_get_by_name(context, item_name):
    pass

def item_create(context, values):
    pass

def item_delete(context, item_id):
    pass

# item_types

def item_type_get(context, item_type_id):
    pass

def item_type_get_all(context):
    pass

def item_type_get_by_name(context, item_type_name):
    pass

def item_type_create(context, values):
    pass

def item_type_delete(context, item_type_id):
    pass

# payment_types

def payment_type_get(context, payment_type_id):
    pass

def payment_type_get_all(context):
    pass

def payment_type_get_by_name(context, payment_type_name):
    pass

def payment_type_create(context, values):
    pass

def payment_type_delete(context, payment_type_id):
    pass

# products

def product_get_all(context):
    pass

def product_get_by_filters(context, filters, sort_key, sort_dir):
    pass

def product_create(context, values):
    pass

def product_delete(context, payment_type_id):
    pass

# subscriptions

def subscription_get(context, subscription_id):
    pass

def subscription_get_all(context):
    pass

def subscription_get_all_by_project(context, project_id):
    pass

def subscription_create(context, values):
    pass

def subscription_delete(context, subscription_id):
    pass

# purchase

def purchase_get(context, purchase_id):
    pass

def purchase_get_by_filters(context, filters, sort_key, sort_dir):
    pass

def purchase_create(context, values):
    pass

def purchase_delete(context, purchase_id):
    pass
