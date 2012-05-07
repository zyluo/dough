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
    cfg.StrOpt('demux_host',
               default='somehost',
               help='Host for demux client.'),
    cfg.IntOpt('demux_port',
               default=5559,
               help='Port number for demux client.'),
    cfg.StrOpt('kanyun_host',
               default='somehost',
               help='Host for kanyun client.'),
    cfg.IntOpt('kanyun_port',
               default=5560,
               help='Port for kanyun client.'),
    cfg.StrOpt('mysql_host',
               default='somehost',
               help='Host for mysql client.'),
    cfg.IntOpt('mysql_port',
               default=3306,
               help='Port for mysql client.'),
    cfg.StrOpt('mysql_user',
               default='someuser',
               help='Username for mysql client.'),
    cfg.StrOpt('mysql_pwd',
               default='somepwd',
               help='Password for mysql client.'),
    cfg.StrOpt('nova_schema',
               default='someschema',
               help='Nova schema name for mysql client.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_opts(billing_opts)
