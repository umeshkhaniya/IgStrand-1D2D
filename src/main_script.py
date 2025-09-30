import argparse
import subprocess
import os, json

def main():
    # Define the argument parser
    parser = argparse.ArgumentParser(description='Process input file for 1D or 2D aligment.')
    parser.add_argument('-f', '--file', help='Input file must have pdbid chain Domain', required=True)
    parser.add_argument('-d', '--dimension', help='Processing dimension (1D, 2D, or 1D,2D)', required=True)
    args = parser.parse_args()

    template_row_col = {
        "V_column_range": 21,
        "V_row_range" : 47}


    # Set environment variables
    os.environ['input_file_path'] = "../input/"
    os.environ['output_file_path'] = "../output/"
    os.environ['node_js_file_path'] = "node_js_script/"
    os.environ['numbering_name'] = "igstrand"
    # dictionary can not be set as environment variable. so
    # Serialize the dictionary to a JSON string
    template_row_col_json = json.dumps(template_row_col)

    # Set the JSON string in the environment variable
    os.environ['template_row_col'] = template_row_col_json



    dimensions = args.dimension.split(',')

    for dim in dimensions:
        if dim == '1D':
            # Call the alignment_1D_igstrand.py script
            subprocess.run(['python', 'alignment_1D_igstrand.py', '-f', args.file])
        elif dim == '2D':
            # Call the alignment_2D_igstrand.py script
            subprocess.run(['python', 'alignment_2D_igstrand.py', '-f', args.file])
        else:
            print(f"Invalid dimension specified: {dim}. Supported dimensions are 1D, 2D, or 1D,2D.")

if __name__ == '__main__':
    main()
