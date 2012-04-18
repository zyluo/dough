from demux.client import client

from nova import flags
from nova.openstack.common import cfg


load_balancer_opts = [
    cfg.StrOpt('demux_url',
               default='someurl',
               help='URL for demux client.'),
    cfg.IntOpt('demux_port',
               default=5557,
               help='Port number for demux client.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(load_balancer_opts)


def is_running(load_balancer_uuid):
    return not is_terminated(load_balancer_uuid)


def is_terminated(load_balancer_uuid):
    # TODO(lzyeval): handle error
    demux = client.Client(FLAGS.demux_url,
                       FLAGS.demux_port)
    load_balancer = demux.load_balancers.get(load_balancer_uuid)
    return load_balancer.deleted


def get_usage(load_balancer_uuid, datetime_from, datetime_to, order_size):
    return order_size
