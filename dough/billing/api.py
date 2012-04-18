# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Sina Corporation
# All Rights Reserved.
# Author: Zhongyue Luo <lzyeval@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from dateutil.relativedelta import relativedelta

from nova import utils

from dough import db
from dough.billing import driver


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
            charge(context, tenant_id, subscription_id, quantity,
                   order_size, price)
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
        db.subscription_delete(context, subscription_id)
        if not is_prepaid:
            interval_info = {
                interval_unit: interval_size,
                }
            quantity = conn.get_usage(resource_uuid,
                    expires_at - relativedelta(**interval_info),
                    expires_at, order_size)
            charge(context, tenant_id, subscription_id, quantity,
                   order_size, price)


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
    charge(context, tenant_id, subscription_id, quantity, order_size, price)
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
