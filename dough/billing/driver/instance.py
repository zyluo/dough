#!/usr/bin/env python
# -*- coding: utf8 -*-

class InstanceBillingManager(object):

    def __init__(self):
        print "instance manager created"

    def is_active(self):
        print "instance is active"

    def is_prepaid(self):
        print "instance is active"

    def register(self):
        print "instance subscribed"

    def unregister(self):
        print "instance unsubscribed"

    def purchase(self):
        print "instance purchased"
