# IgStrand-Align

Understanding the three-dimensional structure of immunoglobulin (Ig) domains in the context of two-dimensional representative maps is critical for advancing biological insights.  

While one-dimensional (1D) protein sequence information is limited to the linear order of amino acid residues, two-dimensional (2D) representations incorporate structural annotations that connect sequence with topology. These representations highlight biologically relevant features such as:  

- Interacting residues  
- Cross-links  
- Surface accessibility  
- Orientation and strand pairing  
- Structural motifs within Ig folds  

The goal of **IgStrand-Align** is to bridge **sequence (1D)** and **structure (2D)** by providing alignment tools and mapping functions based on the IgStrand numbering scheme. This enables systematic comparison of Ig domains and facilitates structural and functional analysis across large datasets.  

---

## Features
- Generate **1D sequence alignments** for Ig domains  
- Produce **2D topological maps** annotated with structural features  
- Map residue positions consistently using the **IgStrand numbering scheme**  
- Export alignments for visualization and downstream analysis  

---

## Usage
Run the main script with:

```bash
python src/main_script.py [-h] -f FILE -d DIMENSION
```
### Arguments

- -h : Show help message and exit

- -f FILE : Input file containing PDB ID, chain ID, and domain number

- -d DIMENSION : Output type, choose one of:

  - 1D : Generate 1D representation
  
  - 2D : Generate 2D representation
  
  - 1D,2D : Generate both 1D and 2D representations

### Example Input File (`input.txt`)

```text
1RHH B 1
5ESV D 1
```

Each line contains:

  - PDB ID
  
  - Chain ID
  
  - Domain number
### Example Commands

  ### Generate 1D representation only
  ```bash
  python src/main_script.py -f input.txt -d 1D
  ```
  ### Generate 2D representation only
  ```bash
  python src/main_script.py -f input.txt -d 2D
  ```
  ### Generate both 1D and 2D representations
  ```bash
  python src/main_script.py -f input.txt -d 1D,2D
 ```
### Output
  - 1D alignment: Shows aligned sequences for domains from the input file, including reference PDB, Ig type, and sequence information, color-coded by the IgStrand numbering scheme.
  
  - 2D alignment: Provides 2D structural annotations and topological information for each specified domain

---


## Applications

- Comparative analysis of Ig domains

- Mapping sequence to structure for antibody engineering

- Understanding evolutionary variation within Ig folds

- Structural annotation in immunogenomics pipelines



