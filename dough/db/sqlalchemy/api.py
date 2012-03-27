"""
"""

# load_balancers

def load_balancer_get(context, load_balancer_id):
    pass

def load_balancer_create(context, values):
    pass

def load_balancer_destroy(context, load_balancer_id):
    pass

def load_balancer_get_all(context, read_deleted=False, filters=None):
    pass

def load_balancer_get_all_by_project(context, project_id):
    pass

def load_balancer_get_by_uuid(context, load_balancer_uuid):
    pass

# regions

def region_get(context, region_id):
    pass

def region_create(context, values):
    pass

def region_destroy(context, region_id):
    pass

def region_get_all(context, read_deleted=False, filters=None):
    pass

def region_get_by_name(context, region_name):
    pass

# items

def item_get(context, item_id):
    pass

def item_create(context, values):
    pass

def item_destroy(context, item_id):
    pass

def item_get_all(context, read_deleted=False, filters=None):
    pass

def item_get_by_name(context, item_name):
    return {'id': 1}

# item_types

def item_type_get(context, item_type_id):
    pass

def item_type_create(context, values):
    pass

def item_type_destroy(context, item_type_id):
    pass

def item_type_get_all(context, read_deleted=False, filters=None):
    pass

def item_type_get_by_name(context, item_type_name):
    return {'id': 1}

# payment_types

def payment_type_get(context, payment_type_id):
    pass

def payment_type_create(context, values):
    pass

def payment_type_destroy(context, payment_type_id):
    pass

def payment_type_get_all(context, read_deleted=False, filters=None):
    pass

def payment_type_get_by_name(context, payment_type_name):
    return {'id': 1}

# products

def product_get(context, product_id):
    pass

def product_create(context, values):
    pass

def product_destroy(context, product_id):
    pass

def product_get_all(context, read_deleted=False, filters=None):
    return [{'price': 220.3, 'payment_type': {'name': 'hourly'}},
            {'price': 221.3, 'payment_type': {'name': 'daily'}},
            {'price': 222.3, 'payment_type': {'name': 'monthly'}}]

# subscriptions

def subscription_get(context, subscription_id):
    pass

def subscription_create(context, values):
    pass

def subscription_destroy(context, subscription_id):
    pass

def subscription_soft_destroy(context, subscription_id):
    return None

def subscription_get_all(context, read_deleted=False, filters=None):
    pass

def subscription_get_all_by_project(context, project_id):
    return None

# purchase

def purchase_get(context, purchase_id):
    pass

def purchase_create(context, values):
    pass

def purchase_destroy(context, purchase_id):
    pass

def purchase_get_all_by_subscription_and_timeframe(context, subscription_id,
                                                   datetime_from, datetime_to):
    # TODO(lzyeval): adopt limit
    return None
