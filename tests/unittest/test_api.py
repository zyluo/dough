from decimal import Decimal
import unittest

import mox

from nova import utils

from dough import api
from dough import context as dough_context
from dough import db


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.mox = mox.Mox()
        self.tenant_id = 'atenant'
        self.context = dough_context.get_context(tenant_id=self.tenant_id)
        self.resource_uuid = 'a-fake-uuid-0'
        self.resource_name = 'a_fake_name_0'
        self.created_at = utils.utcnow()
        self.region_id = 1
        self.region_name = 'default'
        self.region = {
            'id': self.region_id,
            }
        self.item_id = 2
        self.item_name = 'instance'
        self.item = {
            'id': self.item_id,
            }
        self.item_type_id = 3
        self.item_type_name = 'm1.tiny'
        self.item_type = {
            'id': self.item_type_id,
            }
        self.payment_type_id = 4
        self.payment_type_name = 'hourly'
        self.payment_type_names = ['hourly', 'daily', 'monthly']
        self.payment_type = {
            'id': self.payment_type_id,
            }
        self.product_id = 5
        self.product_price = Decimal(2.40).quantize(Decimal('0.01'))
        self.products = [{
            'id': self.product_id,
            'price': self.product_price,
            }]
        self.item_products = [
            {
                'id': self.product_id,
                'payment_type': {
                    'id': self.payment_type_id,
                    'name': self.payment_type_name,
                    },
                },
            {
                'id': 50,
                'payment_type': {
                    'id': 40,
                    'name': 'daily',
                    },
                },
            {
                'id': 51,
                'payment_type': {
                    'id': 41,
                    'name': 'monthly',
                    },
                },
            ]
        self.subscription_id = 6
        self.subscription = {
            'created_at': self.created_at,
            'id': self.subscription_id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            'product': {
                'region': {
                    'name': self.region_name,
                    },
                'item': {
                    'name': self.item_name,
                    },
                'item_type': {
                    'name': self.item_type_name,
                    },
                'payment_type': {
                    'id': self.payment_type_id,
                    'name': self.payment_type_name,
                    'interval_unit': 'days',
                    'interval_size': 1,
                    },
                'order_unit': 'hours',
                'order_size': 1,
                'price': self.product_price,
                'currency': 'CNY',
                }
            }
        self.subscriptions = [{
            'id': self.subscription_id,
            }]

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_subscribe_item(self):
        self.mox.StubOutWithMock(db, 'region_get_by_name')
        self.mox.StubOutWithMock(db, 'item_get_by_name')
        self.mox.StubOutWithMock(db, 'item_type_get_by_name')
        self.mox.StubOutWithMock(db, 'payment_type_get_by_name')
        self.mox.StubOutWithMock(db, 'product_get_all')
        self.mox.StubOutWithMock(db, 'subscription_create')
        self.mox.StubOutWithMock(db, 'subscription_extend')
        db.region_get_by_name(self.context, self.region_name).\
                AndReturn(self.region)
        db.item_get_by_name(self.context, self.item_name).AndReturn(self.item)
        db.item_type_get_by_name(self.context, self.item_type_name).\
                AndReturn(self.item_type)
        db.payment_type_get_by_name(self.context, self.payment_type_name).\
                AndReturn(self.payment_type)
        db.product_get_all(self.context,
                           filters={'region_id': self.region_id,
                                    'item_id': self.item_id,
                                    'item_type_id': self.item_type_id,
                                    'payment_type_id': self.payment_type_id}).\
                                            AndReturn(self.products)
        db.subscription_create(self.context,
                               {'project_id': self.context.project_id,
                                'product_id': self.product_id,
                                'resource_uuid': self.resource_uuid,
                                'resource_name': self.resource_name}).\
                                        AndReturn(self.subscription)
        db.subscription_extend(self.context, self.subscription_id,
                               self.created_at).AndReturn(None)
        self.mox.ReplayAll()
        result = api.subscribe_item(self.context, self.region_name,
                                    self.item_name, self.item_type_name,
                                    self.payment_type_name, self.resource_uuid,
                                    self.resource_name)
        self.mox.VerifyAll()
        self.assertEqual(result, {})

    def test_unsubscribe_item(self):
        self.mox.StubOutWithMock(db, 'region_get_by_name')
        self.mox.StubOutWithMock(db, 'item_get_by_name')
        self.mox.StubOutWithMock(db, 'subscription_get_all')
        self.mox.StubOutWithMock(db, 'subscription_destroy')
        db.region_get_by_name(self.context, self.region_name).\
                AndReturn(self.region)
        db.item_get_by_name(self.context, self.item_name).AndReturn(self.item)
        db.subscription_get_all(self.context,
                                filters={
                                    'region_id': self.region_id,
                                    'item_id': self.item_id,
                                    'project_id': self.context.project_id,
                                    'resource_uuid': self.resource_uuid
                                    }).AndReturn(self.subscriptions)
        db.subscription_destroy(self.context, self.subscription_id).\
                AndReturn(None)
        self.mox.ReplayAll()
        result = api.unsubscribe_item(self.context, self.region_name,
                                      self.item_name, self.resource_uuid)
        self.mox.VerifyAll()
        self.assertEqual(result, {})

    def test_query_payment_types(self):
        self.mox.StubOutWithMock(db, 'region_get_by_name')
        self.mox.StubOutWithMock(db, 'item_get_by_name')
        self.mox.StubOutWithMock(db, 'product_get_all')
        db.region_get_by_name(self.context, self.region_name).\
                AndReturn(self.region)
        db.item_get_by_name(self.context, self.item_name).AndReturn(self.item)
        db.product_get_all(self.context,
                           filters={'region_id': self.region_id,
                                    'item_id': self.item_id}).\
                                            AndReturn(self.item_products)
        self.mox.ReplayAll()
        result = api.query_payment_types(self.context, self.region_name,
                                         self.item_name)
        self.mox.VerifyAll()
        self.assertEqual(result,
                         {'data': {
                              'payment_type_names': self.payment_type_names}})

    def test_query_product_price(self):
        self.mox.StubOutWithMock(db, 'region_get_by_name')
        self.mox.StubOutWithMock(db, 'item_get_by_name')
        self.mox.StubOutWithMock(db, 'item_type_get_by_name')
        self.mox.StubOutWithMock(db, 'payment_type_get_by_name')
        self.mox.StubOutWithMock(db, 'product_get_all')
        db.region_get_by_name(self.context, self.region_name).\
                AndReturn(self.region)
        db.item_get_by_name(self.context, self.item_name).AndReturn(self.item)
        db.item_type_get_by_name(self.context, self.item_type_name).\
                AndReturn(self.item_type)
        db.payment_type_get_by_name(self.context, self.payment_type_name).\
                AndReturn(self.payment_type)
        db.product_get_all(self.context,
                           filters={'region_id': self.region_id,
                                    'item_id': self.item_id,
                                    'item_type_id': self.item_type_id,
                                    'payment_type_id': self.payment_type_id}).\
                                            AndReturn(self.products)
        self.mox.ReplayAll()
        result = api.query_product_price(self.context, self.region_name,
                                         self.item_name, self.item_type_name,
                                         self.payment_type_name)
        self.mox.VerifyAll()
        self.assertEqual(result, {'data': {'price': self.product_price}})

    def test_query_usage_report(self):
        timestamp_from = '2012-03-24T16:44:21'
        timestamp_to = '2012-03-24T16:46:21'
        project_subscriptions = [
            {
                'id': self.subscription_id,
                'resource_uuid': self.resource_uuid,
                'resource_name': self.resource_name,
                'product': {
                    'region': {
                        'name': self.region_name,
                        },
                    'item': {
                        'name': self.item_name,
                        },
                    'item_type': {
                        'name': self.item_type_name,
                        },
                    'order_unit': 'hours',
                    'order_size': 1,
                    'price': self.product_price,
                    'currency': 'CNY',
                    }
                },
            {
                'id': 60,
                'resource_uuid': 'a-fake-uuid-1',
                'resource_name': 'a_fake_name_1',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'instance',
                        },
                    'item_type': {
                        'name': 'm1.large',
                        },
                    'order_unit': 'months',
                    'order_size': 1,
                    'price': Decimal(2100.00).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 61,
                'resource_uuid': 'a-fake-uuid-2',
                'resource_name': '10.211.23.45',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'floating_ip',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'days',
                    'order_size': 1,
                    'price': Decimal(1.10).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 62,
                'resource_uuid': 'a-fake-uuid-3',
                'resource_name': '170.1.223.5',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'floating_ip',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'days',
                    'order_size': 1,
                    'price': Decimal(1.10).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 63,
                'resource_uuid': 'a-fake-uuid-4',
                'resource_name': 'a_fake_name_4',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'load_balancer',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'days',
                    'order_size': 1,
                    'price': Decimal(2.70).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 64,
                'resource_uuid': 'a-fake-uuid-5',
                'resource_name': 'a_fake_name_5',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'load_balancer',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'days',
                    'order_size': 1,
                    'price': Decimal(2.70).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 65,
                'resource_uuid': self.resource_uuid,
                'resource_name': '192.168.0.2',
                'product': {
                    'region': {
                        'name': self.region_name,
                        },
                    'item': {
                        'name': 'network-out',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'KBytes',
                    'order_size': 1,
                    'price': Decimal(0.70).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            {
                'id': 66,
                'resource_uuid': 'a-fake-uuid-1',
                'resource_name': '192.168.0.3',
                'product': {
                    'region': {
                        'name': 'default',
                        },
                    'item': {
                        'name': 'network-out',
                        },
                    'item_type': {
                        'name': 'default',
                        },
                    'order_unit': 'KBytes',
                    'order_size': 1,
                    'price': Decimal(0.70).quantize(Decimal('0.01')),
                    'currency': 'CNY',
                    }
                },
            ]
        purchases1 = [
            {
                'quantity': 6,
                'line_total': Decimal(14.40).quantize(Decimal('0.01')),
                },
            {
                'quantity': 8,
                'line_total': Decimal(19.20).quantize(Decimal('0.01')),
                },
            {
                'quantity': 2,
                'line_total': Decimal(4.80).quantize(Decimal('0.01')),
                },
            ]
        purchases2 = [
            {
                'quantity': 1,
                'line_total': Decimal(2100.00).quantize(Decimal('0.01')),
                },
            ]
        purchases3 = [
            {
                'quantity': 6,
                'line_total': Decimal(6.60).quantize(Decimal('0.01')),
                },
            {
                'quantity': 8,
                'line_total': Decimal(8.80).quantize(Decimal('0.01')),
                },
            {
                'quantity': 5,
                'line_total': Decimal(5.50).quantize(Decimal('0.01')),
                },
            ]
        purchases4 = [
            {
                'quantity': 6,
                'line_total': Decimal(6.60).quantize(Decimal('0.01')),
                },
            {
                'quantity': 3,
                'line_total': Decimal(3.30).quantize(Decimal('0.01')),
                },
            {
                'quantity': 2,
                'line_total': Decimal(2.20).quantize(Decimal('0.01')),
                },
            ]
        purchases5 = [
            {
                'quantity': 6,
                'line_total': Decimal(16.20).quantize(Decimal('0.01')),
                },
            {
                'quantity': 3,
                'line_total': Decimal(8.10).quantize(Decimal('0.01')),
                },
            {
                'quantity': 4,
                'line_total': Decimal(10.80).quantize(Decimal('0.01')),
                },
            ]
        purchases6 = [
            {
                'quantity': 6,
                'line_total': Decimal(16.20).quantize(Decimal('0.01')),
                },
            {
                'quantity': 8,
                'line_total': Decimal(21.60).quantize(Decimal('0.01')),
                },
            {
                'quantity': 13,
                'line_total': Decimal(35.10).quantize(Decimal('0.01')),
                },
            ]
        purchases7 = [
            {
                'quantity': 1000,
                'line_total': Decimal(700.00).quantize(Decimal('0.01')),
                },
            {
                'quantity': 800,
                'line_total': Decimal(560.00).quantize(Decimal('0.01')),
                },
            {
                'quantity': 52,
                'line_total': Decimal(36.40).quantize(Decimal('0.01')),
                },
            ]
        purchases8 = [
            {
                'quantity': 9000,
                'line_total': Decimal(6300.00).quantize(Decimal('0.01')),
                },
            {
                'quantity': 800,
                'line_total': Decimal(560.00).quantize(Decimal('0.01')),
                },
            {
                'quantity': 53,
                'line_total': Decimal(37.10).quantize(Decimal('0.01')),
                },
            ]
        usage_report = {
            'load_balancer': {
                'default': [
                    ('a-fake-uuid-4', 'a_fake_name_4', 'default', 'days',
                     Decimal(2.70).quantize(Decimal('0.01')), 'CNY', 13,
                     Decimal(35.10).quantize(Decimal('0.01')),),
                    ('a-fake-uuid-5', 'a_fake_name_5', 'default', 'days',
                     Decimal(2.70).quantize(Decimal('0.01')), 'CNY', 27,
                     Decimal(72.90).quantize(Decimal('0.01')),),
                    ]
                },
            'instance': {
                'default': [
                    (self.resource_uuid, self.resource_name,
                     self.item_type_name, 'hours', self.product_price, 'CNY',
                     16, Decimal(38.40).quantize(Decimal('0.01')),),
                    ('a-fake-uuid-1', 'a_fake_name_1', 'm1.large', 'months',
                     Decimal(2100.00).quantize(Decimal('0.01')), 'CNY', 1,
                     Decimal(2100.00).quantize(Decimal('0.01')),),
                    ],
                },
            'floating_ip': {
                'default': [
                    ('a-fake-uuid-2', '10.211.23.45', 'default', 'days',
                     Decimal(1.10).quantize(Decimal('0.01')), 'CNY', 19,
                     Decimal(20.90).quantize(Decimal('0.01')),),
                    ('a-fake-uuid-3', '170.1.223.5', 'default', 'days',
                     Decimal(1.10).quantize(Decimal('0.01')), 'CNY', 11,
                     Decimal(12.10).quantize(Decimal('0.01')),),
                    ],
                },
            'network-out': {
                'default': [
                    (self.resource_uuid, '192.168.0.2', 'default', 'KBytes',
                     Decimal(0.70).quantize(Decimal('0.01')), 'CNY', 1852,
                     Decimal(1296.40).quantize(Decimal('0.01')),),
                    ('a-fake-uuid-1', '192.168.0.3', 'default', 'KBytes',
                     Decimal(0.70).quantize(Decimal('0.01')), 'CNY', 9853,
                     Decimal(6897.10).quantize(Decimal('0.01')),),
                    ]
                },
            }
        self.mox.StubOutWithMock(db, 'subscription_get_all_by_project')
        _purchase_func = 'purchase_get_all_by_subscription_and_timeframe'
        self.mox.StubOutWithMock(db, _purchase_func)
        db.subscription_get_all_by_project(self.context, self.tenant_id).\
                AndReturn(project_subscriptions)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                self.subscription_id, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases1)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                60, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases2)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                61, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases3)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                62, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases4)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                63, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases5)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                64, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases6)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                65, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases7)
        db.purchase_get_all_by_subscription_and_timeframe(self.context,
                66, timestamp_from, timestamp_to).\
                        InAnyOrder().AndReturn(purchases8)
        self.mox.ReplayAll()
        result = api.query_usage_report(self.context,
                                        timestamp_from,
                                        timestamp_to)
        self.mox.VerifyAll()
        expect_keys = usage_report.keys().sort()
        actual_keys = result['data'].keys().sort()
        self.assertEqual(expect_keys, actual_keys)
        for k, v in result['data'].iteritems():
            self.assertEqual(v, usage_report[k])
