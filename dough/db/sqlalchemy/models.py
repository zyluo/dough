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

"""
SQLAlchemy models for dough data.
"""


from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, DateTime, Boolean, Float

from nova.db.sqlalchemy import models


class Region(models.BASE, models.NovaBase):
    """Represents regions."""

    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)


class Item(models.BASE, models.NovaBase):
    """Represents items."""

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)


class ItemType(models.BASE, models.NovaBase):
    """Represents item types."""

    __tablename__ = 'item_types'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)


class PaymentType(models.BASE, models.NovaBase):
    """Represents payment types."""

    __tablename__ = 'payment_types'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    interval_unit = Column(String(255), nullable=False)
    interval_size = Column(Integer, nullable=False)
    is_prepaid = Column(Boolean, nullable=False, default=False)


class Product(models.BASE, models.NovaBase):
    """Represents products."""

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    region_id = Column(Integer,
                       ForeignKey(Region.id),
                       nullable=False)
    region = relationship(Region,
                          backref=backref('products'),
                          foreign_keys=region_id,
                          primaryjoin='and_('
                                      'Product.region_id == Region.id,'
                                      'Product.deleted == False)')
    item_id = Column(Integer,
                     ForeignKey(Item.id),
                     nullable=False)
    item = relationship(Item,
                        backref=backref('products'),
                        foreign_keys=item_id,
                        primaryjoin='and_('
                                    'Product.item_id == Item.id,'
                                    'Product.deleted == False)')
    item_type_id = Column(Integer,
                          ForeignKey(ItemType.id),
                          nullable=False)
    item_type = relationship(ItemType,
                             backref=backref('products'),
                             foreign_keys=item_type_id,
                             primaryjoin='and_('
                                         'Product.item_type_id == ItemType.id,'
                                         'Product.deleted == False)')
    payment_type_id = Column(Integer,
                             ForeignKey(PaymentType.id),
                             nullable=False)
    payment_type = relationship(PaymentType,
                                backref=backref('products'),
                                foreign_keys=payment_type_id,
                                primaryjoin='and_('
                                            'Product.payment_type_id == '
                                            'PaymentType.id,'
                                            'Product.deleted == False)')
    order_unit = Column(String(255), nullable=False)
    order_size = Column(Integer, nullable=False)
    price = Column(Float(asdecimal=True), nullable=False)
    currency = Column(String(255), nullable=False)


class Subscription(models.BASE, models.NovaBase):
    """Represents subscriptions."""

    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer,
                        ForeignKey(Product.id),
                        nullable=False)
    product = relationship(Product,
                           backref=backref('subscriptions'),
                           foreign_keys=product_id,
                           primaryjoin='and_('
                                       'Subscription.product_id == Product.id,'
                                       'Subscription.deleted == False)')
    resource_uuid = Column(String(255), nullable=False, index=True)
    resource_name = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    status = Column(String(255), nullable=False)


class Purchase(models.BASE, models.NovaBase):
    """Represents purchases."""

    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subscription_id = Column(Integer,
                             ForeignKey(Subscription.id),
                             nullable=False)
    quantity = Column(Float(asdecimal=True), nullable=False)
    line_total = Column(Float(asdecimal=True), nullable=False)
