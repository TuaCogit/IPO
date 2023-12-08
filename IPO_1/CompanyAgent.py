from collections import deque
from OrderAgent import OrderAgent
from CourierAgent import CourierAgent
from prettytable import PrettyTable
from CompletedOrders import CompletedOrders

# Класс  агент компании, хранит в себе список курьеров
class CompanyAgent:
    def __init__(self):
        self.price_per_distance: float = 20.0  # цена за ед.дистанции
        self.couriers = []  # список курьеров
        self.orders= []   #список заказов
        self.orderQueue: deque[OrderAgent] = deque() #очередь заказов
        self.completedOrders: list[CompletedOrders]=[] #выполненные заказы
        self.ordersNotComplited = []  #список не выполненных заказов

    #добавление курьера в список курьеров
    def addCourier(self, courier):
        if isinstance(courier, CourierAgent):
            self.couriers.append(courier)
        else:
            print("Неверный тип данных. Ожидался объект CourierAgent.")

    # добавление заказа в список выпоненных заказов
    def addCompletedOrders(self, completed):
        if isinstance(completed, CompletedOrders):
            self.completedOrders.append(completed)
        else:
            print("Неверный тип данных. Ожидался объект CompletedOrders.")
    # добавление заказа в список всех заказов
    def addOrder(self, order):
        if isinstance(order, OrderAgent):
            self.orders.append(order)
        else:
            print("Неверный тип данных. Ожидался объект OrderAgent.")

    # добавление заказа в список не сделанных заказов
    def addOrderNotComplited(self, order):
        if isinstance(order, OrderAgent):
            self.ordersNotComplited.append(order)
        else:
            print("Неверный тип данных. Ожидался объект OrderAgent.")
    #вывести заказы
    def print_orders(self):
        myTable = PrettyTable(["Заказ", "Откуда", "Куда доставить", "Расстояние", "Стоимость", "Вес"])
        for order in self.orders:
            order.getOrderPrice(self.price_per_distance)
            myTable.add_row(order.getInfo())
        #сортировка по стоимости заказа
        myTable.sortby = "Стоимость"
        print(myTable)

    #вывести курьеров
    def printCouriers(self):
        myTable = PrettyTable(["Курьер", "Скорость", "Грузоподъемность", "Местоположение","Время работы"])
        for courier in self.couriers:
            completed = CompletedOrders(courier) # заполняем таблицу для выполенных заказов курьерами
            self.addCompletedOrders(completed)
            myTable.add_row(courier.getInfo())
        print(myTable)

    # вывести выпоненные заказы по курьерам
    def printCompletedOrdersCouriers(self):
        for compl in self.completedOrders:
            compl.printOrder()

    #выводит незапланированные заказы
    def print_notCompletedOrders(self):
        myTable = PrettyTable(["Заказ", "Откуда", "Куда доставить", "Расстояние", "Стоимость","Вес"])
        for order in self.ordersNotComplited:
            order.getOrderPrice(self.price_per_distance)
            myTable.add_row(order.getInfo())
        print(myTable)

    # Подготовка очереди заказов к планированию
    def prepareQueue(self):
        # отсортированные заказы по стоиости
        sorted_orders = sorted(self.orders, key=lambda x: x.orderPrice, reverse=True)
        #добавляются в очередь от самого дорого к самому дешевому
        for order in sorted_orders:
            self.orderQueue.append(order)

    #Запускает цикл планирования заказов
    def startPlaner(self):
        #отсортированные заказы по стоиости
        self.prepareQueue()
        #цикл планирования заказов
        self.startCycle()

    #Реализация цикла планирования заказов
    def startCycle(self):
        totalProfit: float = 0.0 #общая прибыль
        while len(self.orderQueue) > 0: #пока в очереди есть заказы
            #получение первого заказа в очереди
            orderForPlanning = self.orderQueue.popleft()
            print(f"Планируется заказ: " + str(orderForPlanning.getInfo()))
            #планирование заказа (список курьеров, первый заказ в очереди)
            result = orderForPlanning.planOrderAction(self.couriers, orderForPlanning)
            if result: #если заказ запланирован
                #общая приыль += прибыль текущего плана
                totalProfit += orderForPlanning.currentPlan.profit()
                #получаем текущего назначенного на заказ курьеа
                thisCourier=orderForPlanning.currentPlan.courier
                #формируем строку с названием заказа размером с длительностью самого заказа
                st = [orderForPlanning.currentPlan.order.name for x in range(0, thisCourier.durationOrders[-1])]
                #добавляем строку названий заказов в список выполненных заказов текущего курьера
                for compl in self.completedOrders:
                    if compl.courier==thisCourier:
                        for j in range(thisCourier.durationOrders[-1]):
                            compl.addStrOrder(st[j])
                print(
                    f"Заказ запланирован: {thisCourier.name} c прибылью: "
                    f"{round(orderForPlanning.currentPlan.p, 2)}р"
                    f" Рабочий день курьера: {thisCourier.workingDay}ч"
                    f" Осталось работать: {thisCourier.workingDay-len(thisCourier.durationOrders)}ч")
            #если не нашелся курьер, подходящий по грузоподъемности и времени работы
            else:
                self.addOrderNotComplited(orderForPlanning)
                print("Заказ не запланирован")
        #вывести выполненные заказы каждого курьера
        self.printCompletedOrdersCouriers()
        #если есть невыполненные заказы
        if self.ordersNotComplited:
            print(f"Невыполненные заказы")
            self.print_notCompletedOrders()
        print(f"Итоговая прибыль: {round(totalProfit, 2)}")

