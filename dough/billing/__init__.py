#!/usr/bin/env python
# -*- coding: utf8 -*-

from dateutil.relativedelta import relativedelta

from nova import flags
from nova import utils
from nova.openstack.common import cfg

from dough import db
from dough.billing import driver


api_opts = [
    cfg.StrOpt('farmer_listen',
               default='localhost',
               help='IP address for dough farmer to bind.'),
    cfg.IntOpt('farmer_listen_port',
               default=5558,
               help='Port for dough farmer to bind.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(api_opts)


def creating(context, subscription_id, tenant_id, resource_uuid,
             created_at, deleted_at, expires_at,
             order_unit, order_size, price, currency, region_name, 
             item_name, interval_unit, interval_size, is_prepaid):
    conn = driver.get_connection(item_name)
    if not conn.is_running(resource_uuid):
        if created_at + relativedelta(minutes=10) < utils.utcnow():
            db.subscription_error(context, subscription_id)
            # TODO(lzyeval): report
    else:
        interval_info = {
            interval_unit: interval_size,
            }
        db.subscription_verify(context, subscription_id)
        if is_prepaid:
            quantity = conn.get_usage(resource_uuid,
                    expires_at - relativedelta(**interval_info),
                    expires_at, order_size)
            charge(context, subscription_id, quantity, order_size, price)
        db.subscription_extend(context, subscription_id,
                               expires_at + relativedelta(**interval_info))


def deleting(context, subscription_id, tenant_id, resource_uuid,
             created_at, deleted_at, expires_at,
             order_unit, order_size, price, currency, region_name, 
             item_name, interval_unit, interval_size, is_prepaid):
    conn = driver.get_connection(item_name)
    if not conn.is_terminated(resource_uuid):
        if deleted_at + relativedelta(minutes=10) < utils.utcnow():
            db.subscription_error(context, subscription_id)
            # TODO(lzyeval): report
    else:
        # TODO(lzyeval): implement
        db.subscription_destroy(context, subscription_id)
        if not is_prepaid:
            interval_info = {
                interval_unit: interval_size,
                }
            quantity = conn.get_usage(resource_uuid,
                    expires_at - relativedelta(**interval_info),
                    expires_at, order_size)
            charge(context, subscription_id, quantity, order_size, price)


def verified(context, subscription_id, tenant_id, resource_uuid,
             created_at, deleted_at, expires_at,
             order_unit, order_size, price, currency, region_name, 
             item_name, interval_unit, interval_size, is_prepaid):
    conn = driver.get_connection(item_name)
    if not conn.is_running(resource_uuid):
        raise Exception()
    interval_info = {
        interval_unit: interval_size,
        }
    quantity = conn.get_usage(resource_uuid,
                              expires_at - relativedelta(**interval_info),
                              expires_at, order_size)
    charge(context, subscription_id, quantity, order_size, price)
    db.subscription_extend(context, subscription_id,
                           expires_at + relativedelta(**interval_info))


def error(*args, **kwargs):
    # TODO(lzyeval): report
    return


def charge(context, tenant_id, subscription_id, quantity, order_size, price):
    line_total = order_size * price / quantity
    values = {
        'subscription_id': subscription_id,
        'quantity': quantity,
        'line_total': line_total,
    }
    db.purchase_create(context, values)
    conn = driver.get_connection('corporate')
    conn.deduct(tenant_id, line_total)
