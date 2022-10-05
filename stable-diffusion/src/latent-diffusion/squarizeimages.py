#this script was modified by https://github.com/nicolai256 to make square training images squared without cropping

import argparse
import cv2
import time
import os, sys
import shutil
from pathlib import Path



import subprocess
import random
parser = argparse.ArgumentParser()
#inpaint
#parser.add_argument("--mask", type=str, help="thickness of the mask for seamless inpainting",choices=["thinnest", "thin", "medium", "thick", "thickest"],default="medium")
#u can change these
parser.add_argument("--input",type=str,nargs="?",default="tmp360/tiled_image/",help="input image",)
parser.add_argument("--outdir",type=str,nargs="?",default="outputs/training_imgs_squarized/",help="dir to write results to",)
parser.add_argument("--steps",type=int,default=50,help="number of ddim sampling steps",)
parser.add_argument("--projectname",type=str,default="project1",help="foldername of the export",)


parser.add_argument("--edgeremoval",type=int,default=False,help="activate edgedetection",)
parser.add_argument("--edgedetection",type=str,default="40%",help="strength of edgedetection, percentage strength depends on how much of a complex border your images have ",)
parser.add_argument("--extra_crop",type=int,default=False,help="add extra crop of 10 px on each side",)



#to activate paths in voc
parser.add_argument("--voc",type=int,default=False,help="a command to activate it so it works with visions of chaos paths",)

#to find latent diffusion folder in non voc
parser.add_argument("--latent_diffusion_path",type=str,default="/src/latent-diffusion",help="pass the path to your 'stable-diffusion/src/latent-diffusion' folder",)


opt = parser.parse_args()  

if opt.voc:
    visions_path = os.path.expanduser('~\Documents\\visions of chaos')
    latent_diffusion_path = os.path.expanduser('~\AppData\\Roaming\\Visions of Chaos\\Examples\\MachineLearning\\Text To Image\\Stable Diffusion\\src\\latent-diffusion')
    voc = opt.voc
else:
    visions_path = os.path.expanduser('~\Documents')
    latent_diffusion_path = opt.latent_diffusion_path


##first pass of inpainting
import argparse, os, sys, glob
from omegaconf import OmegaConf
from PIL import Image
from tqdm import tqdm
import numpy
import numpy as np
import torch
#from src.latentdiffusion.ldm.util import instantiate_from_config
from main import instantiate_from_config
from ldm.models.diffusion.ddim import DDIMSampler
import natsort
from natsort import natsorted
path=opt.input
dirs = os.listdir( path )
path=opt.input
  
def rmdirs():
	zero1=visions_path+"/tmpsquarize"
	one1=visions_path+"/tmpsquarize/resizedimages/"
	two1=visions_path+"/tmpsquarize/Imagesfortrainingdark/"
	three1=visions_path+"/tmpsquarize/padded_imgs-masks/"
	five1=visions_path+"/tmpsquarize/images/"

	import shutil

	
	if os.path.exists(zero1):
		shutil.rmtree(zero1, ignore_errors=True)
	if os.path.exists(one1):
		shutil.rmtree(one1, ignore_errors=True)
	if os.path.exists(two1):
		shutil.rmtree(two1, ignore_errors=True)
	if os.path.exists(three1):
		shutil.rmtree(three1, ignore_errors=True)
	if os.path.exists(five1):
		shutil.rmtree(five1, ignore_errors=True)
	import subprocess
	from pathlib import Path

	#using pathlib.Path
	if os.path.exists(zero1):
		path = Path(zero1)
		subprocess.run(["rm", "-rf", str(path)])

	#using strings
	if os.path.exists(zero1):
		path = zero1
		subprocess.run(["rm", "-rf", path])
rmdirs()

def mkdirs():
	zero=visions_path+"/tmpsquarize"
	one=visions_path+"/tmpsquarize/resizedimages/"
	two=visions_path+"/tmpsquarize/Imagesfortrainingdark/"
	three=visions_path+"/tmpsquarize/padded_imgs-masks/"
	five=visions_path+"/tmpsquarize/images/"
	four=opt.outdir+"/"+opt.projectname+"/"
	six=visions_path+"/tmpsquarize/trimmedborders/"
	if not os.path.exists(zero):
		os.mkdir(zero)
	if not os.path.exists(one):
		os.mkdir(one)
	if not os.path.exists(two):
		os.mkdir(two)
	if not os.path.exists(three):
		os.mkdir(three)
	if not os.path.exists(four):
		os.mkdir(four)
	if not os.path.exists(five):
		os.mkdir(five)
	if not os.path.exists(six):
		os.mkdir(six)
mkdirs()

def move ():
	source1 = opt.input
	destination1 = visions_path+"/tmpsquarize/images/"
	allfiles = os.listdir(source1)
 
	# iterate on all files to move them to destination folder
	for f in allfiles:
		src_path = os.path.join(source1, f)
		dst_path = os.path.join(destination1, f)
		shutil.copy(src_path, dst_path)
move()

def edgeremoval():
	if opt.edgeremoval:
		source2 = visions_path+"/tmpsquarize/images/*"
		desitiantion2 = visions_path+"/tmpsquarize/resizedimages/"
		print('removing edges for improved inpainting')
		edgedetection = opt.edgedetection
		subprocess.run(['magick', 'mogrify', '-path', desitiantion2, '-fuzz', edgedetection, '-trim', '-format', 'png', source2])
	else:
		source2 = visions_path+"/tmpsquarize/images/"
		desitiantion2 = visions_path+"/tmpsquarize/resizedimages/"
		allfiles = os.listdir(source2)
		for f in allfiles:
			src_path = os.path.join(source2, f)
			dst_path = os.path.join(desitiantion2, f)
			shutil.copy(src_path, dst_path)
	
edgeremoval()

def crop():
	if opt.extra_crop:
		desitiantion2 = visions_path+"/tmpsquarize/resizedimages/"
		path_to_input_images=desitiantion2
		path=path_to_input_images
		dirs = os.listdir( path )
		tmp_imgs_crop = latent_diffusion_path + '/scripts/squarize/tmp_imgs_crop.py'
		if opt.voc:
			subprocess.run(['python.exe', tmp_imgs_crop, '--voc', '1'])
		else:
			subprocess.run(['python.exe', tmp_imgs_crop])
		print('cropping 5%')
		for item in dirs:
			if os.path.isfile(path+item):
				im = Image.open(path+item).convert("RGB")
				w, h = im.size
 
				# Setting the points for cropped image
				left =  w-w+10
				top =  h-h+10
				right =  w-10
				bottom = h-10
 
                # Cropped image of above dimension
                # (It will not change original image)
				im1 = im.crop((left, top, right, bottom))
				im1.save(path+item)
	print('cropped')
crop()

def cropsquarefix():
	
		desitiantion2 = visions_path+"/tmpsquarize/resizedimages/"
		path_to_input_images=desitiantion2
		path=path_to_input_images
		dirs = os.listdir( path )
		
		print('cropping 5%')
		for item in dirs:
			if os.path.isfile(path+item):
				im = Image.open(path+item).convert("RGB")
				w, h = im.size
 
				# Setting the points for cropped image
				left =  w-w+0
				top =  h-h+0
				right =  w-0
				bottom = h-2
 
                # Cropped image of above dimension
                # (It will not change original image)
				im1 = im.crop((left, top, right, bottom))
				im1.save(path+item)
				print('cropped')
crop()

def square():
	desitiantion2 = visions_path+"/tmpsquarize/resizedimages/"
	path_to_input_images=desitiantion2
	path=path_to_input_images
	files=glob.glob(path+"*")
	files=natsorted(files)
	for image in tqdm(files):
		head_tail = os.path.basename(image)
		i=cv2.imread(image)
		size=i.shape
		h,w=size[0],size[1]
		output_folder = opt.outdir + "/" + opt.projectname + "/" + head_tail
		if w==h:
			shutil.move(os.path.join(image),output_folder)
		elif w==h-1:
			shutil.move(os.path.join(image),output_folder)
		elif w==h+1:
			shutil.move(os.path.join(image),output_folder)
		elif w-1==h:
			shutil.move(os.path.join(image),output_folder)
		elif w+1==h:
			shutil.move(os.path.join(image),output_folder)
# commented out as we want to fix images that are still 1:1 or close
# square()

def padding():
    tmp_imgs_darken = latent_diffusion_path + '/scripts/squarize/tmp_imgs_darken.py'
    tmp_imgs_dark = latent_diffusion_path + '/scripts/squarize/tmp_imgs_dark.py'
    tmp_imgs = latent_diffusion_path + '/scripts/squarize/tmp_imgs.py'
    pad_imgs = latent_diffusion_path + '/scripts/squarize/pad_imgs.py'
    pad_masks = latent_diffusion_path + '/scripts/squarize/pad_masks.py'
    if opt.voc:
        subprocess.run(['python.exe',tmp_imgs_darken, '--voc', '1'])
        subprocess.run(['python.exe',tmp_imgs_dark, '--voc', '1'])
        subprocess.run(['python.exe',tmp_imgs, '--voc', '1'])
        subprocess.run(['python.exe',pad_imgs, '--voc', '1'])
        subprocess.run(['python.exe',pad_masks, '--voc', '1'])
    else:
        subprocess.run(['python.exe',tmp_imgs_darken])
        subprocess.run(['python.exe',tmp_imgs_dark])
        subprocess.run(['python.exe',tmp_imgs])
        subprocess.run(['python.exe',pad_imgs])
        subprocess.run(['python.exe',pad_masks])
padding()

def make_batch(image, mask, device):
    image = np.array(Image.open(image).convert("RGB"))
    image = image.astype(np.float32)/255.0
    image = image[None].transpose(0,3,1,2)
    image = torch.from_numpy(image)

    mask = np.array(Image.open(mask).convert("L"))
    mask = mask.astype(np.float32)/255.0
    mask = mask[None,None]
    mask[mask < 0.5] = 0
    mask[mask >= 0.5] = 1
    mask = torch.from_numpy(mask)

    masked_image = (1-mask)*image

    batch = {"image": image, "mask": mask, "masked_image": masked_image}
    for k in batch:
        batch[k] = batch[k].to(device=device)
        batch[k] = batch[k]*2.0-1.0
    return batch

def run():
	#for item in dirs:
	#	if os.path.isfile(path+item):
			import ntpath
			global base_count
			paddedfolder = visions_path+"/tmpsquarize/padded_imgs-masks/"
			indir = paddedfolder
			masks = sorted(glob.glob(os.path.join(indir, "*_mask.png")))
			images = [x.replace("_mask.png", ".png") for x in masks]
			#basename = ntpath.basename(images)
			outdir = opt.outdir + "/" + opt.projectname + "/"
			print(f"Found {len(masks)} inputs.")
			configpath = latent_diffusion_path +"/models/ldm/inpainting_big/config.yaml"
			modelpath = latent_diffusion_path + "/models/ldm/inpainting_big/last.ckpt"
			config = OmegaConf.load(configpath)
			model = instantiate_from_config(config.model)
			#'MachineLearning/Super Resolution Latent-Diffusion/last.ckpt'
			model.load_state_dict(torch.load(modelpath)["state_dict"],strict=False)

			device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
			model = model.to(device)
			sampler = DDIMSampler(model)

			os.makedirs(opt.outdir, exist_ok=True)
			with torch.no_grad():
				with model.ema_scope():
					for image, mask in tqdm(zip(images, masks)):
						outpath = os.path.join(outdir, os.path.split(image)[1])
						batch = make_batch(image, mask, device=device)
						global base_count
						# encode masked image and concat downsampled mask
						c = model.cond_stage_model.encode(batch["masked_image"])
						cc = torch.nn.functional.interpolate(batch["mask"],size=c.shape[-2:])
						c = torch.cat((c, cc), dim=1)

						shape = (c.shape[1]-1,)+c.shape[2:]
						samples_ddim, _ = sampler.sample(S=opt.steps,conditioning=c,batch_size=c.shape[0],shape=shape,verbose=False)
						x_samples_ddim = model.decode_first_stage(samples_ddim)

						image = torch.clamp((batch["image"]+1.0)/2.0,min=0.0, max=1.0)
						mask = torch.clamp((batch["mask"]+1.0)/2.0,min=0.0, max=1.0)
						predicted_image = torch.clamp((x_samples_ddim+1.0)/2.0,min=0.0, max=1.0)

						inpainted = (1-mask)*image+mask*predicted_image
						inpainted = inpainted.cpu().numpy().transpose(0,2,3,1)[0]*255
						base_count = 0
						base_count += 1
						Image.fromarray(inpainted.astype(np.uint8)).save(outpath)
						base_count += 1


run()

def rmdirs2():
	zero1=visions_path+"/tmpsquarize"
	one1=visions_path+"/tmpsquarize/resizedimages/"
	two1=visions_path+"/tmpsquarize/Imagesfortrainingdark/"
	three1=visions_path+"/tmpsquarize/padded_imgs-masks/"
	five1=visions_path+"/tmpsquarize/images/"

	import shutil

	
	if os.path.exists(zero1):
		shutil.rmtree(zero1, ignore_errors=True)
	if os.path.exists(one1):
		shutil.rmtree(one1, ignore_errors=True)
	if os.path.exists(two1):
		shutil.rmtree(two1, ignore_errors=True)
	if os.path.exists(three1):
		shutil.rmtree(three1, ignore_errors=True)
	if os.path.exists(five1):
		shutil.rmtree(five1, ignore_errors=True)
	import subprocess
	from pathlib import Path

	#using pathlib.Path
	if os.path.exists(zero1):
		path = Path(zero1)
		subprocess.run(["rm", "-rf", str(path)])

	#using strings
	if os.path.exists(zero1):
		path = zero1
		subprocess.run(["rm", "-rf", path])
rmdirs2()