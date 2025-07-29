"""QEPPI score calculation utilities.

This file originates from `ohuelab/QEPPI` and is maintained by the
community at `AspirinCode/QEPPI-community`.
It implements the :class:`QEPPI_Calculator` used for scoring molecules.
"""

from .util import ads
from .constant import CHEM_LABELS, DESC_FUNC_DICT, WEIGHT
from rdkit.Chem import rdMolDescriptors, Crippen

import numpy as np
import pickle
import warnings


class QEPPI_Calculator:
    def __init__(self, desc_func_dict=DESC_FUNC_DICT, model=None):
        # if model is not None:
        #     self.model = load(model)
        self.desc_func_dict = desc_func_dict

    def load(self, model_path):
        with open(model_path, "rb") as rf:
            model = pickle.load(rf)
        self.model = model
    
    def read(self, weight=WEIGHT):
        self.model = weight

    def qeppi(self, mol, method="mo", detail=False):
        if method == "u":
            w = np.ones(len(CHEM_LABELS))
        else:
            if method not in self.model["weights"]:
                raise ValueError("invalid or unprepared weight set was specified.")
            w = np.array(self.model["weights"][method])
        d_lst = []
        if detail:
            d_dict = {}
        for label in CHEM_LABELS:
            desc = self.desc_func_dict[label](mol)
            params = self.model["params"][label]
            func_d = lambda x: ads(x, *params["coefficients"])
            rtn = func_d(desc)
            d_lst.append(rtn)
            if detail:
                d_dict[label] = rtn
        d = np.array(d_lst)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ld = np.nan_to_num(np.log(d))
        wd = w * ld
        q = np.exp(np.sum(wd) / np.sum(w))
        if detail:
            d_dict["QEPPI"] = q
            return d_dict
        return q

    def descript(self, mol):
        d_dict = {}
        for label in CHEM_LABELS:
            desc = self.desc_func_dict[label](mol)
            d_dict[label] = desc
        return d_dict

def get_qeppi_properties(mol):
    """Return descriptor values used by the QEPPI score.

    Parameters
    ----------
    mol : rdkit.Chem.Mol
        Molecule to compute properties for.

    Returns
    -------
    dict
        Mapping of descriptor labels to their calculated values.
    """

    return {
        "MW": rdMolDescriptors.CalcExactMolWt(mol),
        "ALOGP": Crippen.MolLogP(mol),
        "HBD": rdMolDescriptors.CalcNumHBD(mol),
        "HBA": rdMolDescriptors.CalcNumHBA(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "ROTB": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "AROM": rdMolDescriptors.CalcNumAromaticRings(mol),
    }
