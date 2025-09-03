import os
import shutil
from typing import Tuple


def prepare_data_folder(folder_path: str) -> None:
    """
    prepare data folder, create one if not exist
    if exist, empty the folder
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def rename_and_copy_files(src_folder: str, des_folder: str, in_suffix:str, out_suffix: str) -> Tuple[dict, dict]:
    """
    Input:
         src_folder: a user input folder, name could be anything, will be convert into nnUnet
         format internally

         des_folder: where you want to store your folder

    Returns:
         rename_dict : a dictionary mapping your original name into nnUnet format name
         rename_back_dict:  a dictionary will be use to mapping backto the original name

    """
    files = os.listdir(src_folder)
    rename_dict = {}
    rename_back_dict = {}

    for idx, filename in enumerate(files):
        old_name = os.path.join(src_folder, filename)
        rename_file = f"case_{idx:04d}_0000.nii.gz"
        rename_back = f"case_{idx:04d}.nii.gz"
        new_name = os.path.join(des_folder, rename_file)
        print(f"Copying {old_name} to {new_name}")
        shutil.copy2(old_name, new_name)
        rename_dict[filename] = rename_file
        # rename_back_dict[rename_back] = "label_" + filename
        print(filename)
        rename_back_dict[rename_back] = str(filename).split(in_suffix)[0] + str(out_suffix)

    return rename_dict, rename_back_dict

# def rename_and_copy_files(src_folder: str, des_folder: str, suffix: str) -> Tuple[dict, dict]:
#     """
#     Input:
#          src_folder: a user input folder, name could be anything, will be convert into nnUnet
#          format internally

#          des_folder: where you want to store your folder

#     Returns:
#          rename_dict : a dictionary mapping your original name into nnUnet format name
#          rename_back_dict:  a dictionary will be use to mapping backto the original name

#     """
#     if not os.path.exists(src_folder):
#         raise FileNotFoundError(f"Source folder '{src_folder}' does not exist.")
#     if not os.path.exists(des_folder):
#         raise FileNotFoundError(f"Source folder '{des_folder}' does not exist.")

#     files = os.listdir(src_folder)
#     rename_dict = {}
#     rename_back_dict = {}

#     for idx, filename in enumerate(files):
#         old_name = os.path.join(src_folder, filename)
#         if not os.path.isfile(old_name):  # We only want files!
#             continue
#         rename_file = f"case_{idx:03d}_0000.nii.gz"
#         rename_back = f"case_{idx:03d}.nii.gz"
#         new_name = os.path.join(des_folder, rename_file)
#         try:
#             shutil.copy2(old_name, new_name)
#             rename_dict[filename] = rename_file
#             rename_back_dict[rename_back] = filename.split(".nii")[0] + suffix
#         except Exception as e:
#             print(f"Error copying file '{filename}' to '{new_name}': {e}")
#     print(rename_back_dict)
    
#     return rename_dict, rename_back_dict