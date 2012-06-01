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

import zmq

from nova import flags
from nova import utils
from novaclient.v1_1 import client


FLAGS = flags.FLAGS

NOVA_CLIENT = client.Client(FLAGS.keystone_username,
                            FLAGS.keystone_password,
                            FLAGS.keystone_tenant_name,
                            FLAGS.keystone_auth_url,
                            service_type="compute")


class Client():

    def __init__(self, protocol="tcp", host="localhost", port="80"):
        url = "%s://%s:%s" % (protocol, host, port)
        context = zmq.Context()
        self.handler = context.socket(zmq.REQ)
        self.handler.connect(url)
        # default value
        self.cf_str = u''
        self.scf_str = u''
        self.statistic = 0
        self.period = 5
        self.time_from = 0
        self.time_to = 0
        self.key = u''

    def __del__(self):
        self.handler.close()

    def send(self, msg_body):
        msg_type = 'kanyun'
        msg_uuid = str(utils.gen_uuid())
        self.handler.send_multipart([msg_type, msg_uuid,
                                     utils.dumps(msg_body)])
        r_msg_type, r_msg_uuid, r_msg_body = self.handler.recv_multipart()
        assert (all([x == y for x, y in zip([msg_type, msg_uuid],
                                            [r_msg_type, r_msg_uuid])]))
        result = utils.loads(r_msg_body)
        if result['code'] == 500:
            raise Exception()
        else:
            return result['data'] or dict()


KANYUN_CLIENT = Client(host=FLAGS.kanyun_host, port=FLAGS.kanyun_port)


def is_running(instance_uuid):
    try:
        instance = NOVA_CLIENT.servers.get(instance_uuid)
    except Exception:
        return True
    return instance.status == "ACTIVE"


def is_terminated(instance_uuid):
    try:
        instance = NOVA_CLIENT.servers.get(instance_uuid)
    except Exception:
        return True
    return instance.status == "DELETED"


def get_usage(instance_uuid, datetime_from, datetime_to, order_size):
    data = KANYUN_CLIENT.send({'method': 'query_usage_report',
                               'args': {
                                   'id': instance_uuid,
                                   'metric': 'vmnetwork',
                                   'metric_param': 'total',
                                   'statistic': 'sum',
                                   'period': 60,
                                   'timestamp_from': datetime_from.isoformat(),
                                   'timestamp_to': datetime_to.isoformat(),
                                   }})
    return sum(data.values())
