import random 
import simpy 

rushhours = 120 # From 6AM to 8AM
interarrival_time = 0.5 # Suppose that students arrive at every 30 seconds
service_time = 3*2 #1.7 KM from the motorcycle taxi stand to the school 

def input_for_rider():
    num_rider = int(input("Set the number of rider(s) avaliable: "))
    if num_rider > 0:
        num_rider = num_rider
    else:
        print("Cannot have less than 1 rider. Use default number of rider = 1")
        num_rider = 1
    return num_rider

def main():
    random.seed(19233)                 
    env=simpy.Environment()
    rider= simpy.Resource(env, capacity=input_for_rider())
    env.process(queue_generator(env,rider))
    env.run(until = rushhours)

class motorcycletaxistand(object): 
    def __init__(self,env,rider,student,time): 
        self.env=env 
        self.rider = rider
        self.student_counter = student
        self.arrival_time = time
        
        print('Student %s arrived motorcycle taxi stand at %0.2f' %(self.student_counter, self.arrival_time)) 
        
        env.process(self.service())

    def service(self): 
        ride_request = self.rider.request()
        yield ride_request
        print('Student %s waited %0.2f minutes, get on the motorcycle at %0.2f' %(self.student_counter , self.env.now-self.arrival_time, self.env.now))    
        
        service_mean = random.expovariate(1/service_time)
        yield self.env.timeout(service_mean) 

        print('\t the student %s motorcycle taxi service takes %0.2f minutes' %(self.student_counter,service_mean/2))
        print('\t Student %s reached the school at %0.2f' %(self.student_counter,self.env.now))
        
        self.rider.release(ride_request)
          
def queue_generator(env,rider):  
    num = 0
    motorcycletaxistand(env, rider, num, env.now)
    while True:       
        num += 1
        IAT = random.expovariate (1/interarrival_time)
        yield env.timeout(IAT)                                           
        motorcycletaxistand(env, rider, num, env.now) 
    
if __name__ == '__main__':
    main()
    
    
# Thank you to examples on SimPy documentation and the RealPython tutorial and to my teacher, Mr. Berdinsky
# By 6305574 Wuttada Rungseesantivanon
