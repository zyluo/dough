import datetime
from decimal import Decimal
import unittest
import sys

from dough import context as dough_context
from dough import db
from dough import exception

from nova import flags
from nova import utils
from nova.db.sqlalchemy.session import get_engine

utils.default_flagfile(filename='/etc/dough/dough.conf')
flags.FLAGS(sys.argv)

FLAGS = flags.FLAGS


class DBApiTestCase(unittest.TestCase):

    def setUp(self):
        super(DBApiTestCase, self).setUp()
        engine = get_engine()
        self.connection = engine.connect()
        self.tenant_id = 'atenant'
        self.context = dough_context.get_context(tenant_id=self.tenant_id)
        self.resource_uuid = 'a-fake-uuid-0'
        self.resource_name = 'a_fake_name_0'
        self.region_name = 'default'
        self.item_name = 'instance'
        self.item_type_name = 'm1.tiny'
        self.payment_type_name = 'hourly'
        #self.product_price = Decimal(2.40).quantize(Decimal('0.01'))

    def truncate_table(self, table):
        self.connection.execution_options(autocommit=True).\
                execute("TRUNCATE %s;" % table) 

    def compare_records(self, expect, actual, skip_id=False):
        for k, v in expect.__dict__.iteritems():
            if k.startswith('_') or isinstance(v, datetime.datetime):
                continue
            elif k == 'id' and skip_id:
                continue
            if k in ['price', 'quantity', 'line_total']:
                self.assertEqual(Decimal(v).quantize(Decimal('0.01')),
                                 actual[k].quantize(Decimal('0.01')))
            else:
                self.assertEqual(v, actual[k])

    def tearDown(self):
        pass

    def test_region_create(self):
        self.truncate_table("regions")
        values = {
            'name': self.region_name,
            }
        expect = db.region_create(self.context, values)
        actual = db.region_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_region_create_duplicate_name(self):
        self.truncate_table("regions")
        values = {
            'name': self.region_name,
            }
        db.region_create(self.context, values)
        self.assertRaises(Exception, db.region_create, self.context, values)

    def test_region_destroy(self):
        self.truncate_table("regions")
        values = {
            'name': self.region_name,
            }
        expect = db.region_create(self.context, values)
        db.region_destroy(self.context, expect.id)
        self.assertRaises(exception.RegionNotFoundByName,
                          db.region_get_by_name,
                          self.context, self.region_name)
        self.assertRaises(exception.RegionNotFound,
                          db.region_get,
                          self.context, expect.id)

    def test_region_create_deleted_duplicate_name(self):
        self.truncate_table("regions")
        values = {
            'name': self.region_name,
            }
        expect = db.region_create(self.context, values)
        db.region_destroy(self.context, expect.id)
        actual = db.region_create(self.context, values)
        self.compare_records(expect, actual, skip_id=True)

    def test_item_create(self):
        self.truncate_table("items")
        values = {
            'name': self.item_name,
            }
        expect = db.item_create(self.context, values)
        actual = db.item_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_item_create_duplicate_name(self):
        self.truncate_table("items")
        values = {
            'name': self.item_name,
            }
        db.item_create(self.context, values)
        self.assertRaises(Exception, db.item_create, self.context, values)

    def test_item_destroy(self):
        self.truncate_table("items")
        values = {
            'name': self.item_name,
            }
        expect = db.item_create(self.context, values)
        db.item_destroy(self.context, expect.id)
        self.assertRaises(exception.ItemNotFoundByName,
                          db.item_get_by_name,
                          self.context, self.item_name)
        self.assertRaises(exception.ItemNotFound,
                          db.item_get,
                          self.context, expect.id)

    def test_item_create_deleted_duplicate_name(self):
        self.truncate_table("items")
        values = {
            'name': self.item_name,
            }
        expect = db.item_create(self.context, values)
        db.item_destroy(self.context, expect.id)
        actual = db.item_create(self.context, values)
        self.compare_records(expect, actual, skip_id=True)

    def test_item_type_create(self):
        self.truncate_table("item_types")
        values = {
            'name': self.item_type_name,
            }
        expect = db.item_type_create(self.context, values)
        actual = db.item_type_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_item_type_create_duplicate_name(self):
        self.truncate_table("item_types")
        values = {
            'name': self.item_type_name,
            }
        db.item_type_create(self.context, values)
        self.assertRaises(Exception, db.item_type_create, self.context, values)

    def test_item_type_destroy(self):
        self.truncate_table("item_types")
        values = {
            'name': self.item_type_name,
            }
        expect = db.item_type_create(self.context, values)
        db.item_type_destroy(self.context, expect.id)
        self.assertRaises(exception.ItemTypeNotFoundByName,
                          db.item_type_get_by_name,
                          self.context, self.item_type_name)
        self.assertRaises(exception.ItemTypeNotFound,
                          db.item_type_get,
                          self.context, expect.id)

    def test_item_type_create_deleted_duplicate_name(self):
        self.truncate_table("item_types")
        values = {
            'name': self.item_type_name,
            }
        expect = db.item_type_create(self.context, values)
        db.item_type_destroy(self.context, expect.id)
        actual = db.item_type_create(self.context, values)
        self.compare_records(expect, actual, skip_id=True)

    def test_payment_type_create(self):
        self.truncate_table("payment_types")
        values = {
            'name': self.payment_type_name,
            'interval_unit': 'hours',
            'interval_size': 1,
            'is_prepaid': True,
            }
        expect = db.payment_type_create(self.context, values)
        actual = db.payment_type_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_payment_type_create_duplicate_name(self):
        self.truncate_table("payment_types")
        values = {
            'name': self.payment_type_name,
            'interval_unit': 'hours',
            'interval_size': 1,
            'is_prepaid': True,
            }
        db.payment_type_create(self.context, values)
        self.assertRaises(Exception, db.payment_type_create,
                          self.context, values)

    def test_payment_type_destroy(self):
        self.truncate_table("payment_types")
        values = {
            'name': self.payment_type_name,
            'interval_unit': 'hours',
            'interval_size': 1,
            'is_prepaid': True,
            }
        expect = db.payment_type_create(self.context, values)
        db.payment_type_destroy(self.context, expect.id)
        self.assertRaises(exception.PaymentTypeNotFoundByName,
                          db.payment_type_get_by_name,
                          self.context, self.payment_type_name)
        self.assertRaises(exception.PaymentTypeNotFound,
                          db.payment_type_get,
                          self.context, expect.id)

    def test_payment_type_create_deleted_duplicate_name(self):
        self.truncate_table("payment_types")
        values = {
            'name': self.payment_type_name,
            'interval_unit': 'hours',
            'interval_size': 1,
            'is_prepaid': True,
            }
        expect = db.payment_type_create(self.context, values)
        db.payment_type_destroy(self.context, expect.id)
        actual = db.payment_type_create(self.context, values)
        self.compare_records(expect, actual, skip_id=True)

    def test_product_create(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        expect = db.product_create(self.context, values)
        actual = db.product_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_product_create_duplicate(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        db.product_create(self.context, values)
        self.assertRaises(Exception, db.product_create, self.context, values)

    def test_product_destroy(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        expect = db.product_create(self.context, values)
        db.product_destroy(self.context, expect.id)
        self.assertRaises(exception.ProductNotFound,
                          db.product_get,
                          self.context, expect.id)

    def test_subscription_create(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        expect = db.subscription_create(self.context, values)
        actual = db.subscription_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_subscription_create_duplicate(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        db.subscription_create(self.context, values)
        self.assertRaises(Exception, db.subscription_create,
                          self.context, values)

    def test_subscription_extend(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        expect = db.subscription_create(self.context, values)
        datetime_to = datetime.datetime.now() + datetime.timedelta(days=1)
        db.subscription_extend(self.context, expect.id, datetime_to)
        actual = db.subscription_get(self.context, expect.id)
        self.assertEqual(datetime_to.day, actual['expires_at'].day)

    def test_subscription_destroy(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        expect = db.subscription_create(self.context, values)
        db.subscription_destroy(self.context, expect.id)
        self.assertRaises(exception.SubscriptionNotFound,
                          db.subscription_get,
                          self.context, expect.id)

    def test_subscription_verify(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        expect = db.subscription_create(self.context, values)
        db.subscription_verify(self.context, expect.id)
        actual = db.subscription_get(self.context, expect.id)
        expect.status = "verified"
        self.compare_records(expect, actual)

    def test_subscription_error(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        expect = db.subscription_create(self.context, values)
        db.subscription_error(self.context, expect.id)
        actual = db.subscription_get(self.context, expect.id)
        expect.status = "error"
        self.compare_records(expect, actual)

    def test_purchase_create(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        self.truncate_table("purchases")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        subscription_ref = db.subscription_create(self.context, values)
        values = {
            'subscription_id': subscription_ref.id,
            'quantity': 1.56,
            'line_total': 1.56 * product_ref.price,
            }
        expect = db.purchase_create(self.context, values)
        actual = db.purchase_get(self.context, expect.id)
        self.compare_records(expect, actual)

    def test_purchase_destroy(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        self.truncate_table("purchases")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        subscription_ref = db.subscription_create(self.context, values)
        values = {
            'subscription_id': subscription_ref.id,
            'quantity': 1.56,
            'line_total': 1.56 * product_ref.price,
            }
        expect = db.purchase_create(self.context, values)
        db.purchase_destroy(self.context, expect.id)
        self.assertRaises(exception.PurchaseNotFound,
                          db.purchase_get,
                          self.context, expect.id)

    def test_purchase_get_by_subscription_recent(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        self.truncate_table("purchases")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        subscription_ref = db.subscription_create(self.context, values)
        values = {
            'subscription_id': subscription_ref.id,
            'quantity': 1.56,
            'line_total': 1.56 * product_ref.price,
            }
        expect = db.purchase_create(self.context, values)
        actual = db.purchase_get_by_subscription_recent(self.context,
                                                        expect.subscription_id)
        self.compare_records(expect, actual)

    def test_purchase_get_by_subscription_recent_not_found(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        self.truncate_table("purchases")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        subscription_ref = db.subscription_create(self.context, values)
        values = {
            'subscription_id': subscription_ref.id,
            'quantity': 1.56,
            'line_total': 1.56 * product_ref.price,
            }
        db.purchase_create(self.context, values)
        self.assertRaises(exception.PurchaseNotFoundBySubscription,
                          db.purchase_get_by_subscription_recent,
                          self.context, 12345)

    def test_purchase_get_all_by_subscription_and_timeframe(self):
        self.truncate_table("regions")
        self.truncate_table("items")
        self.truncate_table("item_types")
        self.truncate_table("payment_types")
        self.truncate_table("products")
        self.truncate_table("subscriptions")
        self.truncate_table("purchases")
        region_ref = db.region_create(self.context, {'name': 'a_region'})
        item_ref = db.item_create(self.context, {'name': 'an_item'})
        item_type_ref = db.item_type_create(self.context,
                                            {'name': 'an_item_type'})
        payment_type_ref = db.payment_type_create(self.context,
                                                  {'name': 'a_payment_type',
                                                   'interval_unit': 'days',
                                                   'interval_size': 12345,
                                                   'is_prepaid': False})
        values = {
            'region_id': region_ref.id,
            'item_id': item_ref.id,
            'item_type_id': item_type_ref.id,
            'payment_type_id': payment_type_ref.id,
            'order_unit': 'some_measure',
            'order_size': 1,
            'price': 11.24,
            'currency': 'CNY',
            }
        product_ref = db.product_create(self.context, values)
        values = {
            'project_id': self.context.project_id,
            'product_id': product_ref.id,
            'resource_uuid': self.resource_uuid,
            'resource_name': self.resource_name,
            }
        subscription_ref = db.subscription_create(self.context, values)
        values = {
            'subscription_id': subscription_ref.id,
            'quantity': 1.56,
            'line_total': 1.56 * product_ref.price,
            }
        expect = db.purchase_create(self.context, values)
        purchases = db.purchase_get_all_by_subscription_and_timeframe(
                self.context, expect.subscription_id,
                datetime.datetime.now() - datetime.timedelta(seconds=3),
                datetime.datetime.now() + datetime.timedelta(seconds=3))
        self.compare_records(expect, purchases[0])
