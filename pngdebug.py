from PIL import Image
import sys
import os

def fix_image_srgb_profile(file_path):
    img = Image.open(file_path)
    img.save(file_path, icc_profile=None)

# fix_image_srgb_profile('images/STAR.png')
def get_resource_path(relative_path):
    """处理路径问题"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


