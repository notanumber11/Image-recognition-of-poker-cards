from __future__ import division
import numpy as np


class RefinateDecission():

    bigThreshold = 0.45


    def __init__(self):
        pass

    def refinateDecission(self,samples):

        mean,std = self.obtainMeanStd(samples)

        smalSamples = []
        if( std/mean > self.bigThreshold):
            print 'removing big symbols... '
            for s in samples:
                if(s.rectangleArea  < mean   ):
                    smalSamples.append(s)

            return  smalSamples

        return samples




    def obtainMeanStd(self,samples):
        sizes = []
        length = len(samples)
        start = int(0.2*length)
        end = int(0.8*length)

        start = 0
        print start,end

        for i in range(start,end):
            sizes.append(samples[i].rectangleArea)


        sizes = np.array(sizes)
        print sizes
        mean = np.mean(sizes)
        std = np.std(sizes)
        print mean,std,std/mean
        return mean,std