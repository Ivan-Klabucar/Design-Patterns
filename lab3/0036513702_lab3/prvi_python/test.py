#PRVI PYTHON
import os
from importlib import import_module

def myfactory(module):
    m = import_module('.'+module, package='plugins')
    return getattr(m, module.capitalize())

def printGreeting(pet):
    print(f'{pet.name()} pozdravlja: {pet.greet()}')

def printMenu(pet):
    print(f'{pet.name()} voli: {pet.menu()}')

def test():
    pets=[]
    # obiđi svaku datoteku kazala plugins 
    for mymodule in os.listdir('plugins'):
        moduleName, moduleExt = os.path.splitext(mymodule)
        # ako se radi o datoteci s Pythonskim kodom ...
        if moduleExt=='.py':
            # instanciraj ljubimca ...
            ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
            # ... i dodaj ga u listu ljubimaca
            pets.append(ljubimac)

    # ispiši ljubimce
    for pet in pets:
        printGreeting(pet)
        printMenu(pet)

test()

# py3 test.py 
# Ljubimac 0 pozdravlja: Mijau!
# Ljubimac 0 voli: mlako mlijeko.
# Ljubimac 1 pozdravlja: Sto mu gromova!
# Ljubimac 1 voli: brazilske orahe.