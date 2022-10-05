import os
import argparse

import PIL
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--voc", type=int, default=False, help="activate edge detection")
opt = parser.parse_args()

if opt.voc:
    visions_path = os.path.expanduser('~\Documents\\visions of chaos')
else:
    visions_path = os.path.expanduser('~\Documents')
path_to_input_images = visions_path + "/tmpsquarize/resizedimages/"
path = path_to_input_images
dirs = os.listdir(path)


def resize2():
    for item in dirs:
        if os.path.isfile(path + item):
            img = Image.open(path + item)
            # get width and height
            w = img.width
            h = img.height
            print("The height of the image is: ", img.height)
            print("The width of the image is: ", img.width)
            if img.width > img.height:
                new_width = 512
                img = Image.open(path + item)
                new_height = int(new_width * h / w)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                img.save(path + item)
            if img.height > img.width:
                new_height = 512
                img = Image.open(path + item)
                new_width = int(new_height * w / h)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                img.save(path + item)
                # return size
                print("next")


resize2()


def resize():
    for item in dirs:
        if os.path.isfile(path + item):
            image = Image.open(path + item).convert("RGB")
            f, e = os.path.splitext(path + item)
            # imResize = image.resize((200,200), Image.ANTIALIAS)
            # imResize.save(f + ' resized.jpg', 'JPEG', quality=90)
            w, h = image.size

            w2, h2 = map(lambda x: x - x % 2, (w, h))  # resize to integer multiple of 2
            image = image.resize((w2, h2), resample=PIL.Image.BICUBIC)
            image = image.save(path + item)
            # image = np.array(image).astype(np.float32) / 255.0
            # image = image[None].transpose(0, 3, 1, 2)
            # image = torch.from_numpy(image)
            # return 2.*image - 1.
            # print(f"loaded input image of size ({w2}, {h2}) from {image}")


resize()
