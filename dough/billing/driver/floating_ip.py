from novaclient.v1_1 import client

from nova import flags
from nova.openstack.common import cfg

FLAGS = flags.FLAGS

def is_running(floating_ip_uuid):
    return not is_terminated(floating_ip_uuid)


def is_terminated(floating_ip_uuid):
    # TODO(lzyeval): handle error
    nt = client.Client(FLAGS.keystone_username,
                       FLAGS.keystone_password,
                       FLAGS.keystone_tenant_name,
                       FLAGS.keystone_auth_url,
                       service_type="compute")
    #fix me(yaguang),handle vary exception,when floating ip
    #is released by user,we can not get info from novaclient
    try:
        floating_ip = nt.floating_ips.get(floating_ip_uuid)
    except Exception:
        return True
    return False


def get_usage(floating_ip_uuid, datetime_from, datetime_to, order_size):
    return order_size
