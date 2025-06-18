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

from gem_utilities.biomass import calculate_biomass_weight

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(FILE_DIR, "results")

# If the output directory does not exist, create it
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# E coli core model
ecoli_core = cobra.io.load_model("textbook")
weight = calculate_biomass_weight(
    ecoli_core,
    "Biomass_Ecoli_core",
    lumped_biomass_components=None,
    save_work_table=True,
    out_dir=OUT_DIR,
)

# E. coli full model
ecoli_full = cobra.io.load_model("iML1515")
weight_full = calculate_biomass_weight(
    ecoli_full,
    "BIOMASS_Ec_iML1515_WT_75p37M",
    lumped_biomass_components=None,
    save_work_table=True,
    out_dir=OUT_DIR,
)

# Different version of E. coli full model
ecoli_full_v2 = cobra.io.load_json_model(
    "/Users/helenscott/Library/CloudStorage/OneDrive-SharedLibraries-BostonUniversity/Segre Lab - Documents/2-INDIVIDUAL_FOLDERS/Scott_Helen/Projects/C-CoMP/Education/FBA-case-studies/jet-fuel-bugs-on-mars/iJO1366.json"
)
weight_full = calculate_biomass_weight(
    ecoli_full_v2,
    "BIOMASS_Ec_iJO1366_WT_53p95M",
    lumped_biomass_components=None,
    save_work_table=True,
    out_dir=OUT_DIR,
)

# A model from KBase
# CACIA_model_kbase.xml uses the KBase default Gram Negative biomass
model = cobra.io.read_sbml_model(os.path.join(FILE_DIR, "CACIA_model_kbase.xml"))
model.id = "CACIA_model_kbase"
weight_kbase = calculate_biomass_weight(
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
    save_work_table=True,
    out_dir=OUT_DIR,
)

# Human GEM
human_gem_url = "https://raw.githubusercontent.com/SysBioChalmers/Human-GEM/main/model/Human-GEM.xml"
print(f"Downloading Human-GEM model from {human_gem_url}...")
try:
    response = requests.get(human_gem_url)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

    # Load the model directly from the string content
    # cobra.io.read_sbml_model can take a file path or a file-like object
    # For XML text content, use io.StringIO
    model_content_str = response.text
    human_gem_model = cobra.io.read_sbml_model(io.StringIO(model_content_str))
    print("Human-GEM model loaded successfully.")

    # Now you can use human_gem_model, for example:
    weight_human = calculate_biomass_weight(
        human_gem_model,
        "MAR13082",  # "Generic human cell biomass reaction"
        lumped_biomass_components=[
            "MAM01721n",  # DNA
            "MAM02847c",  # RNA
            "MAM10012c",  # cofactor_pool_biomass
            "MAM10013c",  # protein_pool_biomass
            "MAM10014c",  # lipid_pool_biomass
            "MAM10015c",  # metabolite_pool_biomass
        ],
        save_work_table=True,
        out_dir=OUT_DIR,
    )

except requests.exceptions.RequestException as e:
    print(f"Error downloading Human-GEM model: {e}")
except Exception as e:
    print(f"Error processing Human-GEM model: {e}")


# Model with KBase default Gram Negative biomass

# My current alteromonas model
