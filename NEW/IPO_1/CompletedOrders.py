
from prettytable import PrettyTable
from OrderAgent import OrderAgent
import emoji
# Класс выполненных заказзов
class CompletedOrders:
    def __init__(self,courier=None):
        self.orders = []
        self.strOrders = [] #названия заказов
        self.strDist = []  # расстояния заказов
        self.courier = courier

    #список названий заказов для вывода в таблице
    def addStrOrder(self, st):
        self.strOrders.append(st)

    #добавить заказ в список выполненных
    def addOrder(self, order: OrderAgent):
        self.orders.append(order)

    #построить путь от курьера до заказа и места назначения
    def addStrDist(self, currentDistance,rderDistance):
        self.strDist.append(emoji.emojize(':man_pouting:') + '_' * (int)(currentDistance) + emoji.emojize(
                    ':wrapped_gift:') + '_' * (int)(rderDistance) + emoji.emojize(
                    ':house:')+'|')
    #выводит маршрут
    def printemoji(self):
        print(f"{''.join(self.strDist)}", sep='',end='\n')

    #вывести таблицу выполенных заказов курьера по часам работы
    #для нагядности сколько часов на какой заказ было потрачено в расписании курьера
    def printOrder(self):
        #время в табице заполняется от 1го часа работы до всего количества отработанных часов
        myTable = PrettyTable(["Час" + str(i) for i in range(1, len(self.strOrders) + 1)])
        #список выпоненных заказов (названия)
        myTable.add_row(self.strOrders)
        #если курьер выполнил заказы, то вывести их
        if(len(self.strOrders)>0):
            print('\n'+self.courier.name + ' выполнил:')
            print(myTable)

