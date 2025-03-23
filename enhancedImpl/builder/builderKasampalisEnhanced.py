import time
from enum import Enum

PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')
PizzaDough = Enum('PizzaDough', 'thin thick')
PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')
PizzaTopping = Enum('PizzaTopping', 
                    'mozzarella double_mozzarella bacon ham mushrooms red_onion oregano')

STEP_DELAY = 3  # seconds, just like in the original

class Pizza:
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        return self.name

class PizzaBuilder:
    def __init__(self, style):
        self.pizza = Pizza(style["name"])
        self.dough_type = style["dough"]
        self.sauce_type = style["sauce"]
        self.topping_info = style["topping_info"]    
        self.topping_list = style["topping_list"]    
        self.baking_time = style["baking_time"]
        self.progress = PizzaProgress.queued

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        print(f'preparing the {self.dough_type.name} dough of your {self.pizza}...')
        time.sleep(STEP_DELAY)
        self.pizza.dough = self.dough_type
        print(f'done with the {self.dough_type.name} dough')
        return self

    def add_sauce(self):
        print(f'adding the {self.sauce_type.name.replace("_", " ")} sauce to your {self.pizza}...')
        time.sleep(STEP_DELAY)
        self.pizza.sauce = self.sauce_type
        print(f'done with the {self.sauce_type.name.replace("_", " ")} sauce')
        return self

    def add_topping(self):
        print(f'adding the topping ({self.topping_info}) to your {self.pizza}')
        time.sleep(STEP_DELAY)
        self.pizza.toppings.extend(self.topping_list)
        print(f'done with the topping ({self.topping_info})')
        return self

    def bake(self):
        self.progress = PizzaProgress.baking
        print(f'baking your {self.pizza} for {self.baking_time} seconds')
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print(f'your {self.pizza} is ready')
        return self

    def get_pizza(self):
        return self.pizza

class Waiter:
    def __init__(self):
        self.builder = None

    def construct_pizza(self, style_dict):
        self.builder = (
            PizzaBuilder(style_dict)
            .prepare_dough()
            .add_sauce()
            .add_topping()
            .bake()
        )
        return self.builder.get_pizza()

def main():
    pizza_styles = {
        "m": {
            "name": "margarita",
            "dough": PizzaDough.thin,
            "sauce": PizzaSauce.tomato,
            "topping_info": "double mozzarella, oregano",
            "topping_list": [PizzaTopping.double_mozzarella, PizzaTopping.oregano],
            "baking_time": 5
        },
        "c": {
            "name": "creamy bacon",
            "dough": PizzaDough.thick,
            "sauce": PizzaSauce.creme_fraiche,
            "topping_info": "mozzarella, bacon, ham, mushrooms, red onion, oregano",
            "topping_list": [
                PizzaTopping.mozzarella,
                PizzaTopping.bacon,
                PizzaTopping.ham,
                PizzaTopping.mushrooms,
                PizzaTopping.red_onion,
                PizzaTopping.oregano
            ],
            "baking_time": 7
        }
    }

    valid_input = False
    while not valid_input:
        choice = input("What pizza would you like, [m]argarita or [c]reamy bacon? ")
        if choice in pizza_styles:
            valid_input = True
        else:
            print("Sorry, only margarita (key m) and creamy bacon (key c) are available")

    waiter = Waiter()
    print()
    pizza = waiter.construct_pizza(pizza_styles[choice])
    print()
    print(f"Enjoy your {pizza}!")

if __name__ == "__main__":
    main()
