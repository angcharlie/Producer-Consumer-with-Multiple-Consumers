"""
 Charlie Ang
 CSC 4800 Python Applications Programming
 Lab # 7 Producer/Consumer with Multiple Consumers
 Dr. Tindall
 February 27, 2017

 This program is a producer/consumer with any number of consumer threads which can process
 or consume more than one item from the Queue at any given moment.
"""
#!/usr/bin/env python
# Chun Example 4-12, changes by mht

from random import randrange
from time import sleep
from queue import Queue
from myThread3 import MyThread

NITEMS = 10                                         # number of items to be produced
NREADERS = 3                                        # number of readers (consumers)
WRITERDELAY = float(2)                              # delay time between items

WRITERFINISHED = False                              # global variable producer modifies and consumer checks
                                                    # True when writer (producer) has finished its operations

 # writing item into the queue (producer)
def writeQ(queue, item):
    print('Writer producing object %d for Q...' % item, end='')
    queue.put(item, True)
    print("size now", queue.qsize())

#reading item from queue (consumer)
def readQ(queue, threadName):
    if(WRITERFINISHED == True and queue.qsize() == 0):  # end of prod-cons processing
        return None                                       # exit thread

    try:                                            # wrtierfinished == FALSE (producer not done)
        val = queue.get(False)                      # non-blocking operation; returns next val or throws exception
        print('   ', threadName, 'consumed object %d from Q... size now' % val, queue.qsize())
        sleep(1)
        return val
    except:                                         # queue is empty
        print('   ', threadName, 'polling empty queue')

def writer(queue, loops):
    for i in range(loops):
        writeQ(queue, i)
        #sleep(randrange(1, 3)) #1-2 sec
        sleep(float(WRITERDELAY))                   # delay specified # sec between items

    global WRITERFINISHED
    WRITERFINISHED = True                           # producer finishes its normal operations

def reader(queue, loops, threadName):
    for i in range(loops):
        item = readQ(queue, threadName)
        if (item == -1):
            return                                  # exit thread
        sleep(3)


funcs = [writer]
for i in range(0, int(NREADERS)):                   #0-2 for 3 readers
    funcs.append(reader)
nfuncs = range(len(funcs))  # length of funcs

def main():
    nloops = NITEMS
    q = Queue(32)

    threads = []
    for i in nfuncs:                                # putting writers and readers into thread
        if (i == 0):    # writer
            t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
            threads.append(t)
        else:           # reader
            t = MyThread(funcs[i], (q, nloops, 'Reader-{}'.format(i - 1)), funcs[i].__name__)
            threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print('all DONE')

if __name__ == '__main__':
    main()
