#!/usr/bin/python3
import os, sys
import requests
import re
import subprocess


def check_filename_exist(file_name_tocheck, input_file_path):
    """
    This will check whether given file exits on the defined path.
    """
    if os.path.isfile(input_file_path+file_name_tocheck):
        return True
    else:
        return False


def get_igstrand_reference(pdb_name, mapping_file_path):
    """
    This will create the mapping  numbering file for given pdb.
    input: pdb_name: 5esv
           input_path: input file path : Make sure have folder: mapping file, pdb_file inside input.

           node_js_file: node js script path
    """

    mapping_file_name = f"{pdb_name.upper()}_refnum_igstrand.json"
    if not check_filename_exist(mapping_file_name, mapping_file_path):
            # if mapping file not found then call node script
            print(f"{mapping_file_name} is not found in {mapping_file_path} . Creating {mapping_file_name}.")
      
            command = ["node", "./refnum.js", pdb_name.upper()]
            result = subprocess.run(command, capture_output=True, text=True)
            if len(result.stdout) > 3:
                with open(mapping_file_path+mapping_file_name, 'w') as f:
                    f.write(result.stdout) 
                    print(f"{mapping_file_name} is created.")
                return True

            else:
                print(f"mapping_file_name is not created")
                print(f"Check if refnum.js file in ./node_js_script/")
                return False

            
    else:
        return True


            


if __name__ == "__main__":
    input_file_path = "../input/"
    output_file_path = "../output/"
    node_js_file_path = "./node_js_script/"
    pdb_name = '1rhh'
    get_igstrand_reference(pdb_name, f"{input_file_path}number_mapping_files/")
    






