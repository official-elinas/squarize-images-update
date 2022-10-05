# @title pad squarize images
import os
import argparse

import glob
from natsort import natsorted
from tqdm import tqdm
import cv2
import numpy as np

# from IPython.display import clear_output

parser = argparse.ArgumentParser()
parser.add_argument("--voc", type=int, default=False, help="activate edgedetection", )
opt = parser.parse_args()

if opt.voc:
    visions_path = os.path.expanduser('~\Documents\\visions of chaos')
else:
    visions_path = os.path.expanduser('~\Documents')

extract_from = "folder"
path_to_input_images = visions_path + "/tmpsquarize/resizedimages/"
path = path_to_input_images

if not os.path.exists(path):
    raise Exception("folder doesn't exist, please check it.")
# if extract_from=="zip":
#  shutil.unpack_archive("/content/inputs","zip",path)
#  path="/content/inputs/"
else:
    if not path.endswith("/"): path += "/"

c = 0
files = glob.glob(path + "*")
files = natsorted(files)

padded_folder = visions_path + "/tmpsquarize/padded_imgs-masks/"

print("Preprocessing images")

dirs = os.listdir(path)

for image in tqdm(files):

    i = cv2.imread(image)
    size = i.shape
    h, w = size[0], size[1]
    if w > h:
        newim = np.zeros((w, w, 3), dtype=np.uint8)
        newim[:, :] = 255
        pad = int((w - h) / 2)
        padpad = int(w * 0.04)
        newim[pad:w - pad, 0:w] = 0
        newim[:, :] = 255
        # cv2.imwrite("/content/temp/"+str(c)+"_mask.png",newim)
        if pad > ((w - h) / 2):
            newim[pad - 1:w - pad, 0:w] = i[:, :]
        elif pad < ((h - w) / 2):
            newim[pad + 1:w - pad, 0:w] = i[:, :]
        # else:
        # newim[pad+1:w-pad,0:w]=i[:,:]
        else:
            newim[pad:w - pad, 0:w] = i[:, :]
        cv2.imwrite(padded_folder + str(c) + ".png", newim)
    else:
        newim = np.zeros((h, h, 3), dtype=np.uint8)
        newim[:, :] = 255
        pad = int((h - w) / 2)
        newim[0:h, pad:h - pad] = 0
        # cv2.imwrite("/content/temp/"+str(c)+"_mask.png",newim)
        newim[:, :] = 255
        if pad > ((h - w) / 2):
            newim[0:h, pad - 1:h - pad] = i[:, :]
        elif pad < ((h - w) / 2):
            newim[0:h, pad + 1:h - pad] = i[:, :]
        else:
            newim[0:h, pad:h - pad] = i[:, :]
        cv2.imwrite(padded_folder + str(c) + ".png", newim)
    c = c + 1
    Exception("hi")
print("masks half done...")
