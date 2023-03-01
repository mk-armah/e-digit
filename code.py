
import argparse
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
import numpy as np
import cv2
import qrcode


class QrCode:

    def __init__(self) -> None:

        self.outer_image = "./designs/qr-code-frame6.png"
        self.enc_ratio = 1.82
        self.embeded_image = "./designs/embedded_logo.png"
        self.text_embedding = 'https://github.com/mk-armah'
        self.filedir = "./samples"
        self.qrcode_name = "chael.ai"
        self.size = (512,512)


    def make_qr(self,text:str,embedded_image_path:str | None = None):

        qr = qrcode.QRCode(version= 15)
        
        qr.add_data(text)
        
        if embedded_image_path is not None:
            img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=embedded_image_path)
        else:
            img = qr.make_image()

        return img


    def show_image(img):
        """Display image with Open cv
        Args:
            img : the image to display
        Return:
            None, just a image frame will be displayed to the screen"""

        cv2.imshow("image",cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        
        cv2.waitKey(0)
        
        cv2.destroyAllWindows()


    def add_enclosure(qr_img, enc_img_path:str = r"./designs/qr-code-frame6.png", ratio:float = 1.8):
        """"
        Enclose Generated QR-code image in a frame.

        Args :
                ratio -> int|float, default is 1.8, increases the size of the frame 1.8 times the 
                embedded image size

            Returns :
                    PILImage, a qrcode image enclosed in a frame.
        """

        outer_frame = Image.open(enc_img_path).resize(
            (np.array(qr_img.size)*ratio).astype(int)
            )

        outer_frame = outer_frame.convert("RGB")

        qr_img = qr_img.convert("RGB")

        pos = ((outer_frame.size[0] - qr_img.size[0]) // 2, (outer_frame.size[1] - qr_img.size[1]) // 2)
        
        outer_frame.paste(qr_img, pos)
        
        return outer_frame
