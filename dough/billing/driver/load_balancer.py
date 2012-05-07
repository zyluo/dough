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


FLAGS = flags.FLAGS


class Client(object):

    def __init__(self, protocol="tcp", host="localhost", port="80"):
        url = "%s://%s:%s" % (protocol, host, port)
        context = zmq.Context()
        self.handler = context.socket(zmq.REQ)
        self.handler.connect(url)

    def __del__(self):
        self.handler.close()

    def send(self, msg_body):
        msg_type = 'lb'
        msg_uuid = str(utils.gen_uuid())
        self.handler.send_multipart([msg_type, msg_uuid,
                                     utils.dumps(msg_body)])
        r_msg_type, r_msg_uuid, r_msg_body = self.handler.recv_multipart()
        assert (all([x == y for x, y in zip([msg_type, msg_uuid],
                                            [r_msg_type, r_msg_uuid])]))
        result = utils.loads(r_msg_body)['msg']
        if result['code'] == 500:
            raise Exception()
        else:
            return result['load_balancer_ids']


DEMUX_CLIENT = Client(host=FLAGS.demux_host, port=FLAGS.demux_port)


def is_running(load_balancer_uuid):
    # TODO(lzyeval): handle error
    load_balancers = DEMUX_CLIENT.send({'cmd': 'read_load_balancer_id_all',
                                        'msg': {'user_name': 'foo',
                                                'tenant': 'bar',}})
    return load_balancer_uuid in load_balancers


def is_terminated(load_balancer_uuid):
    return not is_running(load_balancer_uuid)


def get_usage(load_balancer_uuid, datetime_from, datetime_to, order_size):
    return order_size
