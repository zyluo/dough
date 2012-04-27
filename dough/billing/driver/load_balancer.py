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

from demux.client import client
from nova import flags


FLAGS = flags.FLAGS

DEMUX_CLIENT = client.Client(FLAGS.demux_url, FLAGS.demux_port)


def is_running(load_balancer_uuid):
    return not is_terminated(load_balancer_uuid)


def is_terminated(load_balancer_uuid):
    # TODO(lzyeval): handle error
    load_balancer = DEMUX_CLIENT.send(load_balancer_uuid)
    return load_balancer.deleted


def get_usage(load_balancer_uuid, datetime_from, datetime_to, order_size):
    return order_size
