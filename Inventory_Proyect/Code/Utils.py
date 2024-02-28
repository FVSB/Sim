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
    def __init__(self, name: str, count: int, start_time: float,process_time: float, count_stock_before: int, count_stock_after: int):
        self.name = name
        self.count = count
        self.start_time = start_time
        self.end_time = 0
        self.process_time = process_time
        self.count_stock_before = count_stock_before
        self.count_stock_after = count_stock_after

