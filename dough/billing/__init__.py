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

from nova import flags
from nova import utils
from nova.openstack.common import cfg

from dough.billing.api import *


billing_opts = [
    cfg.StrOpt('farmer_listen',
               default='localhost',
               help='IP address for dough farmer to bind.'),
    cfg.IntOpt('farmer_listen_port',
               default=5558,
               help='Port for dough farmer to bind.'),
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
    cfg.StrOpt('demux_url',
               default='someurl',
               help='URL for demux client.'),
    cfg.IntOpt('demux_port',
               default=5557,
               help='Port number for demux client.'),
    cfg.StrOpt('kanyun_url',
               default='someurl',
               help='URL for kanyun client.'),
    cfg.IntOpt('kanyun_port',
               default=5558,
               help='Port for kanyum client.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(billing_opts)
