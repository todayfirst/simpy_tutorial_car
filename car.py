import simpy
def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)
        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until = 15)

print("end")
class Car(object):
     def __init__(self, env):
         self.env = env
         # Start the run process everytime an instance is created.
         self.action = env.process(self.run())

     def run(self):
         while True:
             print('Start parking and charging at %d' % self.env.now)
             charge_duration = 5
             # We yield the process that process() returns
             # to wait for it to finish
             yield self.env.process(self.charge(charge_duration))

             # The charge process has finished and
             # we can start driving again.
             print('Start driving at %d' % self.env.now)
             trip_duration = 2
             yield self.env.timeout(trip_duration)

     def charge(self, duration):
         yield self.env.timeout(duration)


def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()

env = simpy.Environment()
car = Car(env)
env.run(until=15)

#######
import simpy


def clock(env, name, tick):


    while True:

        yield env.timeout(tick)
        print(name, env.now)


env = simpy.Environment()
env.process(clock(env, 'fast', 0.5))
env.process(clock(env, 'slow', 1))

env.run(until=2)


#######

class Car(object):
     def __init__(self, env):
         self.env = env
         self.action = env.process(self.run())

     def run(self):
         while True:
             print('Start parking and charging at %d' % self.env.now)
             charge_duration = 5
             # We may get interrupted while charging the battery
             try:
                 yield self.env.process(self.charge(charge_duration))
             except simpy.Interrupt:
                 # When we received an interrupt, we stop charging and
                 # switch to the "driving" state
                 print('Was interrupted. Hope, the battery is full enough ...')

             print('Start driving at %d' % self.env.now)
             trip_duration = 2
             yield self.env.timeout(trip_duration)

     def charge(self, duration):
         yield self.env.timeout(duration)

def driver(env, car):
    while True:
        yield env.timeout(3)
        car.action.interrupt()

env = simpy.Environment()
car = Car(env)
env.process(driver(env, car))
env.run(15)
