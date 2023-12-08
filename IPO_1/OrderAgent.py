
import math
from PlanningOption import PlanningOption


# Класс агент заказа
class OrderAgent:
    def __init__(self, name):
        self.name = name
        self.fromLocation: list = [0, 0] # из места
        self.toLocation: list = [0, 0] # в место
        self.weight: float = 1.0  # вес
        self.orderDistance: float = 0.0 # расстояние
        self.orderPrice: float = 0.0 #цена заказа по тарифу компании
        self.currentPlan: PlanningOption = PlanningOption() #текущий план/состояние
        self.isPlanned: bool #спланированный
        self.duration: int=0 # Стоимость выполнения заказа по тарифу компании

    def getOrderPrice(self, price):
        self.orderPrice = self.orderDistance * price
    #расстояние от начально точки до конечной
    def getOrderDistance(self):
        self.orderDistance = math.dist(self.fromLocation, self.toLocation)
        return self.orderDistance

    #Строка, содержащая информацию о Заказе
    def getInfo(self):
        st = [self.name, self.fromLocation, self.toLocation, (str(round(self.orderDistance, 2)) + "км"), (str(round(self.orderPrice, 2)) + "р"), (str(round(self.weight, 2)) + "кг")]
        return st

    #Базовый процесс планирования Заказа
    def planOrderAction(self, couriers, order):
        #cписок курьеров = поиск курьера по параметрам
        couriersList = self.findCouriers(couriers, order)
        planning = []
        for courier in couriersList:
            #вариант назаначения заказа текущему курьеру
            planningOption = courier.requestPlanningOptionAction(order, courier)
            #если заказ спланирован, поместить его в список вариантов курьер-заказ
            if planningOption:
                planning.append(planningOption)

        #если список планирование не пустой (есть варианты назначения курьера на заказ)
        if len(planning) > 0:
            #Выбирает лучший для заказа вариант назначения исходя из прибыли для компании
            bestOption = self.getBestOptions(planning)
            if bestOption:
                #если удачно, то разместить вариант в плане курьера
                bestOption.courier.acceptPlanAction(bestOption)
                #текущее состояние = лучший вариант назначения курьера на заказ
                self.currentPlan = bestOption
                return True
        return False
    #Список подходящих курьеров
    def findCouriers(self, couriers, order):
        couriersList = []
        for courier in couriers:
            #Предварительный расчет суммы длительностей заказов
            #длительности всех выпоненных заказов + время доставки заказа курьером(расстояние/скорость)
            totalDuration = sum(courier.durationOrders)+ self.timeCouriers(courier)
            # если грузоподъемность позволяет И последнее время завершения заказа + время текущ зак. меньше времени работы
            if (totalDuration <= courier.workingDay) and (courier.canOrder(order)):
                self.duration=self.timeCouriers(courier) #длительность выполнения текуего заказа
                couriersList.append(courier) #добавить курера в список курьеров
        return couriersList

    def timeCouriers(self, courier):
        #время доставки = расстояние на скорость
        timeDuration = math.ceil(self.getOrderDistance()/courier.speed)
        return timeDuration

    #Выбирает лучший для заказа вариант планирования
    def getBestOptions(self, options: list[PlanningOption]):
        sortedOption = sorted(options, key=lambda x: x.profit(), reverse=True)
        if sortedOption:
            sortedOption[0].courier.durationOrders.append(self.duration)
            bestOption = sortedOption[0]
        else:
            bestOption = None
        return bestOption
