from lecopain.app import db
from flask import jsonify
from sqlalchemy import func

from lecopain.dao.models import (
    Shipment, 
    Order, 
    Customer, 
    ShipmentSchema, 
    CompleteShipmentSchema,
    ShipmentStatus_Enum,
    PaymentStatus_Enum
)

class ShipmentDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_shipments = Shipment.query \
            .order_by(Shipment.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments)

    @staticmethod
    def read_by_subscription(subscription_id, nocanceled, nopaid):
        all_shipments = Shipment.query \
            .filter(Shipment.subscription_id == subscription_id)
        
        if nocanceled is True:
            all_shipments = all_shipments.filter(Shipment.status != ShipmentStatus_Enum.ANNULEE.value)
        
        if nopaid is True:
            all_shipments = all_shipments.filter(Shipment.payment_status != PaymentStatus_Enum.OUI.value)
        
        all_shipments =  all_shipments.order_by(Shipment.shipping_dt.desc()).all()

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments)
    
    @staticmethod
    def read_by_subscription_pagination(subscription_id, page, per_page):
        all_shipments = Shipment.query \
            .filter(Shipment.subscription_id == subscription_id) \
            .filter(Shipment.subscription_id == subscription_id) \
            .order_by(Shipment.shipping_dt.desc()) \
            .paginate(page=page, per_page=per_page)

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments.items), all_shipments.prev_num, all_shipments.next_num

    @staticmethod
    def read_by_customer_by_period(customer_id, start=0, end=None, nocanceled=False, nopaid=False):
      all_shipments = Shipment.query \
        .filter(Shipment.customer_id == customer_id)
      
      if nocanceled is True:
        all_shipments = all_shipments.filter(Shipment.status != ShipmentStatus_Enum.ANNULEE.value)
        
      if nopaid is True:
        all_shipments = all_shipments.filter(Shipment.payment_status != PaymentStatus_Enum.OUI.value)
      
      if(start != 0 ):
            all_shipments = all_shipments.filter(
                Shipment.shipping_dt >= start).filter(
                Shipment.shipping_dt <= end)
        
      all_shipments = all_shipments.order_by(Shipment.shipping_dt.desc()).all()
      
      # Serialize the data for the response
      shipment_schema = ShipmentSchema(many=True)
      return shipment_schema.dump(all_shipments)
            
    @staticmethod
    def count_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0
    
    @staticmethod
    def count_canceled_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id) \
            .filter(Shipment.shipping_status == ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_canceled_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)\
            .filter(Shipment.shipping_status == ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0
    
    @staticmethod
    def count_effective_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id) \
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_effective_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)\
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0

    @staticmethod
    def count_paid_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id) \
            .filter(Shipment.payment_status == PaymentStatus_Enum.OUI.value)\
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_paid_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)\
            .filter(Shipment.payment_status == PaymentStatus_Enum.OUI.value)\
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0

    @staticmethod
    def count_in_sub_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id) \
            .filter(Shipment.subscription_id != None) \
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_in_sub_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)\
            .filter(Shipment.subscription_id != None)\
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0
    
    @staticmethod
    def count_out_sub_by_customer(customer_id, start=None, end=None):
        query = Shipment.query \
            .filter(Shipment.customer_id == customer_id) \
            .filter(Shipment.subscription_id == None) \
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.count()
    
    @staticmethod
    def sum_out_sub_by_customer(customer_id, start=None, end=None):
        query = db.session.query(func.sum(Shipment.shipping_price))\
            .filter(Shipment.customer_id == customer_id)\
            .filter(Shipment.subscription_id == None)\
            .filter(Shipment.shipping_status != ShipmentStatus_Enum.ANNULEE.value)
        if start != None and end != None:
            query = query.filter(Shipment.shipping_dt >= start)\
            .filter(Shipment.shipping_dt <= end)
        return query.scalar() or 0

    
    @staticmethod
    def read_by_customer_pagination(customer_id, page, per_page):
      all_shipments = Shipment.query \
        .filter(Shipment.customer_id == customer_id) \
        .order_by(Shipment.shipping_dt.desc()) \
        .paginate(page=page, per_page=per_page)

      # Serialize the data for the response
      shipment_schema = ShipmentSchema(many=True)
      return shipment_schema.dump(all_shipments.items), all_shipments.prev_num, all_shipments.next_num

    @staticmethod
    def get_one(id):
        return Shipment.query.get_or_404(id)


    @staticmethod
    def read_one(id):

        shipment = Shipment.query.get_or_404(id)

        # Serialize the data for the response
        shipment_schema = CompleteShipmentSchema(many=False)
        return shipment_schema.dump(shipment)

    @staticmethod
    def read_some(customer_id, start, end):

        all_shipments = Shipment.query

        if(start != 0 ):
            all_shipments = all_shipments.filter(
                Shipment.shipping_dt >= start).filter(
                Shipment.shipping_dt <= end)

        if customer_id != 0:
            all_shipments = all_shipments.filter(
                Shipment.customer_id == customer_id)

        all_shipments = all_shipments.order_by(Shipment.shipping_dt.desc()) \
        .all()

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments)
    
    @staticmethod
    def read_some_pagination(customer_id, start, end, page, per_page, nocanceled, nopaid):

        all_shipments = Shipment.query

        if(start != 0 ):
            all_shipments = all_shipments.filter(
                Shipment.shipping_dt >= start).filter(
                Shipment.shipping_dt <= end)
                
        if nocanceled is True:
            all_shipments = all_shipments.filter(Shipment.status != ShipmentStatus_Enum.ANNULEE.value)
        
        if nopaid is True:
            all_shipments = all_shipments.filter(Shipment.payment_status != PaymentStatus_Enum.OUI.value)

        if customer_id != 0:
            all_shipments = all_shipments.filter(
                Shipment.customer_id == customer_id)
            
        #all_shipments = all_shipments.order_by(Shipment.id.desc())

        all_shipments = all_shipments.order_by(Shipment.shipping_dt.desc()) \
        .paginate(page=page, per_page=per_page)

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments.items), all_shipments.prev_num, all_shipments.next_num
    
    @staticmethod
    def read_some_valid(customer_id, start, end):

        all_shipments = Shipment.query

        if(start != 0 ):
            all_shipments = all_shipments.filter(
                Shipment.shipping_dt >= start).filter(
                Shipment.shipping_dt <= end)

        if customer_id != 0:
            all_shipments = all_shipments.filter(
                Shipment.customer_id == customer_id)
        
        all_shipments = all_shipments.filter(
                Shipment.status != ShipmentStatus_Enum.ANNULEE.value)

        all_shipments = all_shipments.order_by(Shipment.shipping_dt.desc()) \
        .all()

        # Serialize the data for the response
        shipment_schema = ShipmentSchema(many=True)
        return shipment_schema.dump(all_shipments)


    @staticmethod
    def add(shipment):
        customer = Customer.query.get_or_404(int(shipment.get('customer_id')))
        # TODO
        ## get Customer address =| set shipment address

        created_shipment = Shipment(title=shipment.get('title'),
            status=shipment.get('status'),
            customer_id=shipment.get('customer_id'),
            shipping_dt=shipment.get('shipping_dt'),
            category=shipment.get('category'),
            shipping_address = customer.address,
            shipping_cp=customer.cp,
            shipping_city=customer.city)
        if shipment.get('subscription_id') != None and shipment.get('subscription_id') != 'None':
           created_shipment.subscription_id = int(shipment.get('subscription_id'))
        
        db.session.add(created_shipment)
        
        customer.nb_shipments = customer.nb_shipments + 1
        return created_shipment

    @staticmethod
    def update_shipping_dt(id, shipping_dt):
        shipment = shipment = Shipment.query.get_or_404(id)
        shipment.shipping_dt = shipping_dt
        db.session.commit()

    @staticmethod
    def update_status(id, status):
        shipment = shipment = Shipment.query.get_or_404(id)
        shipment.status = status
        db.session.commit()

    @staticmethod
    def update_payment_status(id, status):
        shipment = shipment = Shipment.query.get_or_404(id)
        shipment.payment_status = status
        db.session.commit()

    @staticmethod
    def update_shipping_status(id, status):
        shipment = shipment = Shipment.query.get_or_404(id)
        shipment.shipping_status = status
        db.session.commit()

    @staticmethod
    def delete(id):
        shipment = shipment = Shipment.query.get_or_404(id)
        customer = Customer.query.get_or_404(shipment.customer.id)
        db.session.delete(shipment)
        customer.nb_subscriptions = customer.nb_shipments - 1
        db.session.commit()

    # @
    #
    @staticmethod
    def create_shipment(shipment):
        created_shipment = ShipmentDao.add(shipment)
        db.session.commit()
        return created_shipment

    # @
    #
    @staticmethod
    def remove_all_orders(shipment):
        for order in shipment.orders :
            db.session.delete(order)
        db.session.commit()

    @staticmethod
    def update_db(shipment):
        db.session.commit()
