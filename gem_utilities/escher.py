import json
import warnings

import cobra


def create_comparison_data_file(*models):
    """A function that takes any number of COBRA models and creates a
    JSON file to use as 'reaction data' in Escher, where the reaction
    line will be weighted based on the number of models that the reaction
    is present in. This is useful for visually comparing models.
    Ideally, there would be a function in Escher for comparing models,
    but this is a workaround for now.

    Parameters
    ----------
    models : cobra.Model
        Any number of cobra model objects

    Returns
    -------
    A dictionary that can be saved to make a reaction data JSON file
    """
    # Check that all arguments are cobra models
    for model in models:
        if not isinstance(model, cobra.Model):
            raise TypeError("All arguments must be cobra models.")

    # If there is only one model, give an error
    if len(models) == 1:
        raise ValueError("This function requires at least two models.")

    # TODO: Check that the models use the same comparement nomenclature
    # (e.g. 'c' vs 'c0') since the compartment ID is ususally in the
    # reaction IDs

    # Create a dictionary of reactions and the number of models they are
    # present in and return it
    reaction_dict = {}
    for model in models:
        for reaction in model.reactions:
            if reaction.id not in reaction_dict:
                reaction_dict[reaction.id] = 1
            else:
                reaction_dict[reaction.id] += 1
    return reaction_dict


def merge_escher_maps(input_files, output_file, combined_map_name=None, spacing=1000):
    """
    Merges multiple Escher JSON maps into a single file, side-by-side.

    Parameters
    ----------
    input_files : list of str
        List of file paths to the Escher JSON maps to be merged.
    output_file : str
        Path to save the combined JSON file.
    combined_map_name : str, optional
        Name for the combined map, by default None
    spacing : int, optional
        Horizontal gap between the maps, by default 1000
    """
    combined_nodes = {}
    combined_reactions = {}
    combined_text_labels = {}

    current_x_offset = 0
    min_y, max_y = 0, 0
    total_width = 0

    for i, file_path in enumerate(input_files):
        with open(file_path, "r") as f:
            map_data = json.load(f)

        # Escher files are lists: [meta_data, map_elements]
        elements = map_data[1]  # Yes, always the second element contains the map elements
        canvas = elements["canvas"]
        prefix = f"m{i}_"

        # 1. Process Nodes
        for n_id, node in elements["nodes"].items():
            node["x"] += current_x_offset
            if "label_x" in node:
                node["label_x"] += current_x_offset
            combined_nodes[f"{prefix}{n_id}"] = node

        # 2. Process Reactions
        for r_id, rxn in elements["reactions"].items():
            rxn["label_x"] += current_x_offset
            for s_id, seg in rxn["segments"].items():
                # Update node references to use the new prefixed IDs
                seg["from_node_id"] = f"{prefix}{seg['from_node_id']}"
                seg["to_node_id"] = f"{prefix}{seg['to_node_id']}"
                # Update control point coordinates
                if seg["b1"]:
                    seg["b1"]["x"] += current_x_offset
                if seg["b2"]:
                    seg["b2"]["x"] += current_x_offset
            combined_reactions[f"{prefix}{r_id}"] = rxn

        # 3. Process Text Labels
        labels = elements.get("text_labels", {})
        for l_id, label in labels.items():
            label["x"] += current_x_offset
            combined_text_labels[f"{prefix}{l_id}"] = label

        # 4. Update offset for the next map based on current map width
        current_x_offset += canvas["width"] + spacing

        # Track canvas boundaries for the final bounding box
        min_y = min(min_y, canvas["y"])
        max_y = max(max_y, canvas["y"] + canvas["height"])

    # Define the new global canvas
    new_canvas = {
        "x": 0,
        "y": min_y,
        "width": current_x_offset,
        "height": max_y - min_y,
    }

    # Assemble the final structure
    final_output = [
        {
            "map_name": "Combined Escher Map",
            "map_id": "merged_map_auto",
            "map_description": f"Auto-merged from {len(input_files)} files.",
            "homepage": "https://escher.github.io",
            "schema": "https://escher.github.io/escher/jsonschema/1-0-0#",
        },
        {
            "canvas": new_canvas,
            "nodes": combined_nodes,
            "reactions": combined_reactions,
            "text_labels": combined_text_labels,
        },
    ]

    with open(output_file, "w") as f:
        json.dump(final_output, f, indent=4)
    print(f"Successfully merged {len(input_files)} maps into {output_file}")


# Example Usage:
# files_to_merge = ['map1.json', 'map2.json', 'map3.json']
# merge_escher_maps(files_to_merge, 'final_combined_map.json')
merge_escher_maps(
    [
        "/Users/helenscott/Documents/PhD/Segre-lab/GEM-repos/GEM-mit1002/escher/MIT1002_glycolysis_and_tca_escher-map.json",
        "/Users/helenscott/Desktop/MIT1002_ETC_escher-map-38.json",
    ],
    "/Users/helenscott/Documents/PhD/Segre-lab/GEM-repos/GEM-mit1002/escher/MIT1002_central_w_etc_escher-map.json",
)
