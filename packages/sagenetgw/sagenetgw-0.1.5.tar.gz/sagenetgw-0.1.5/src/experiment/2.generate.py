from IPython.display import clear_output
from stiffGWpy.stiff_SGWB import LCDM_SG as SG
from tqdm import tqdm
import numpy as np
import json
import argparse
parser = argparse.ArgumentParser(description='Load a specific JSON data part.')
parser.add_argument('--volume', type=int, required=True, help='Volume number of the JSON file (e.g., 1, 2, 3, or 4)')
args = parser.parse_args()
volume = args.volume

with open(f'./src/solve/input/data_part_{volume}.json', 'r') as f:
    data = json.load(f)

unprocessed_data = [
    doc for doc in data
    if 'log10OmegaGW' not in doc
]

processed_docs = []

if __name__ == "__main__":
    for document in tqdm(unprocessed_data):
        try:
            print(document['_id'])
            model4_new = SG(r=document['r'], n_t=document['n_t'], cr=0, T_re=document['T_re'], DN_re=document['DN_re'],
                            kappa10=document['kappa10'],
                            Omega_bh2=document['Omega_bh2'], Omega_ch2=document['Omega_ch2'], H0=document['H0'],
                            A_s=document['A_s'])
            model4_new.SGWB_iter()
            N_hc_arr_new = np.array(model4_new.N_hc, dtype=object)
            Th_arr_new = np.array(model4_new.Th, dtype=object)
            targets_new = [line[-1] for line in Th_arr_new]
            windows_new = [[line[0], line[-1]] for line in N_hc_arr_new]
            clear_output()
            document.update({
                "targets": targets_new,
                "windows": windows_new,
                "f": list(model4_new.f),
                "log10OmegaGW": list(model4_new.log10OmegaGW),
            })
            processed_docs.append(document)
        except AttributeError:
            continue

    with open(f'./src/solve/output/processed_data_{volume}.json', 'w') as f:
        json.dump(processed_docs, f, indent=2)
