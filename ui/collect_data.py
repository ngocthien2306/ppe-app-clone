import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore
from utils.image_utils import center_crop, resize_image
from utils.constant import constant as c
from utils.project_config import project_config as cf
import time
import datetime
import logging
from utils.utils import save_image
from utils.logging import CustomLoggerConfig
import threading
import os
from core.model_handler import logic

    
class CollectWindow(QMainWindow):
    
    def __init__(self, start_yn=True):
        super().__init__()
        
        self._logic = logic
        self.logger = CustomLoggerConfig.configure_logger()
        self.detect_yn = False
        self.simulate_yn = False
        self.inference_yn = False
        self.sound_yn = False
        self.frame_crop = None


        self.init_main_window()

        # Create a container widget to hold camera and button
        container_widget = QWidget(self)
        container_layout = QHBoxLayout(container_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        # Create a QLabel to display the camera feed
        self.camera_label = QLabel(self)

        button_layout = QHBoxLayout()

        self.home_btn = QPushButton("", self)
        self.home_btn.setFixedHeight(150)
        self.home_btn.setFixedWidth(216)
        # self.home_btn.setEnabled(False)
        self.home_btn.clicked.connect(self.show_home)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.enable_home_button)
        
        button_layout.addWidget(self.home_btn, alignment=QtCore.Qt.AlignLeft)
        button_layout.setContentsMargins(10, 30, 10, 10)

        # Create the second additional button and set its properties
        self.info_data_label = QLabel(self.count_sample_text(), self)
        font = QFont()
        font.setPointSize(20)
        self.info_data_label.setFont(font)
        self.info_data_label.setFixedHeight(132)
        self.info_data_label.setFixedWidth(256)
        

        # Add the second button to the layout
        # button_layout.addWidget(self.simulate_btn)

        # Set up the camera_label layout
        camera_layout = QVBoxLayout(self.camera_label)
        camera_layout.addLayout(button_layout)
        camera_layout.addStretch(1)  # Add stretch to push buttons to the top

        container_layout.addWidget(self.camera_label, 4)
        spacer_item = QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        container_layout.addItem(spacer_item)
        
        # Create buttons
        self.pass_button = QPushButton("", self)
        self.fail_button = QPushButton("", self)

        # Set attributes for Pass button
        self.pass_button.setEnabled(True)
        self.pass_button.setFixedHeight(216)
        self.pass_button.setFixedWidth(256)
        self.pass_button.clicked.connect(self.pass_action)

        # Set attributes for Fail button
        self.fail_button.setEnabled(True)
        self.fail_button.setFixedWidth(256)
        self.fail_button.setFixedHeight(216)
        self.fail_button.clicked.connect(self.fail_action)

        # Create horizontal layout and add buttons to it
        self.button_layout = QVBoxLayout()
        # self.button_layout.addSpacing(10)
        self.button_layout.addWidget(self.info_data_label, alignment=QtCore.Qt.AlignCenter)
        self.button_layout.addSpacing(250)
        self.button_layout.addWidget(self.pass_button, alignment=QtCore.Qt.AlignCenter)
        self.button_layout.addSpacing(30)
        self.button_layout.addWidget(self.fail_button, alignment=QtCore.Qt.AlignCenter)
        self.button_layout.addSpacing(10)
        container_layout.addLayout(self.button_layout, 1)  # 1/5 of the space for the button

        # Set the container widget as the central widget
        self.setCentralWidget(container_widget)

        self.update_button_styles()
        if start_yn:
            self.init_camera()
            self.start_timer()
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Left mouse button double-clicked")
            self.close()
        elif event.button() == Qt.RightButton:
            print("Right mouse button double-clicked")
    
    def show_home(self):
        self.home_btn.setEnabled(False)
        # Start the timer to enable the button after 5000 milliseconds (5 seconds)
        self.timer.start(5000)
        self.camera.release()
        self.timer.stop()
        from ui.home import HomeWindow
        home_window = HomeWindow(start_yn=False)
        home_window.show()
        home_window.raise_()
        home_window.showFullScreen()
        home_window.init_camera()
        home_window.start_timer()
        self.close()

    def enable_home_button(self):
        # Enable the button when the timer times out
        self.home_btn.setEnabled(True)
        self.timer.stop()

    def pass_action(self):
        img_path = os.path.join(cf.COLLECT_PATH, 'ok', f"{time.time()}_pass.png")
        cv2.imwrite(img_path, self.frame_crop)
        self.update_simulate_button_text()

    def fail_action(self):
        img_path = os.path.join(cf.COLLECT_PATH, 'ng', f"{time.time()}_fail.png")
        cv2.imwrite(img_path, self.frame_crop)
        self.update_simulate_button_text()

    def update_simulate_button_text(self):
        self.info_data_label.setText(self.count_sample_text())

    def count_sample_text(self):
        import glob
        fail_list_paths = glob.glob(os.path.join(cf.COLLECT_PATH, 'ng', '*.png'))
        pass_list_paths = glob.glob(os.path.join(cf.COLLECT_PATH, 'ok', '*.png'))
        return " Pass: {0} \n Fail: {1}".format(str(len(pass_list_paths)), str(len(fail_list_paths)))

    def init_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        
    def init_main_window(self):
        width = 1080
        aspect_ratio = 9 / 16  # 9:16
        height = int(width / aspect_ratio)
        self.setGeometry(0, 0, width, height)
        self.setStyleSheet(c.BACKGROUND_PATH)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
    
    def update_button_styles(self):
        self.home_btn.setStyleSheet(c.DETECT_PATH)
        self.pass_button.setStyleSheet(c.PASS_PATH)
        self.fail_button.setStyleSheet(c.FAIL_PATH)
    
    def start_timer(self):
        time.sleep(3)
        self.timer.start(16)  # Update every 33 milliseconds (approximately 30 fps)

          
    def update(self):
        try: 
            size = self.camera_label.size()
            size_list = [size.width(), size.height()]
            ret, frame = self.camera.read()
            if ret:
                output_frame, frame_crop, is_wrong = self._logic.update(frame, size_list, self.detect_yn, True)
                self.frame_crop = frame_crop.copy()
                self.show_image(output_frame)
                    
            else:
                print('Failed to read from the camera. Trying to reconnect...')
                # Release the previous camera instance
                self.camera.release()
                # Introduce a short delay before retrying
                time.sleep(5)
                # Try to connect to the camera again
                self.camera = cv2.VideoCapture(0)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                
        except Exception as e:
            self.logger.error(f"Exception durring update frame: {e}", exc_info=True)
    
    def show_image(self, output_frame):
        height, width, _ = output_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(output_frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        self.camera_label.setPixmap(QPixmap.fromImage(q_image))
    
    def closeEvent(self, event):
        # Stop the camera when the application is closed
        self.camera.release()
        self.timer.stop()
        super().closeEvent(event)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
            

            
        