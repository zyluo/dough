from novaclient.v1_1 import client

from nova import flags
from nova.openstack.common import cfg


instance_opts = [
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
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(instance_opts)


def is_running(instance_uuid):
    return not is_terminated(instance_uuid)


def is_terminated(instance_uuid):
    # TODO(lzyeval): handle error
    nt = client.Client(FLAGS.keystone_username,
                       FLAGS.keystone_password,
                       FLAGS.keystone_tenant_name,
                       FLAGS.keystone_auth_url,
                       service_type="compute")
    instance = nt.servers.get(instance_uuid)
    return not instance.status=="ACTIVE"


def get_usage(instance_uuid, datetime_from, datetime_to, order_size):
    return order_size
