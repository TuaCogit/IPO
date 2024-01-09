
import math
from OrderAgent import OrderAgent
from PlanningOption import PlanningOption

#Класс  агент курьера
class CourierAgent:
    def __init__(self, name):
        self.name = name #имя курьера
        self.initialLocation: list = [0, 0] #местоположение
        self.speed: float = 1.0  # Скорость
        self.price: float = 1.0  # Стоимость курьреа
        self.cheduledOrder: list[OrderAgent] = []#занятость
        self.сarryingCapacity: float = 1.0 #грузоподъемность
        self.workingDay: int = 10  # 10 часов по умолчанию
        self.durationOrders:list[int] = [] #Длительности заказа


    #Истина, если курьер способен выполнить заказ, ложь - в других случаях
    def canOrder(self, order: OrderAgent):
        #если вес меньше/= грузоподъемности
        return self.сarryingCapacity >= order.weight

    #расстояние до заказа
    def currentDistance(self, order: OrderAgent):
        if len(self.cheduledOrder) > 0:
            # текущее местоположение курьера = последнее расположение курьера
            currentCourierInitialLocation = self.cheduledOrder[-1].toLocation
        else:
            # иначе текущее местоположение курьера по умолчанию (начальное, 0)
            currentCourierInitialLocation = self.initialLocation
        distance = math.dist(currentCourierInitialLocation, order.fromLocation)
        return distance

    # Истина, если курьеру выгодно
    def benefitDistance(self, order: OrderAgent):
        #дистанция заказа > расстояние до заказа
        return order.getOrderDistance() > self.currentDistance(order)

    #Строка, содержащая информацию о курьере
    def getInfo(self):
        #имя, скорость, грузоподъеность, местоположение, рабочий день
        st= [self.name, (str(round(self.speed, 2))+"км/ч"), (str(round(self.сarryingCapacity, 2))+"кг"), self.initialLocation, (str(self.workingDay)+"ч"),(str(self.workingDay-sum(self.durationOrders))+"ч")]
        return st

    #смена местоположения
    def changeLocation(self):
        self.initialLocation=self.cheduledOrder[-1].toLocation

    #Вариант размещения заказа в плане курьера
    def acceptPlanAction(self, planning_option):
        self.cheduledOrder.append(planning_option.order)

    #Вариант размещения, включающий оценки
    def requestPlanningOptionAction(self, order: OrderAgent, courier):
        #создание планирования заказа
        planningOption = PlanningOption(order, courier)
        # занятость не пустая
        if len(self.cheduledOrder) > 0:
            #текущее местоположение курьера = последнее расположение курьера
            currentCourierInitialLocation = self.cheduledOrder[-1].toLocation
        else:
            #иначе текущее местоположение курьера по умолчанию (начальное, 0)
            currentCourierInitialLocation = self.initialLocation

        #расстояние = вычисляет расстояние между 2 точками в трехмерном пространстве
        #(текущее местоположение курьера, местополож. заказа) + дистанция заказа
        distance = math.dist(currentCourierInitialLocation, order.fromLocation) + order.getOrderDistance()
        currentDistance = math.dist(currentCourierInitialLocation, order.fromLocation)
        #стоимость доставки = расстояние * ценник курьера
        courierCost = distance * courier.price
        #назначение курьера, заказа, стоимости
        planningOption.courier = courier
        planningOption.order = order
        planningOption.price = courierCost
        planningOption.currentDistance = currentDistance
        #поучение варианта назначенного заказа
        return planningOption

