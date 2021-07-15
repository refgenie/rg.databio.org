#!/usr/bin/env python3

import json
from argparse import ArgumentParser
from typing import Dict


def get_build_resources(asset: str, genome: str) -> Dict[str, str]:
    """
    Get the build parameters for the given asset and genome.

    :param str asset: The asset to get the build parameters for.
    :param str genome: The genome to get the build parameters for.
    :return Dict[str, str]: A dictionary of build parameters.
    """

    compute = {
        "bulker_crate": "databio/refgenie:0.7.7",
        "mem": "24000",
        "cores": "1",
        "partition": "largemem",
        "time": "04:00:00",
    }

    # These are ones that go quick
    fast_assets = [
        "fasta",
        "gencode_gtf",
        "ensembl_gtf",
        "ensembl_rb",
        "feat_annotation",
        "refgene_anno",
        "fasta_txome",
    ]

    slow_assets = ["bismark_bt2_index", "bismark_bt1_index", "salmon_partial_sa_index"]

    if asset in fast_assets:
        compute["time"] = "01:00:00"
        compute["partition"] = "standard"
        compute["mem"] = "6000"
        if genome == "Picea_abies__ConGenIE_v1_0":
            compute["time"] = "08:00:00"
            compute["mem"] = "24000"

    if asset in slow_assets:
        compute["time"] = "8:00:00"

    if asset == "suffixerator_index":
        compute["mem"] = "32000"

    if asset == "bowtie2_index":
        compute["mem"] = "64000"

    if asset == "bismark_bt2_index":
        compute["mem"] = "64000"

    if asset == "bismark_bt1_index":
        compute["mem"] = "64000"

    if asset == "salmon_partial_sa_index":
        compute["mem"] = "112000"
        compute["time"] = "6:00:00"
        compute["cores"] = "8"

    if asset == "dbnsfp":
        compute["time"] = "12:00:00"

    if asset == "salmon_sa_index":
        compute["mem"] = "72000"

    if asset == "star_index":
        compute["mem"] = "64000"

    return compute


parser = ArgumentParser(description="Refgenie build params")

parser.add_argument("-s", "--size", help="size", required=False)  # do we need this?
parser.add_argument("-a", "--asset", type=str, help="asset", required=True)
parser.add_argument("-g", "--genome", type=str, help="genome", required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    print(json.dumps(get_build_resources(args.asset, args.genome)))
