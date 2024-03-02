class Person:
    name: str = ""
    count_to_buy: int = -1
    count_can_buy: int = -1
    can_buy: bool = False
    arrival_time: float = 0
    service_time: float = -1
    waiting_time: float = -1
    departure_time: float = -1

    def __init__(self, name, arrival_time: float):
        self.name = name
        self.count_to_buy: int = -1
        self.count_can_buy: int = -1
        self.can_buy: bool = False
        self.arrival_time: float = arrival_time
        self.service_time: float = -1
        self.waiting_time: float = float("inf")
        self.departure_time: float = float("-inf")

    def display(self):
        print("Name:", self.name)
        print("Count to buy:", self.count_to_buy)
        print("Count can buy:", self.count_can_buy)
        print("Can buy:", self.can_buy)
        print("Arrival time:", self.arrival_time)
        print("Service time:", self.service_time)
        print("Departure time:", self.departure_time)
        print("Waiting time:", self.waiting_time)
        print("")


class Orders:
    name: str = ""
    count: int = -1
    start_time: float = -1
    end_time: float = -1
    process_time: float = -1
    count_stock_before: int = -1
    count_stock_after: int = -1

    def __init__(self, name: str, count: int, start_time: float, process_time: float, count_stock_before: int,
                 count_stock_after: int):
        self.name = name
        self.count = count
        self.start_time = start_time
        self.end_time = 0
        self.process_time = process_time
        self.count_stock_before = count_stock_before
        self.count_stock_after = count_stock_after

    def display(self):
        print("Name:", self.name)
        print("Count:", self.count)
        print("Start time:", self.start_time)
        print("End time:", self.start_time + self.process_time)
        print("Process time:", self.process_time)
        print("Count stock before:", self.count_stock_before)
        print("Count stock after:", self.count_stock_after)
        print("")


class Experiment:
    sim_time: float = 0
    arrival_time: float = 0
    service_time: float = 0
    stock: int = 0
    stock_max: int = 0
    stock_min: int = 0
    stock_restock: int = 0
    clients_count: int = 0
    people: list[Person] = []
    orders: list[Orders] = []
    money_balance: float = 0
    # about persons
    count_persons_can_buy = 0
    count_persons_cannot_buy = 0
    count_persons_can_buy_all=0
    count_persons_cannot_buy_all=0

    def __init__(self, sim_time: float, arrival_time: float, service_time: float, stock: int, stock_max: int,
                 stock_min: int, stock_restock: int, clients_count: int, money_balance: int, people: list, orders: list,
                 count_persons_can_buy: int,count_persons_cannot_buy:int,count_persons_can_buy_all:int,count_persons_cannot_buy_all:int):
        self.sim_time = sim_time
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.stock = stock
        self.stock_max = stock_max
        self.stock_min = stock_min
        self.stock_restock = stock_restock
        self.clients_count = clients_count
        self.people = people
        self.orders = orders
        self.money_balance = money_balance
        self.count_persons_can_buy = count_persons_can_buy
        self.count_persons_cannot_buy=count_persons_cannot_buy
        self.count_persons_can_buy_all=count_persons_can_buy_all
        self.count_persons_cannot_buy_all=count_persons_cannot_buy_all

    def display(self):
        print(f"Money Balance: {self.money_balance}")
        print("Sim time:", self.sim_time)
        print("Arrival time:", self.arrival_time)
        print("Service time:", self.service_time)
        print("Stock:", self.stock)
        print("Stock max:", self.stock_max)
        print("Stock min:", self.stock_min)
        print("Stock restock:", self.stock_restock)
        print("Clients count:", self.clients_count)
        print("People:")
        for person in self.people:
            person.display()
        print("Orders:")
        for order in self.orders:
            print("Name:", order.name)
            print("Count:", order.count)
            print("Start time:", order.start_time)
            print("End time:", order.end_time)
            print("Process time:", order.process_time)
            print("Count stock before:", order.count_stock_before)
            print("Count stock after:", order.count_stock_after)
            print("")

    def display_people(self):
        for person in self.people:
            person.display()

    def display_orders(self):
        for order in self.orders:
            order.display()

    def count_persons_cannot_buy(self):
        count = 0
        for person in self.people:
            if not person.can_buy:
                count += 1
        return count

    def display_count_persons_cannot_buy(self):
        print(f" No pudieron comprar {self.count_persons_cannot_buy()}")


    def display_count_persons_can_buy(self):
        print(f" Pudieron comprar {self.count_persons_can_buy}")
    def persons_cannot_buy_all(self):
        lis=[]
        count = 0
        for person in self.people:
            if person.count_can_buy < person.count_to_buy and person.can_buy:
                lis.append(person)

        return lis
    def count_persons_cannot_buy_all(self):
        return len(self.persons_cannot_buy_all())
    def display_count_persons_cannot_buy_all(self):
        print(f" No pudieron comprar todo lo que pidieron {len(self.persons_cannot_buy_all())}")



    def count_orders(self):
        return len(self.orders)



    def display_count_orders(self):
        print(f" Cantidad de ordenes {self.count_orders()}")


