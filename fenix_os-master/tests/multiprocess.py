from multiprocessing import Process, Queue, TimeoutError
import time


def FirstSonStarter():
    print 'Lancement processus 1'


def SecondSonStarter():
    print("Lancement processus 2")

def LaunchProcess():

    son1 = Process(target=FirstSonStarter)
    son2 = Process(target=SecondSonStarter)

    son1.start()
    son2.start()

    time.sleep(2)

    son1.join()
    son2.join()

    print("C'est la fin")

if __name__ == '__main__':
    LaunchProcess()
