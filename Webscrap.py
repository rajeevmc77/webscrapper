#!/usr/bin/env python
# coding: utf-8

import time
import classes.MGuruProcessorAsync as mpa
import classes.MGuruProcesor as mp

def main():

    startTime = time.time()
    p = mpa.MGuruProcessorAsync()
    #p = mp.MGuruProcessor()
    p.process()
    duration = time.time() - startTime
    print('Total Time Taken ', duration)


if __name__ == "__main__":
    main()



