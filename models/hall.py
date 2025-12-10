from abc import ABC, abstractmethod

# ABSTRACTION: Abstract Base Class
class Hall(ABC):
    def __init__(self, id, name, rows, cols):
        self.id = id
        self.name = name
        self.rows = rows
        self.cols = cols

    @abstractmethod
    def get_base_price(self):
        pass

    def get_capacity(self):
        return self.rows * self.cols

# INHERITANCE: StandardHall IS-A Hall
class StandardHall(Hall):
    def get_base_price(self):
        return 350.00

# INHERITANCE: IMAXHall IS-A Hall
class IMAXHall(Hall):
    def get_base_price(self):
        # POLYMORPHISM: Different behavior for same method name
        return 750.00 

class VIPHall(Hall):
    def get_base_price(self):
        return 550.00

# Factory Pattern to create the right object from DB data
def hall_factory(id, name, rows, cols):
    name_upper = name.upper()
    if "IMAX" in name_upper:
        return IMAXHall(id, name, rows, cols)
    elif "VIP" in name_upper or "LUXE" in name_upper:
        return VIPHall(id, name, rows, cols)
    else:
        return StandardHall(id, name, rows, cols)