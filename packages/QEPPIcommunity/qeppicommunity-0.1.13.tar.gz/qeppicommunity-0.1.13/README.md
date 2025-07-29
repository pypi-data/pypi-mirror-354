<p align="center">
  <img src="https://user-images.githubusercontent.com/7370243/135420088-f616adc8-1e92-4d9b-8b53-0b863497244d.png"  width="400px">
</p>

# QEPPI
Quantitative Estimate Index for Compounds Targeting Protein-Protein Interactions

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
![PyPI](https://img.shields.io/pypi/v/QEPPIcommunity?style=flat-square)
[![Python Versions](https://img.shields.io/pypi/pyversions/QEPPIcommunity.svg)](https://pypi.org/project/QEPPIcommunity/)


## Calculation QEPPI with using Google Colab
We have made it so that you can use Google Colab to calculate QEPPI from SMILES without creating your own environment.   
If you have a lot of SMILES to calculate, please convert the SMILES to SDF files.  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AspirinCode/QEPPI-community/blob/main/notebook/QEPPI.ipynb)

## Mininal environment setup (Git clone)
We setup it on a Linux.  

```bash
# Python >= 3.8
# dependencies
pip install rdkit      # >= 2025.3.2
pip install numpy
pip install pandas
```

We also confirmed that QEPPI works with Colab. (see [notebook](https://colab.research.google.com/github/AspirinCode/QEPPI-community/blob/main/notebook/QEPPI.ipynb))

### Clone QEPPI-community 
Clone QEPPI-community  repository when you are done with the setup.

```bash
git clone https://github.com/AspirinCode/QEPPI-community.git
```

### Test
Test it after git clone the QEPPI-community repository. If the test passes, the QEPPI calculation has been successfully performed. 
```bash
cd QEPPI
pytest -v
```

## QEPPI calculation example
```bash
# for .sdf
python calc_QEPPI.py --sdf PATH_TO_YOUR_COMPOUND.sdf --out PATH_TO_OUTPUT.csv
```
```bash
# for .csv ("A column name of "SMILES" is required.")
python calc_QEPPI.py --csv PATH_TO_YOUR_COMPOUND.csv --out PATH_TO_OUTPUT.csv
```

## Instalation using pip install
You can also install QEPPI-community  with ```pip install QEPPIcommunity```. The following sample code is available as an implementation example.  
Note: some dependancies will also be installed with QEPPI module, so a clean environment is preferred!
```bash
# QEPPI-community
pip install QEPPIcommunity
```

```python
import QEPPI as ppi
from rdkit import Chem
from rdkit.Chem import SDMolSupplier

q = ppi.QEPPI_Calculator()
q.read()

# SMILES
smiles = "COC1=CC(=CC=C1NC(=O)[C@@H]1N[C@@H](CC(C)(C)C)[C@@](C#N)([C@H]1C1=CC=CC(Cl)=C1F)C1=CC=C(Cl)C=C1F)C(O)=O"
mol = Chem.MolFromSmiles(smiles)
print(q.qeppi(mol))
# 0.7862842663145835

# SDF
ppi_s = SDMolSupplier("PATH_TO_SDF/YOUR_COMPOUND.sdf")
ppi_mols = [mol for mol in ppi_s if mol is not None]
result = list(map(q.qeppi, ppi_mols))
```

## Reference
If you find QEPPI useful, please consider citing this publication;
- Kosugi T, Ohue M. [**Quantitative estimate index for early-stage screening of compounds targeting protein-protein interactions**](https://www.mdpi.com/1422-0067/22/20/10925). _International Journal of Molecular Sciences_, 22(20): 10925, 2021. doi: 10.3390/ijms222010925 

Another QEPPI publication (conference paper)
- Kosugi T, Ohue M. **Quantitative estimate of protein-protein interaction targeting drug-likeness**. In _Proceedings of The 18th IEEE International Conference on Computational Intelligence in Bioinformatics and Computational Biology (CIBCB 2021)_. (in press)
ChemRxiv, Preprint. 2021. [doi:10.33774/chemrxiv-2021-psqq4-v2](https://doi.org/10.33774/chemrxiv-2021-psqq4-v2)
