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

"""Implementation of SQLAlchemy backend."""

import datetime

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload_all
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import asc
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.expression import literal_column

from nova.db.sqlalchemy.api import model_query

from dough import exception
from dough.db.sqlalchemy import models


# regions

def region_get(context, region_id):
    result = model_query(context, models.Region).\
                     filter_by(id=region_id).\
                     first()
    if not result:
        raise exception.RegionNotFound(region_id=region_id)
    return result


def region_create(context, values):
    region_ref = models.Region()
    region_ref.update(values)
    region_ref.save()
    return region_ref


def region_destroy(context, region_id):
    session = get_session()
    with session.begin():
        session.query(models.Region).\
                filter_by(id=region_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def region_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.Region).filter_by(**filters).all()


def region_get_by_name(context, region_name):
    result = model_query(context, models.Region).\
                     filter_by(name=region_name).\
                     first()
    if not result:
        raise exception.RegionNotFoundByName(region_name=region_name)
    return result


# items

def item_get(context, item_id):
    result = model_query(context, models.Item).\
                     filter_by(id=item_id).\
                     first()
    if not result:
        raise exception.ItemNotFound(item_id=item_id)
    return result


def item_create(context, values):
    item_ref = models.Item()
    item_ref.update(values)
    item_ref.save()
    return item_ref


def item_destroy(context, item_id):
    session = get_session()
    with session.begin():
        session.query(models.Item).\
                filter_by(id=item_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def item_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.Item).filter_by(**filters).all()


def item_get_by_name(context, item_name):
    result = model_query(context, models.Item).\
                     filter_by(name=region_name).\
                     first()
    if not result:
        raise exception.ItemNotFoundByName(item_name=item_name)
    return result


# item_types

def item_type_get(context, item_type_id):
    result = model_query(context, models.ItemType).\
                     filter_by(id=item_type_id).\
                     first()
    if not result:
        raise exception.ItemTypeNotFound(item_type_id=item_type_id)
    return result


def item_type_create(context, values):
    item_type_ref = models.ItemType()
    item_type_ref.update(values)
    item_type_ref.save()
    return item_type_ref


def item_type_destroy(context, item_type_id):
    session = get_session()
    with session.begin():
        session.query(models.ItemType).\
                filter_by(id=item_type_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def item_type_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.ItemType).filter_by(**filters).all()


def item_type_get_by_name(context, item_type_name):
    result = model_query(context, models.ItemType).\
                     filter_by(name=item_type_name).\
                     first()
    if not result:
        raise exception.ItemTypeNotFoundByName(item_type_name=item_type_name)
    return result


# payment_types

def payment_type_get(context, payment_type_id):
    result = model_query(context, models.PaymentType).\
                     filter_by(id=payment_type_id).\
                     first()
    if not result:
        raise exception.PaymentTypeNotFound(payment_type_id=payment_type_id)
    return result


def payment_type_create(context, values):
    payment_type_ref = models.PaymentType()
    payment_type_ref.update(values)
    payment_type_ref.save()
    return payment_type_ref


def payment_type_destroy(context, payment_type_id):
    session = get_session()
    with session.begin():
        session.query(models.PaymentType).\
                filter_by(id=payment_type_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def payment_type_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.PaymentType).filter_by(**filters).all()


def payment_type_get_by_name(context, payment_type_name):
    result = model_query(context, models.ItemType).\
                     filter_by(name=item_type_name).\
                     first()
    if not result:
        raise exception.PaymentTypeNotFoundByName(
                payment_type_name=payment_type_name)
    return result


# products

def product_get(context, product_id):
    result = model_query(context, models.Product).\
                     filter_by(id=product_id).\
                     first()
    if not result:
        raise exception.ProductNotFound(product_id=product_id)
    return result


def product_create(context, values):
    product_ref = models.Product()
    product_ref.update(values)
    product_ref.save()
    return product_ref


def product_destroy(context, product_id):
    session = get_session()
    with session.begin():
        session.query(models.Product).\
                filter_by(id=product_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def product_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.Product).filter_by(**filters).all()

# subscriptions

def subscription_get(context, subscription_id):
    result = model_query(context, models.Product).\
                     filter_by(id=product_id).\
                     first()
    if not result:
        raise exception.SubscriptionNotFound(subscription_id=subscription_id)
    return result


def subscription_create(context, values):
    values = values.copy()
    values['status'] = 'creating'
    subscription_ref = models.Subscription()
    subscription_ref.update(values)
    subscription_ref.save()
    return subscription_ref


def subscription_destroy(context, subscription_id):
    session = get_session()
    with session.begin():
        session.query(models.Subscription).\
                filter_by(id=subscription_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'status': 'deleting',
                        'updated_at': literal_column('updated_at')})


def subscription_confirm(context, subscription_id):
    session = get_session()
    with session.begin():
        session.query(models.Subscription).\
                filter_by(id=subscription_id).\
                update({'status': 'complete',
                        'updated_at': literal_column('updated_at')})


def subscription_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.Subscription).filter_by(**filters).all()


def subscription_get_all_by_project(context, project_id):
    return model_query(context, models.Subscription).\
            filter_by(project_id=project_id).\
            all()


# purchase

def purchase_get(context, purchase_id):
    result = model_query(context, models.Purchase).\
                     filter_by(id=purchase_id).\
                     first()
    if not result:
        raise exception.PurchaseNotFound(purchase_id=purchase_id)
    return result


def purchase_create(context, values):
    purchase_ref = models.Purchase()
    purchase_ref.update(values)
    purchase_ref.save()
    return purchase_ref


def purchase_destroy(context, purchase_id):
    session = get_session()
    with session.begin():
        session.query(models.Purchase).\
                filter_by(id=purchase_id).\
                update({'deleted': True,
                        'deleted_at': utils.utcnow(),
                        'updated_at': literal_column('updated_at')})


def purchase_get_all_by_subscription_and_timeframe(context, subscription_id,
                                                   datetime_from, datetime_to):
    # TODO(lzyeval): adopt limit
    filters = filters or dict()
    return model_query(context, models.Purchase).filter_by(**filters).all()
