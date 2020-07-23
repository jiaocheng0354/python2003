import xadmin

from order.models import Order, OrderDetail


class OrderAdmin(object):
    pass
xadmin.site.register(Order, OrderAdmin)

class OrderDetailAdmin(object):
    pass
xadmin.site.register(OrderDetail, OrderDetailAdmin)
