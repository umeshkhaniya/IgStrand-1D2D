#!/usr/bin/python3
import os
import re
import json, json5

ref2igtype = {'ASF1A_2iijA_human': 'IgE',
'B2Microglobulin_7phrL_human_C1': 'IgC1',
'BArrestin1_4jqiA_rat_n1': 'IgFN3-like',
'BTLA_2aw2A_human_Iset': 'IgI',
'C3_2qkiD_human_n1': 'IgFN3-like',
'CD19_6al5A_human-n1': 'CD19',
'CD28_1yjdC_human_V': 'IgV',
'CD2_1hnfA_human_C2-n2': 'IgC2',
'CD2_1hnfA_human_V-n1': 'IgV',
'CD3d_6jxrd_human_C1': 'IgC1',
'CD3e_6jxrf_human_C1': 'IgC1',
'CD3g_6jxrg_human_C2': 'IgC2',
'CD8a_1cd8A_human_V': 'IgV',
'CoAtomerGamma1_1r4xA_human': 'IgE',
'Contactin1_2ee2A_human_FN3-n9': 'IgFN3',
'Contactin1_3s97C_human_Iset-n2': 'IgI',
'CuZnSuperoxideDismutase_1hl5C_human': 'SOD',
'ECadherin_4zt1A_human_n2': 'Cadherin',
'Endo-1,4-BetaXylanase10A_1i8aA_bacteria_n4': 'IgE',
'FAB-HEAVY_5esv_C1-n2': 'IgC1',
'FAB-HEAVY_5esv_V-n1': 'IgV',
'FAB-LIGHT_5esv_C1-n2': 'IgC1',
'FAB-LIGHT_5esv_V-n1': 'IgV',
'GHR_1axiB_human_C1-n1': 'IgC1',
'ICOS_6x4gA_human_V': 'IgV',
'IL6Rb_1bquB_human_FN3-n2': 'IgFN3',
'IL6Rb_1bquB_human_FN3-n3': 'IgFN3',
'InsulinR_8guyE_human_FN3-n1': 'IgFN3',
'InsulinR_8guyE_human_FN3-n2': 'IgFN3',
'IsdA_2iteA_bacteria': 'IgE',
'JAM1_1nbqA_human_Iset-n2': 'IgI',
'LAG3_7tzgD_human_C1-n2': 'IgC1',
'LAG3_7tzgD_human_V-n1': 'IgV',
'LaminAC_1ifrA_human': 'Lamin',
'MHCIa_7phrH_human_C1': 'IgC1',
'MPT63_1lmiA_bacteria': 'IgE',
'NaCaExchanger_2fwuA_dog_n2': 'IgFN3-like',
'NaKATPaseTransporterBeta_2zxeB_spurdogshark': 'IgE',
'ORF7a_1xakA_virus': 'ORF',
'PD1_4zqkB_human_V': 'IgV',
'PDL1_4z18B_human_V-n1': 'IgV',
'Palladin_2dm3A_human_Iset-n1': 'IgI',
'RBPJ_6py8C_human_Unk-n1': 'IgFN3-like',
'RBPJ_6py8C_human_Unk-n2': 'IgFN3-like',
'Sidekick2_1wf5A_human_FN3-n7': 'IgFN3',
'Siglec3_5j0bB_human_C1-n2': 'IgC1',
'TCRa_6jxrm_human_C1-n2': 'IgC1',
'TCRa_6jxrm_human_V-n1': 'IgV',
'TEAD1_3kysC_human': 'IgE',
'TP34_2o6cA_bacteria': 'IgE',
'TP47_1o75A_bacteria': 'IgE',
'Titin_4uowM_human_Iset-n152': 'IgI',
'VISTA_6oilA_human_V': 'IgV',
'VNAR_1t6vN_shark_V': 'IgV',
'VTCN1_Q7Z7D3_human_C1-n2': 'IgC1'}

def split_string(s):
    """
    This will split the number into strand number and number part
    input: "A'1248a"
    ouput: A', 1248a
    """
    match = re.search(r'^([^0-9]*)([0-9].*)$', s)
    return match.groups() if match else None
   
def load_json_file(file_path):
    """
    The file is downloaded using the node js and it has extra comma (",")
    """
    try:
        with open(file_path, 'r') as file:
            json_data = file.read().rstrip('\n')
            if not json_data:
                return None

            if not json_data.endswith(']'):
                # If not, append a closing bracket
                json_data += ']'
            # Load the JSON
            json_data = json5.loads(json_data)
        return json_data
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return None
    except FileNotFoundError:
        print(f"File not found:{file_path}.")
        return None

def parse_igmapinfo(igstrand_data):
    """
    This will parse the data [{'7CM4_A_350_V': "A'1840"}, {'7CM4_A_351_Y': "A'1841"}, 
    {'7CM4_A_352_A': "A'1842"}, {'7CM4_A_353_W': "A'1843"}] and return mapping data with number as key 
    and value as resid and loop info. Undefined residue info and ig domain residue range.
    """
    ig_map_residue = {}
    undefined_res = []
    ig_domain_start = str(igstrand_data[0].keys()).split("_")[-2]
    ig_domain_end = str(igstrand_data[-1].keys()).split("_")[-2]
    for ig_num_info in igstrand_data:
        residue_identity, strand_number = next(iter(ig_num_info.items()))
        pdb_resid_info = residue_identity.split("_")
        residue_letter = pdb_resid_info[-1]
        residue_number = pdb_resid_info[2]
        if strand_number != "undefined":
            # first split loop
            strandnum_loop = strand_number.split("_")
            if len(strandnum_loop) == 2:
                strandnum, loop_assign = strandnum_loop[0], strandnum_loop[1]
            else:
                strandnum, loop_assign = strandnum_loop[0], ""

            if strandnum not in ig_map_residue:
                
                ig_map_residue[strandnum] = (residue_letter,loop_assign)
            else:
                print(f"Following residue_number is duplicated: {pdb_resid_info}")
        else:
            undefined_res.append(residue_number)
            print(f"undefined residues exits in {pdb_resid_info}")
    return ig_map_residue, f"{ig_domain_start}:{ig_domain_end}", undefined_res

def sort_residue_range(item_dict, residue_range):
    """
    This will sort the list of dictionaries based on residues_range separated by
    :. This will also deal with if residues range has letter
    'residue_range': '30:165'
    """
    match = re.match(r'(\d+)([a-zA-Z]?):(\d+)([a-zA-Z]?)', item_dict[residue_range])
    if match:
        start_num, start_alpha, end_num, end_alpha = match.groups()
        start = int(start_num)
        if start_alpha:
            start += ord(start_alpha.lower()) - ord('a') + 1
        end = int(end_num)
        if end_alpha:
            end += ord(end_alpha.lower()) - ord('a') + 1
        return start, end
    return float('inf'), float('inf')



def igdomain_delineate(ig_chain_data, pdbid_chain):
    """
    It will have each chain data. Will return the igmap data 
    with residues id as key and mapping as value.
    pdbid_chain: {"6xc2_A"}
    """
    parse_domain_data = []
    #
    for id_chain_3d, ref_ig_data in ig_chain_data.items():
        chain_id, domain_info = id_chain_3d.split(",")
        domain_residues_info = domain_info.split("_")
        domain3d_order = int(domain_residues_info[0]) + 1 # 0 based 

        domain3d_res_range = (":".join(domain_residues_info[1].split(":")[0:2]))

        igstrand_data = ref_ig_data['data']
        igstrand_data, igD_res_range, undefined_info = parse_igmapinfo(igstrand_data)


        parse_domain_ref = {"3Ddomain_order": domain3d_order, "refpdbname": ref_ig_data['refpdbname'], "Igtype": ref2igtype[ref_ig_data['refpdbname']], "igD_res_range":igD_res_range, 
        "3dD_res_range":domain3d_res_range, "tmscore":ref_ig_data['score'], "seqid":ref_ig_data["seqid"], "nresAlign": ref_ig_data["nresAlign"], "undefined_info": undefined_info,  "igstrand_data":igstrand_data}
        parse_domain_data.append(parse_domain_ref)

    #  3d domain order  from numbering is not accurate sometimes.  Make domain order based on 
    # ig domain residues selected (igD_res_range).

    sorted_parse_domain = sorted(parse_domain_data, key=lambda x: sort_residue_range(x, "igD_res_range"))
    # Create a new dictionary with keys as order numbers and values as corresponding dictionaries
    sorted_parse_domain_chain = {pdbid_chain + "_" + str(i+1): sorted_parse_domain[i] for i in range(len(sorted_parse_domain))}

    return sorted_parse_domain_chain



def get_igmap_domain(pdb_chain_domain, numbering_name, input_path):
    """
    input: pdb_id: pdbid (1cd8)
           first_sel: ("A", "1") # chain, ig domainn # 1 based
           second_sel: ("B, "1")# chain, ig domain # 1 based
           input_path: where file located.
    ouput: list of dictionary of mapping information of that chain.

    """
    if len(pdb_chain_domain) != 3:
         raise ValueError("pdb_chain_domain length must be 3")

    pdb_chain = pdb_chain_domain[0].upper() + "_" + pdb_chain_domain[1]
    domain = pdb_chain_domain[2]
    

    refnum_file = f"{pdb_chain_domain[0].upper()}_refnum_{numbering_name}.json"
    json_data = load_json_file(os.path.join(input_path, refnum_file))

    if json_data:
        for files_ig in json_data:
            if pdb_chain_domain[0].upper() in files_ig: # filter pdb id
                # # check if ig or not.
                if files_ig[pdb_chain_domain[0].upper()]['Ig domain']== 1: # this means it has ig
                    for ig_parse in files_ig[pdb_chain_domain[0].upper()]['igs']:
                        # we have two ids.
                        # check if id_chain exits#
                        if pdb_chain in ig_parse: # check first chain
                            ig_prase_filter_data = ig_parse.get(pdb_chain)

                            return igdomain_delineate(ig_prase_filter_data, pdb_chain).get(pdb_chain + "_" + str(domain))             
                            
    return 


if __name__ == "__main__":
    input_path= "../input/number_mapping_files"
    pdb_chain_domain = ("7TZG", "D", 2)
    #pdb_chain_domain = ("7LQ7", "H", 1)
    print(get_igmap_domain(pdb_chain_domain, "igstrand", input_path))


