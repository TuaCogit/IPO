
from OrderAgent import OrderAgent
from CompanyAgent import CompanyAgent
from CourierAgent import CourierAgent
import random
from PlanningOption import PlanningOption


if __name__ == '__main__':
    i=1
    j=1
    company = CompanyAgent()
    while i <= 15:
        courier = CourierAgent("Курьер "+str(i)) #создание курьера
        courier.speed=random.uniform(6.0, 12) #скорость курьера
        courier.initialLocation = [random.randint(1, 10), random.randint(1, 10)] #нач.местоположение
        courier.сarryingCapacity = random.uniform(30.0, 100.0) #рузоподъемност
        courier.price = random.uniform(1, 5) #базовая стоимость
        courier.workingDay = random.randint(6, 12) #длительность рабочего дня
        company.addCourier(courier) #добавление курьера в компанию
        i+=1

    while j <= 30:
        order = OrderAgent("Заказ "+str(j)) #создание заказа
        order.weight = random.uniform(1.0, 50.0) #вес заказа
        order.fromLocation = [random.randint(1, 10), random.randint(1, 10)] #из точки
        order.toLocation = [random.randint(1, 10), random.randint(1, 10)] #в точку
        order.getOrderDistance() #расстояние на которое доставить
        company.addOrder(order) #добавление заказа в компанию
        j += 1
    #вывести созданные заказы
    company.print_orders()
    #вывести существующих курьеров
    company.printCouriers()
    #распланировать заказы
    company.startPlaner()



