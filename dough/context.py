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

"""RequestContext: context for requests that persist through all of dough."""

from nova import context as nova_context

def get_admin_context(read_deleted="no"):
    return nova_context.RequestContext(user_id=None,
                                       project_id=None,
                                       is_admin=True,
                                       read_deleted=read_deleted,
                                       overwrite=False)

def get_context(tenant_id=None, **kwargs):
    return nova_context.RequestContext(user_id=None,
                                       project_id=tenant_id,
                                       is_admin=False,
                                       read_deleted="no",
                                       overwrite=False)
