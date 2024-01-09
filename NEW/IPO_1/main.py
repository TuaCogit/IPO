
from OrderAgent import OrderAgent
from CompanyAgent import CompanyAgent
from CourierAgent import CourierAgent
import random
import sys
from PlanningOption import PlanningOption

#создание курьера вручную
def createCourier(i, company):
    courier = CourierAgent("Курьер " + str(i))  # создание курьера
    courier.speed = isFloat("Введите скорость (км/ч): ") #скорость
    print("Введите координаты х и у начального местоположения")
    x=isXY("x: ")
    y=isXY("y: ")
    courier.initialLocation = [x,y] # нач.местоположение
    courier.сarryingCapacity = isFloat("Введите грузоподъемность (кг): ") #грузоподъемност
    courier.price = isFloat("Введите базовую стоимость (р): ")#базовая стоимость
    courier.workingDay = isWorkDay("Введите длительность рабочего дня (ч): ")#длительность рабочего дня
    company.addCourier(courier)  # добавление курьера в компанию
    return company

#создание заказа вручную
def createOrder(company):
    company.numOrder+=1
    j=company.numOrder
    order = OrderAgent("Заказ " + str(j))  # создание заказа
    order.weight =isFloat("Введите вес заказа (кг): ")
    print("Введите координаты х и у откуда забрать заказ")
    x1 = isXY("x: ")
    y1 = isXY("y: ")
    order.fromLocation = [x1,y1]  # из точки
    print("Введите координаты х и у куда доставить заказ")
    x2 = isXY("x: ")
    y2 = isXY("y: ")
    order.toLocation = [x2,y2]  # в точку
    order.getOrderDistance()  # расстояние на которое доставить
    company.addOrder(order)  # добавление заказа в компанию
    return company

#создание курьеров и заказов автоматически
def createOrdersAndCouriers(countCouriers, countOrders, company):
    while company.numCourier < countCouriers:
        company.numCourier += 1
        i = company.numCourier
        courier = CourierAgent("Курьер " + str(i))  # создание курьера
        courier.speed = random.uniform(6.0, 12)  # скорость курьера
        courier.initialLocation = [random.randint(1, 10), random.randint(1, 10)]  # нач.местоположение
        courier.сarryingCapacity = random.uniform(30.0, 100.0)  # рузоподъемност
        courier.price = random.uniform(1, 5)  # базовая стоимость
        courier.workingDay = random.randint(6, 12)  # длительность рабочего дня
        company.addCourier(courier)  # добавление курьера в компанию

    while company.numOrder < countOrders:
        company.numOrder += 1
        j=company.numOrder
        order = OrderAgent("Заказ " + str(j))  # создание заказа
        order.weight = random.uniform(1.0, 50.0)  # вес заказа
        order.fromLocation = [random.randint(1, 10), random.randint(1, 10)]  # из точки
        order.toLocation = [random.randint(1, 10), random.randint(1, 10)]  # в точку
        order.getOrderDistance()  # расстояние на которое доставить
        company.addOrder(order)  # добавление заказа в компанию
    return company

#проверка на ввод целого числа
def isInt(strInput):
    while True:
        try:
            userInput = int(input(strInput))
        except ValueError:
            print("Это не число")
            continue
        else:
            break
    return userInput

#проверка на ввод дробного числа
def isFloat(strInput):
    while True:
        try:
            userInput = float(input(strInput))
        except ValueError:
            print("Это не число")
            continue
        else:
            break
    return userInput

#проверка длительности рабочего дня
def isWorkDay(strInput):
    while True:
        try:
            intInput = isInt(strInput)
            if(intInput>12):
                raise Exception('')
        except Exception:
            print("Рабочий день не больше 12ч")
            continue
        else:
            break
    return intInput

#проверка координат
def isXY(strInput):
    while True:
        try:
            xyInput = isInt(strInput)
            if ((xyInput>10 )or(xyInput<1)):
                raise Exception('')
        except Exception:
            print("Координата от 1 до 10")
            continue
        else:
            break
    return xyInput

if __name__ == '__main__':

    #добавить  тип событий добавить курьер, заказ, удалить курьера
    #перевести в свободные заказы
    #посчитать расстояние от местополож до заказа одна стоимость, а выонение заказа отдельно
    #если далеко ехать, то невыгодно



    company = CompanyAgent()
    while True:
        print(f"Выберите действие\n"
              f"1. Задать количество курьеров и заказов со случайными параметрами\n"
              f"2. Добавить вручную курьера\n"
              f"3. Добавить вручную заказ\n"
              f"4. Удалить курьера\n"
              f"5. ЗАПУСК\n"
              f"Для выхода введите любой символ")

        key = input("Введите номер: ");
        match key:
            case "1":
                #всего курьеров
                countCouriers = isInt("Введите кол-во курьеров: ")+company.numCourier
                #всего заказов
                countOrders = isInt("Введите кол-во заказов: ")+company.numOrder
                #создать курьеров и заказы и добавить в компанию
                currentCompany= createOrdersAndCouriers(countCouriers, countOrders, company)
                currentCompany.print_orders() #вывести ссозданные заказы
                currentCompany.printCouriers() #вывести созданных курьеров

            case "2":
                #создать вручную курьера
                currentCompany = createCourier(len(company.couriers)+1, company)
                currentCompany.printCouriers()  # вывести созданных курьеров

            case "3":
                #создать вручную заказ
                currentCompany = createOrder(company)
                currentCompany.print_orders()  # вывести ссозданные заказы

            case "4":
                # проверить наличие курьрьеров
                if (len(company.couriers) > 0):
                    numCourier = isInt("Введите номер курьера: ")
                    for courier in company.couriers:
                       if(courier.name==("Курьер "+str(numCourier))):
                            company.delCouriers(courier)
                else:
                    print("Курьеры отсутствуют\n")
                    continue

            case "5":
                #проверить наличие заказов и курьрьеров
                if((len(company.couriers)>0) or (len(company.orders)>0)):
                    company.startPlaner()
                else:
                    print("Заказы или курьеры отсутствуют\n")
                    continue
            case _:
                sys.exit()




'''

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

    '''

