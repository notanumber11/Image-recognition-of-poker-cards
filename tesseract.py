import cv2
import numpy as np
from PIL import Image
from pytesseract import image_to_string
import pytesseract as tesseract

class OCR:

    font = cv2.FONT_HERSHEY_SIMPLEX
    idColour = (0, 255, 0)

    def __init__(self):
        pass

    def detectCharacter(self,img,sample,offSetX,offSetY):


        vis = np.concatenate((sample.img,sample.img), axis=1)
        vis = np.concatenate((vis, vis), axis=1)
        vis = np.concatenate((vis, vis), axis=1)

        cv2_im = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

        cv2_im = cv2.cvtColor(sample.img, cv2.COLOR_BGR2RGB)


        pil_im = Image.fromarray(cv2_im)
        # print image_to_string(Image.open('test.png'))
        result = []
        result = image_to_string(pil_im, lang='eng',config="-c tessedit_char_whitelist=01234567890AJQK -psm 6")
        if len(result) > 0:
            cv2.putText(img, result[0], (offSetX, offSetY), self.font, 0.6, self.idColour, 2, cv2.LINE_AA)
            print 'Detectado ' + result
            cv2.imshow("test",sample.img)
            cv2.waitKey()
        # if len (result) > 0 and ((ord(result[0])>47 and ord(result[0])< 58) or (ord(result[0])>64 and ord(result[0])< 91)):
        #

            return result[0]
        return None



    def init_ocr(self):
        """ 
        .. py:function:: init_ocr()

            Utilize the Tesseract-OCR library to create an tesseract_ocr that 
            predicts the numbers to be read off of the meter. 

            :return: tesseract_ocr Tesseracts OCR API.
            :rtype: Class
        """
        # Initialize the tesseract_ocr with the english language package.
        LANGUAGE = "eng"
        CHARACTERS = "0123456789"
        FALSE = "0"
        TRUE = "1"
        tesseract_ocr = tesseract.TessBaseAPI()
        tesseract_ocr.Init(LANGUAGE,
                           tesseract.OEM_DEFAULT)

        # Limit the characters being seached for to numerics.
        tesseract_ocr.SetVariable("tessedit_char_whitelist", CHARACTERS)

        # Set the tesseract_ocr to predict for only one character.
        tesseract_ocr.SetPageSegMode(tesseract.PSM_AUTO)

        # Tesseract's Directed Acyclic Graph.
        # Not necessary for number recognition.
        tesseract_ocr.SetVariable("load_system_dawg", FALSE)
        tesseract_ocr.SetVariable("load_freq_dawg", FALSE)
        tesseract_ocr.SetVariable("load_number_dawg", TRUE)

        tesseract_ocr.SetVariable("classify_enable_learning", FALSE)
        tesseract_ocr.SetVariable("classify_enable_adaptive_matcher", FALSE)

        return tesseract_ocr

    def detectCharacter(self,pathImg):
        img = cv2.imread(pathImg)
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        result = image_to_string(pil_im, lang='eng',config="-c tessedit_char_whitelist=01234567890AJQK -psm 6")

        cv2.putText(img, result, (200, 200), 0, 1, (0, 255, 0))
        for c in result:
            print str(c)
            # cv2.putText(img,result[i],(80,80),0,1,(0,255,0))

        cv2.imshow("test", img)
        cv2.waitKey()