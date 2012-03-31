# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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

"""Nova base exception handling.

Includes decorator for re-raising Nova-type exceptions.

SHOULD include dedicated exception logging.

"""

from nova import exception

class RegionNotFound(exception.NotFound):
    message = _("Region %(region_id)s could not be found.")


class RegionNotFoundByName(exception.NotFound):
    message = _("Region %(region_name)s could not be found.")


class ItemNotFound(exception.NotFound):
    message = _("Item %(item_id)s could not be found.")


class ItemNotFoundByName(exception.NotFound):
    message = _("Item %(item_name)s could not be found.")


class ItemTypeNotFound(exception.NotFound):
    message = _("ItemType %(item_type_id)s could not be found.")


class ItemTypeNotFoundByName(exception.NotFound):
    message = _("ItemType %(item_type_name)s could not be found.")


class PaymentTypeNotFound(exception.NotFound):
    message = _("PaymentType %(payment_type_id)s could not be found.")


class PaymentTypeNotFoundByName(exception.NotFound):
    message = _("PaymentType %(payment_type_name)s could not be found.")


class ProductNotFound(exception.NotFound):
    message = _("Product %(product_id)s could not be found.")


class SubscriptionNotFound(exception.NotFound):
    message = _("Subscription %(subscription_id)s could not be found.")


class PurchaseNotFound(exception.NotFound):
    message = _("Purchase %(purchase_id)s could not be found.")
