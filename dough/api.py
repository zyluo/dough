#!/usr/bin/env python
# -*- coding: utf8 -*-

import iso8601

from nova import flags
from nova import utils
from nova.openstack.common import cfg

from dough import db
from dough import exception


api_opts = [
    cfg.StrOpt('api_listen',
               default='localhost',
               help='IP address for dough API to listen.'),
    cfg.IntOpt('api_listen_port',
               default=5557,
               help='Port for dough api to listen.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(api_opts)

def _product_get_all(context, region=None, item=None, item_type=None,
                     payment_type=None):
    """
    """
    products = None
    try:
        # filter to get product_id
        filters = dict()
        filters['region_id'] = db.region_get_by_name(context, region)['id']
        filters['item_id'] = db.item_get_by_name(context, item)['id']
        filters['item_type_id'] = db.item_type_get_by_name(context,
                                                           item_type)['id']
        filters['payment_type_id'] = db.payment_type_get_by_name(context,
                                                            payment_type)['id']
        products = db.product_get_all(context, filters=filters)
    except Exception, e:
        # TODO(lzyeval): report
        raise
    return products

def subscribe_item(context, region=None, item=None, item_type=None,
                   payment_type=None, resource_uuid=None, resource_name=None,
                   **kwargs):
    """
    """
    # values of product
    values = {
        'project_id': context.project_id,
        'resource_uuid': resource_uuid,
        'resource_name': resource_name,
        }
    try:
        # filter to get product_id
        products = _product_get_all(context, region=region, item=item,
                                    item_type=item_type,
                                    payment_type=payment_type)
        # TODO(lzyeval): check if products size is not 1
        values['product_id'] = products[0]['id']
        subscription_ref = db.subscription_create(context, values)
        db.subscription_extend(context,
                               subscription_ref['id'],
                               subscription_ref['created_at'])
    except Exception, e:
        # TODO(lzyeval): report
        raise
    return dict()


def unsubscribe_item(context, region=None, item=None,
                     resource_uuid=None, **kwargs):
    """
    """
    try:
        subscription_id = 0
        subscriptions = db.subscription_get_all_by_resource_uuid(context,
                                                                 resource_uuid)
        if not subscriptions:
            raise exception.SubscriptionNotFoundByResourceUUID(
                    resource_uuid=resource_uuid)
        for subscription in subscriptions:
            if subscription['product']['region']['name'] != region:
                continue
            elif subscription['product']['item']['name'] != item:
                continue
            subscription_id = subscription['id']
        if not subscription_id:
            raise exception.SubscriptionNotFoundByRegionOrItem(region=region,
                                                               item=item)
        db.subscription_destroy(context, subscription_id)
    except Exception, e:
        # TODO(lzyeval): report
        raise
    return dict()


def query_payment_types(context, region=None, item=None, **kwargs):
    filters = dict()
    filters['region_id'] = db.region_get_by_name(context, region)['id']
    filters['item_id'] = db.item_get_by_name(context, item)['id']
    products = db.product_get_all(context, filters=filters)
    payment_type_info = {
        'payment_type_names': map(lambda x: x['payment_type']['name'],
                                  products),
        }
    return {'data': payment_type_info}


def query_product_price(context, region=None, item=None, item_type=None,
                     payment_type=None, resource_uuid=None, **kwargs):
    try:
        # filter to get product_id
        products = _product_get_all(context, region=region, item=item,
                                    item_type=item_type,
                                    payment_type=payment_type)
        # TODO(lzyeval): check if products size is not 1
    except Exception, e:
        # TODO(lzyeval): report
        raise
    price_info = {
        'price': products[0]['price'],
        }
    return {'data': price_info}


def query_usage_report(context, timestamp_from=None,
                       timestamp_to=None, **kwargs):
    usage_report = dict()
    datetime_from = iso8601.parse_date(timestamp_from)
    datetime_to = iso8601.parse_date(timestamp_to)
    subscriptions = list()
    _subscriptions = db.subscription_get_all_by_project(context,
                                                        context.project_id)
    for subscription in _subscriptions:
        subscription_id = subscription['id']
        resource_uuid = subscription['resource_uuid']
        resource_name = subscription['resource_name']
        region_name = subscription['product']['region']['name']
        item_name = subscription['product']['item']['name']
        item_type_name = subscription['product']['item_type']['name']
        order_unit = subscription['product']['order_unit']
        order_size = subscription['product']['order_size']
        price = subscription['product']['price']
        currency = subscription['product']['currency']
        subscriptions.append([subscription_id, resource_uuid, resource_name,
                              region_name, item_name, item_type_name,
                              order_unit, order_size, price, currency])
    for (subscription_id, resource_uuid, resource_name,
         region_name, item_name, item_type_name,
         order_unit, order_size, price, currency) in subscriptions:
        purchases = db.purchase_get_all_by_subscription_and_timeframe(context,
                                                            subscription_id,
                                                            datetime_from,
                                                            datetime_to)
        if not purchases:
            continue
        quantity_sum = sum(map(lambda x: x['quantity'], purchases))
        line_total_sum = sum(map(lambda x: x['line_total'], purchases))
        # TODO(lzyeval): remove
        #assert (line_total_sum == quantity_sum * price)
        usage_datum = (resource_uuid, resource_name, item_type_name,
                       order_unit, float(price), currency,
                       float(quantity_sum) * order_size, float(line_total_sum))
        item_usage_report = usage_report.get(item_name, dict())
        if not item_usage_report:
            usage_report[item_name] = item_usage_report
        region_usage_data = item_usage_report.get(region_name, list())
        if not region_usage_data:
            item_usage_report[region_name] = region_usage_data
        region_usage_data.append(usage_datum)
    return {'data': usage_report}
