from dough.billing.driver import instance as instance_conn
from dough.billing.driver import floating_ip as floating_ip_conn
from dough.billing.driver import load_balancer as load_balancer_conn
from dough.billing.driver import network as network_conn
from dough.billing.driver import corporate as corporate_conn

def get_connection(item_name):
    return globals()["%s_conn" % item_name]
