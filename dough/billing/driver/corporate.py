import json
import pickle
from urllib import urlencode
import urllib2

from keystoneclient.v2_0 import client

from nova import flags
from nova.openstack.common import cfg


corporate_opts = [
    cfg.StrOpt('keystone_username',
               default='someusername',
               help='Username for keystone client.'),
    cfg.StrOpt('keystone_password',
               default='somepassword',
               help='Password for keystone client.'),
    cfg.StrOpt('keystone_tenant_name',
               default='sometenantname',
               help='Tenant name for keystone client.'),
    cfg.StrOpt('keystone_auth_url',
               default='someurl',
               help='Auth URL for keystone client.'),
    cfg.StrOpt('corporate_user_key',
               default='somekey',
               help='User ID key for corporate account.'),
    cfg.StrOpt('corporate_type',
               default='sometype',
               help='Payment type for corporate account.'),
    cfg.StrOpt('corporate_service',
               default='someservice',
               help='Payment service for corporate account.'),
    cfg.StrOpt('corporate_action',
               default='someaction',
               help='Payment action for corporate account.'),
    cfg.StrOpt('corporate_product',
               default='someproduct',
               help='Payment product for corporate account.'),
    cfg.StrOpt('corporate_url',
               default='someurl',
               help='Payment URL for corporate account.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(corporate_opts)


def deduct(tenant_id, line_total):
    # TODO(lzyeval): handle error
    keystone = client.Client(username=FLAGS.keystone_username,
                             password=FLAGS.keystone_password,
                             tenant_name=FLAGS.keystone_tenant_name,
                             auth_url=FLAGS.keystone_auth_url)
    tenant = keystone.tenants.get(tenant_id)
    tenant_info = pickle.loads(tenant.description.encode('utf-8'))  
    user_id = tenant_info[FLAGS.corporate_user_key]
    values = {
        'uid': user_id,
        'amount': line_total,
        'type': FLAGS.corporate_type,
        'service': FLAGS.corporate_service,
        'action': FLAGS.corporate_action,
        'product': FLAGS.corporate_product,
        'comment': 'openstack payment',
        }
    url = FLAGS.corporate_url + "&" + urlencode(values)
    result =  json.load(res = urllib2.urlopen(url).read())
    if result['code'] != 0:
        # TODO(lzyeval): report
        pass
