#!/usr/bin/env python
# -*- coding: utf8 -*-


def subscribe_item(*args, **kwargs):
    return dict()


def unsubscribe_item(*args, **kwargs):
    return dict()


def query_payment_types(*args, **kwargs):
    resp = {
        'payment_types': ['hourly', 'daily', 'monthly'],
        }
    return {'data': resp}


def query_item_price(*args, **kwargs):
    resp = {
        'price': 222.22,
        }
    return {'data': resp}


def query_usage_report(*args, **kwargs):
    resp = {
        'instance': {
            'default': [
                ('uuid1', 'some instance', 'm1.tiny', 20, 'hours', 1123.9,),
                ('uuid1', 'some instance 2', 'm1.tiny', 20, 'months', 1123.9,),
                ],
            },     
        'floating_ip': {
            'default': [
                ('1111', '10.2.3.4', 20, 'days', 1123.9,),
                ('222', '10.4.5.6', 20, 'days', 1123.9,),
                ],
            },
        'load_balancer': {
            'default': [
                ('lb_id1', 'some load balancer', 20, 'days', 1123.9,),
                ('lb_id2', 'some load balancer 2', 20, 'days', 1123.9,),
                ]
            },
        'network': {
            'default': [
                ('1111', '10.211.23.45', 257.3, 'KBytes', 1123.9,),
                ('222', '170.1.223.5', 120.9, 'KBytes', 1123.9,),
                ]
            },
        }
    return {'data': resp}
