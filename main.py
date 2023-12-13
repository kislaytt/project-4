from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class KivyCamera(Image):
    def is_point_overlapping_background(frame, point1, point2, point3, background_color_range):
    # Extract the color of the pixel at the specified point
        pixel_color1 = frame[point1[1], point1[0]]
        pixel_color2 = frame[point2[1], point1[0]]
        pixel_color3 = frame[point3[1], point1[0]]
        
        # Check if the color of the pixel is within the specified background color range
        is_overlapping1 = all(background_color_range[0] <= pixel_color1) and all(pixel_color1 <= background_color_range[1])
        is_overlapping2 = all(background_color_range[0] <= pixel_color2) and all(pixel_color2 <= background_color_range[1])
        is_overlapping3 = all(background_color_range[0] <= pixel_color3) and all(pixel_color3 <= background_color_range[1])
        print(pixel_color1)
        print(pixel_color2)
        print(pixel_color3)
        if is_overlapping1 and is_overlapping2 and is_overlapping3:
            return True, pixel_color2
        else:
            return False, None


    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        width  = self.capture.get(3)  # float `width`
        height = self.capture.get(4)  # float `height`
        width=int(width)
        height=int(height)
        box_width = int(width * 0.60)# 2:1 ratio (2/3 and 1/3 of the imagewidth)
        margin = (width - box_width) // 2
        box_height = int(box_width // 2)
        margin_x = (width - box_width) // 2
        margin_y = (height - box_height) // 2

        background_color_range = ((0, 0, 0), (50, 50, 50))

        ret, frame = self.capture.read()
        image = frame.copy()

        

        
        if ret:
            # convert it to texture

            '''buf1 = cv2.flip(frame, 0)
            buf1 = cv2.line(frame, (80,60), (80, 100), (0,255,0), 5)'''
            thickness = 2
            color = (0, 255, 0)
            image= cv2.line(image,(margin_x,margin_y), (margin_x,margin_y+20), color, thickness) 
            image= cv2.line(image,(margin_x,margin_y), (margin_x+20,margin_y), color, thickness)

            image= cv2.line(image,(margin_x+box_width,margin_y), (margin_x+box_width,margin_y+20), color, thickness)
            image= cv2.line(image,(margin_x+box_width,margin_y), (margin_x+box_width-20,margin_y), color, thickness)

            image= cv2.line(image,(margin_x,margin_y+box_height), (margin_x,margin_y+box_height-20), color, thickness) 
            image= cv2.line(image,(margin_x,margin_y+box_height), (margin_x+20,margin_y+box_height), color, thickness)

            image= cv2.line(image,(margin_x+box_width,margin_y+box_height), (margin_x+box_width,margin_y+box_height-20), color, thickness) 
            image= cv2.line(image,(margin_x+box_width,margin_y+box_height), (margin_x+box_width-20,margin_y+box_height), color, thickness)
            topLeft_point1 = (margin_x, margin_y)
            topLeft_point2 = (margin_x, margin_y+20)
            topLeft_point3 = (margin_x+20, margin_y)

            topRight_point1 = (margin_x+box_width,margin_y)
            topRight_point2 = (margin_x+box_width,margin_y+20)
            topRight_point3 = (margin_x+box_width-20,margin_y)

            bottomLeft_point1 = (margin_x,margin_y+box_height)
            bottomLeft_point2 = (margin_x,margin_y+box_height-20)
            bottomLeft_point3 = (margin_x+20,margin_y+box_height)

            bottomRight_point1 = (margin_x+box_width,margin_y+box_height)
            bottomRight_point2 = (margin_x+box_width,margin_y+box_height-20)
            bottomRight_point3 = (margin_x+box_width-20,margin_y+box_height)

            result1, background_color_at_point = KivyCamera.is_point_overlapping_background(frame, topLeft_point1,topLeft_point2, topLeft_point3, background_color_range)
            result2, background_color_at_point = KivyCamera.is_point_overlapping_background(frame, topRight_point1,topRight_point2, topRight_point3, background_color_range)
            result3, background_color_at_point = KivyCamera.is_point_overlapping_background(frame, bottomRight_point1,bottomRight_point2, bottomRight_point3, background_color_range)
            result4, background_color_at_point = KivyCamera.is_point_overlapping_background(frame, bottomLeft_point1,bottomLeft_point2, bottomLeft_point3, background_color_range)
            
            if result1 and result2 and result3 and result4:
                print("Does the pixel at the specified point overlap the specified background color range?", True)
                print(f"Background color at the specified point: {background_color_at_point}")
            else:
                print(print("Does the pixel at the specified point overlap the specified background color range?", False))
            buf = image.tobytes()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()