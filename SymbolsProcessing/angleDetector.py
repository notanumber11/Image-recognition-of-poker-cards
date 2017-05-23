from MachineLearning.knearest import knearest
from MachineLearning.roi_detector import RoiDetector


class AngleDetector:



    def __init__(self):
        self.roiDetector = RoiDetector(heightThreshold=20, areaThreshold=100)
        self.knnHearts = knearest('MachineLearning/AngleTraining/hearts_360.data','MachineLearning/AngleTraining/angles.data')

    def obtainAngle(self,listSamples):
        for sample in listSamples:
            if(sample.label == 'H'):
                self.knnHearts.applyKnearestToSample(self.roiDetector, sample)


