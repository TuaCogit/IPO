

#Вариант планирования выполнения заказ на курьером
class PlanningOption:
    def __init__(self, order=None, courier=None):
        self.order = order
        self.courier = courier
        self.price: float = 0.0
        self.currentDistance: float = 0.0
        self.p: float = 0.0

    #профит=цена заказа - текущая цена
    def profit(self):
        #прибыль = стоимость заказа - стоимость курьера
        self.p = self.order.orderPrice - self.price
        return self.p

