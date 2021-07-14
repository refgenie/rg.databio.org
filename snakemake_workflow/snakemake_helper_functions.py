import os
from refgenie.asset_build_packages import *

INPUT_TEMPLATE = os.path.join(
    os.environ.get("REFGENIE_RAW"), "{genome}-{asset}-{input_id}"
)


def get_req_by_asset(req_type):
    return {
        asset: [req[KEY] for req in asset_recipe[req_type]]
        for asset, asset_recipe in asset_build_packages.items()
    }


def get_req_assets_by_asset():
    return get_req_by_asset(req_type=REQ_ASSETS)


def get_req_files_by_asset():
    return get_req_by_asset(req_type=REQ_FILES)


def get_input_templates(wildcards, asset=None):
    a = asset or wildcards.asset
    if isinstance(a, str):
        a = [a]
    nested_list = [
        [
            INPUT_TEMPLATE.format(genome=wildcards.genome, asset=a, input_id=file_id)
            for file_id in get_req_files_by_asset()[a]
        ]
        for a in a
    ]
    return [item for sublist in nested_list for item in sublist]


def get_asset_file_spec(wildcards, asset=None):
    return [
        "{}={}".format(
            file_id,
            INPUT_TEMPLATE.format(
                genome=wildcards.genome,
                asset=asset or wildcards.asset,
                input_id=file_id,
            ),
        )
        for file_id in get_req_files_by_asset()[asset or wildcards.asset]
    ]


def get_pep_intersect_for_genome(genome, recipe_list, project, exclusion_list=[]):
    genome_samples = [sample for sample in project.samples if sample.genome == genome]
    # this assumes that there is a 1:1 mapping between asset and recipe names
    # this is the case for now, but in the future we may want to use asset classes somehow
    return [
        sample.asset
        for sample in genome_samples
        if sample.asset in recipe_list and sample.asset not in exclusion_list
    ]
