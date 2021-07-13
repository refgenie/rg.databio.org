import os

from refgenie.asset_build_packages import asset_build_packages

DESC = "description"
ASSET_DESC = "asset_description"
ASSETS = "assets"
PTH = "path"
REQ_FILES = "required_files"
REQ_ASSETS = "required_assets"
REQ_PARAMS = "required_parameters"
CONT = "container"
CMD_LST = "command_list"
KEY = "key"
DEFAULT = "default"


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
    input_files_dir = os.environ.get(
        "REFGENIE_RAW", "/Users/mstolarczyk/Desktop/testing/refgenie/raw"
    )
    input_file_template = "{genome}-{asset}-{input_id}"
    input_template = os.path.join(input_files_dir, input_file_template)
    nested_list = [
        [
            input_template.format(genome=wildcards.genome, asset=a, input_id=file_id)
            for file_id in get_req_files_by_asset()[a]
        ]
        for a in a
    ]
    return [item for sublist in nested_list for item in sublist]
