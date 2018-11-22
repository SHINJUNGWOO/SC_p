import cv2
import numpy as np

class process_video:
    def __init__(self,vidname,clear_val=False,unsharp=False):
        self.vidfilename=vidname
        self.pMOG2=cv2.createBackgroundSubtractorMOG2(40,40,False)
        self.frame=None
        self.fgMaskMOG2=None
        self.video_out_dir='./output.mp4'
        self.picture_out_dir="./test_d/picture"

        self.clear=clear_val
        self.unsharp=unsharp

        # 기초 코드




    def processVideo(self):

        self.capture = cv2.VideoCapture(self.vidfilename)
        self.full_frame=full=int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

        self.frame_width =int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.vFourcc =self.capture.get(cv2.CAP_PROP_FOURCC)
        # 기초 코드


        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(self.video_out_dir,self.fourcc, 30.0, (self.frame_width,self.frame_height))

        while (int(self.capture.get(1))<full):
            try:
                ret,self.frame=self.capture.read()
                self.kernel1=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,ksize=(5,5))
                self.kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5, 5))

                self.backgroundImage=None
                self.fgMaskMOG2=self.pMOG2.apply(self.frame)
                self.backgroundImage=self.pMOG2.getBackgroundImage()

                self.img1=None
                self.img2 = None

                self.img1=cv2.erode(self.fgMaskMOG2,self.kernel1)
                self.img2=cv2.dilate(self.img1,self.kernel2)

                self.foregroundImgage=self.img2


                if self.clear==True:
                    test_k = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                    self.backgroundImage = cv2.filter2D(self.backgroundImage, -1, test_k)

                if self.unsharp !=False:
                    #unsharp가 1.5에서 2.5로 들어감, Default가
                    gaussian_3 = cv2.GaussianBlur(self.backgroundImage, (9, 9), 10.0)
                    self.backgroundImage = cv2.addWeighted(self.backgroundImage, self.unsharp, gaussian_3, -0.5, 0, self.backgroundImage)



                # cv2.imshow("HI",self.backgroundImage)
                # cv2.imshow("HI2", self.frame)
                self.video.write(self.backgroundImage)

                if int(self.capture.get(1))%10==0:
                    cv2.imwrite(filename=self.picture_out_dir+"Picture_%d.png"%(int(self.capture.get(1))//10),img=self.backgroundImage)
                if cv2.waitKey(2) & 0xff == 27:
                    break
            except:
                return -1

