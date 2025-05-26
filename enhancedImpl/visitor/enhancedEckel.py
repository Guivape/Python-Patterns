from __future__ import generators
import random
from multipledispatch import dispatch

class Flower:
    def accept(self, visitor):
        visit(self, visitor) 

    def pollinate(self, pollinator):
        print(self, "pollinated by", pollinator)

    def eat(self, eater):
        print(self, "eaten by", eater)

    def __str__(self):
        return self.__class__.__name__

class Gladiolus(Flower): pass
class Runuculus(Flower): pass
class Chrysanthemum(Flower): pass
class Visitor:
    def __str__(self):
        return self.__class__.__name__

class Bug(Visitor): pass
class Pollinator(Bug): pass
class Predator(Bug): pass

class Bee(Pollinator): pass
class Fly(Pollinator): pass
class Worm(Predator): pass

# === Multiple dispatch for visit logic ===

@dispatch(Gladiolus, Bee)
def visit(flower, bee):
    flower.pollinate(bee)

@dispatch(Runuculus, Bee)
def visit(flower, bee):
    flower.pollinate(bee)

@dispatch(Chrysanthemum, Bee)
def visit(flower, bee):
    flower.pollinate(bee)

@dispatch(Flower, Fly)
def visit(flower, fly):
    flower.pollinate(fly)

@dispatch(Flower, Worm)
def visit(flower, worm):
    flower.eat(worm)

# fallback
@dispatch(Flower, Bug)
def visit(flower, bug):
    print(f"No specific interaction between {flower} and {bug}")


def flowerGen(n):
    for _ in range(n):
        yield random.choice(Flower.__subclasses__())()

bee = Bee()
fly = Fly()
worm = Worm()

for flower in flowerGen(10):
    flower.accept(bee)
    flower.accept(fly)
    flower.accept(worm)
