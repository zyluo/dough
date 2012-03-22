#!/usr/bin/env python
# -*- coding: utf8 -*-

class InstanceBillingManager(object):

    def __init__(self):
        print "instance manager created"

    def is_active(self):
        print "instance is active"

    def subscribe(self):
        # try:
        #     check instance status
        #     create subscription
        #     if prepaid:
        #         self.purchase
        # except Exception, e:
        #     report
        #     raise
        print "instance subscribed"

    def unsubscribe(self):
        # try:
        #     check instance status
        #     create subscription
        #     if not prepaid:
        #         self.purchase
        # except Exception, e:
        #     report
        #     raise
        print "instance unsubscribed"

    def purchase(self):
        print "instance purchased"
