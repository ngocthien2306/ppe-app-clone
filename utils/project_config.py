import os
import json
from pydantic import BaseSettings
from dotenv import load_dotenv

# Get the base directory path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# Load environment variables from the .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Define a Pydantic configuration class
class ProjectConfig(BaseSettings):
    RECTANGLES: list = [(500, 90, 1200, 970)]
    COLORS_MAPPING: dict = {2: (0, 0, 255), 1: (88, 214, 141), 0: (0, 0, 255)}
    WIDTH: int = 1280
    HEIGHT: int = 720
    
    GPIO_SOUND: int = 19
    GPIO_READY: int = 31
    GPIO_RESULT: int = 33
    GPIO_ERROR: int = 35
     
    GPIO_ENZIM: int = 16
    GPIO_MACHINE_RUN: int = 18
    GPIO_OPEN_DOOR: int = 22
    
    TRANSPARENT_SCORE = 0.3
    LINE_AREA_COLOR = (94, 73, 52)
    TIMES_OUTPUT: int = 2
    MODEL_PATH: str = "public/models/yolo/cls_ppe_l.pt"
    ROOT_UI_PATH: str = "public/assets/images/"
    LOG_PATH: str = "public/logs"
    COLLECT_PATH: str = "public/collect"
    ANOTATION_PATH: str = "public/data/annotations.txt"
    CLASSIFY_ENGINE_PATH = "public/models/vit/vit_base_p32_224.py"
    CLASSIFY_ENGINE = "YOLO"
    IMAGE_SIZE = (224, 351)
    
    STATE_INTERLOCK = 0 # Interlock at block -> state = 0, the oposite is None -> state = 1
    STATE_MACHINE = 0 # Machine running 
    STATE_ENZYME = 1 # Enzyme on
    STATE_DOOR = 1 # Close
    
    STATE_BUZER = 1 # on
    STATE_READY = 1 # system ready
    
    
project_config = ProjectConfig()





