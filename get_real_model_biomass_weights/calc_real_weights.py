import io
import os
import sys

import requests

# Calculate the path to the project root directory (GEM-utils)
# This goes one level up from the script's directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import cobra

from gem_utilities.biomass import save_biomass_composition_work_table

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(FILE_DIR, "results")

# If the output directory does not exist, create it
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# E coli core model
ecoli_core = cobra.io.load_model("textbook")
save_biomass_composition_work_table(
    ecoli_core,
    "Biomass_Ecoli_core",
    lumped_biomass_components=None,
    out_dir=OUT_DIR,
)

# E. coli full model
ecoli_full = cobra.io.load_model("iML1515")
save_biomass_composition_work_table(
    ecoli_full,
    "BIOMASS_Ec_iML1515_WT_75p37M",
    lumped_biomass_components=None,
    out_dir=OUT_DIR,
)

# Different version of E. coli full model
ecoli_full_v2 = cobra.io.load_json_model(
    "/Users/helenscott/Library/CloudStorage/OneDrive-SharedLibraries-BostonUniversity/Segre Lab - Documents/2-INDIVIDUAL_FOLDERS/Scott_Helen/Projects/C-CoMP/Education/FBA-case-studies/jet-fuel-bugs-on-mars/iJO1366.json"
)
save_biomass_composition_work_table(
    ecoli_full_v2,
    "BIOMASS_Ec_iJO1366_WT_53p95M",
    lumped_biomass_components=None,
    out_dir=OUT_DIR,
)

# A model from KBase
# CACIA_model_kbase.xml uses the KBase default Gram Negative biomass
model = cobra.io.read_sbml_model(os.path.join(FILE_DIR, "CACIA_model_kbase.xml"))
model.id = "CACIA_model_kbase"
save_biomass_composition_work_table(
    model,
    "bio1_biomass",
    mets_to_ignore=[
        "cpd11416_c0",  # Biomass_c0
        "cpd15665_c0",  # Peptidoglycan polymer (n subunits)_c0
        "cpd15666_c0",  # Peptidoglycan polymer (n-1 subunits)_c0
        "cpd12370_c0",  # apo-ACP_c0
        "cpd11493_c0",  # ACP_c0
    ],
    lumped_biomass_components=[
        "cpd17041_c0",  # Protein biosynthesis_c0
        "cpd17043_c0",  # RNA transcription_c0
        "cpd17042_c0",  # DNA replication_c0
    ],
    out_dir=OUT_DIR,
)

# My current alteromonas model
alteromonas_model = cobra.io.read_sbml_model(
    "/Users/helenscott/Documents/PhD/Segre-lab/GEM-repos/GEM-mit1002/model.xml"
)
save_biomass_composition_work_table(
    alteromonas_model,
    "bio1_biomass",
    mets_to_ignore=[
        "cpd11416_c0",  # Biomass_c0
    ],
    lumped_biomass_components=[
        "cpd11461_c0",  # DNA [c0]
        "cpd11463_c0",  # Protein [c0]
        "cpd11462_c0",  # mRNA [c0]
    ],
    out_dir=OUT_DIR,
)
