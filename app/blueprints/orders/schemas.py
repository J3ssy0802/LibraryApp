from marshmallow import fields

from app.extensions import ma
from app.models import Order, OrderItems


class ReceiptSchema(ma.Schema):
    '''
    total: 39.02
    order: {
            order_id: 1,
            member_id: 1,
            order_date: 2024-07-01,
            order_items: [
            {
            item:{item_name: "PSL", price: 13.02},
            quantity: 3
            }
            ]
            }
    '''
    total = fields.Float(required=True)
    order = fields.Nested("OrderSchema", required=True)

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        include_relationships = True
    order_items = fields.Nested("OrderItemSchema", exclude=["id"], many=True)

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems
    item = fields.Nested("ItemSchema", exclude=["id"])

class CreateOrderSchema(ma.Schema):
    {
      "member_id": 1,
      "item_quant": [{"item_id": 1, "item_quant": 3}]
    }
    member_id = fields.Int(required=True)
    item_quant = fields.Nested("ItemQuant", many=True, required=True)

 
class ItemQuant(ma.Schema):
    item_id = fields.Int(required=True)
    item_quant = fields.Int(required=True)


order_schema = OrderSchema() 
orders_schema = OrderSchema(many=True)
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()