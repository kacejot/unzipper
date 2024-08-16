import os
import shutil
import glob
import argparse
from psd_tools import PSDImage

parser = argparse.ArgumentParser(description='Unzip, copy and render PSD files.')
parser.add_argument('--source', type=str, help='Source folder containing zip files', required=True)
parser.add_argument('--destination', type=str, help='Destination folder for extracted PSD files')
args = parser.parse_args()

source_folder = args.source
destination_folder = args.destination if args.destination else "./rendered"
unarchived_folder = "./unarchived"
psd_folder = "./psd"

archives = glob.glob(os.path.join(source_folder, "*.zip"))

for archive in archives:
    archive_name = os.path.splitext(os.path.basename(archive))[0]
    shutil.unpack_archive(archive, unarchived_folder)
    # os.remove(archive)

if not os.path.exists(psd_folder):
    os.makedirs(psd_folder)
    
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
    
psd_files = glob.glob(os.path.join(unarchived_folder, "**/*.psd"), recursive=True)

for psd_file in psd_files:
    new_file_name = os.path.basename(psd_file)
    suffix = 1

    while True:
        if not os.path.exists(os.path.join(psd_folder, new_file_name)):
            break
        new_file_name = f"{os.path.splitext(new_file_name)[0]}_{suffix}{os.path.splitext(new_file_name)[1]}"
        suffix += 1

    psd_destination_path = os.path.join(psd_folder, new_file_name)
    shutil.copy(psd_file, psd_destination_path)
    psd_file_name = os.path.splitext(new_file_name)[0]
    psd = PSDImage.open(psd_file)
    layers = [x for x in psd]
    
    if not layers:
        psd.composite().save('{0}/{1}.png'.format(destination_folder, psd_file_name))
    
    for i, layer in enumerate(layers):
        layer_image = layer.composite()
        layer_image.save('{0}/{1}_{2}.png'.format(destination_folder, psd_file_name, i+1))
