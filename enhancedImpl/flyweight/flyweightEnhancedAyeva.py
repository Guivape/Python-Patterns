import random
from enum import Enum


#Ayeva and ksampalis already used new, and a decent implementation this is in table 3.2, 
# TESTING PURPOSES: using color as flyweights key to create more distinct flyweights to test. worked ok

CarType = Enum('CarType', 'subcompact compact suv')

class Car:
    """
    Enhanced Flyweight version of Kasampalis' Car class, 
    now using (car_type, color) as the key in the flyweight pool.
    This means each (car_type, color) combination is reused.
    """

    pool = dict()

    def __new__(cls, car_type, color):
        key = (car_type, color)
        obj = cls.pool.get(key)
        if not obj:
            obj = super().__new__(cls)
            cls.pool[key] = obj
            obj.car_type = car_type
            obj.color = color
        return obj

    def render(self, x, y):
        """
        Render the car at (x, y). 
        Since car_type and color are intrinsic now, 
        they are stored as part of the flyweight's shared state.
        """
        print(f"Render a {self.color} {self.car_type.name} at ({x}, {y})")

def main():
    rnd = random.Random()
    colors = 'white black silver gray red blue brown beige yellow green'.split()
    min_point, max_point = 0, 100
    car_counter = 0

    # Create a number of subcompact cars with random colors
    for _ in range(10):
        c1 = Car(CarType.subcompact, random.choice(colors))
        c1.render(rnd.randint(min_point, max_point), rnd.randint(min_point, max_point))
        car_counter += 1

    # Create a number of compact cars with random colors
    for _ in range(3):
        c2 = Car(CarType.compact, random.choice(colors))
        c2.render(rnd.randint(min_point, max_point), rnd.randint(min_point, max_point))
        car_counter += 1

    # Create a number of SUV cars with random colors
    for _ in range(5):
        c3 = Car(CarType.suv, random.choice(colors))
        c3.render(rnd.randint(min_point, max_point), rnd.randint(min_point, max_point))
        car_counter += 1

    print(f"cars rendered: {car_counter}")
    print(f"cars actually created: {len(Car.pool)}")

    # Demonstrate object identity reuse within the same color and car_type
    c4 = Car(CarType.subcompact, 'red')
    c5 = Car(CarType.subcompact, 'red')
    c6 = Car(CarType.suv, 'blue')
    print(f"{id(c4)} == {id(c5)}? {id(c4) == id(c5)}")
    print(f"{id(c5)} == {id(c6)}? {id(c5) == id(c6)}")

if __name__ == '__main__':
    main()
