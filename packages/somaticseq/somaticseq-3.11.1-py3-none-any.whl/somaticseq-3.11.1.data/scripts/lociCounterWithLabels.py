#!python

import argparse
import logging
import os
import re
import tempfile
import uuid
from copy import copy
from os.path import basename

from somaticseq.vcf_modifier.bed_util import bed_sort_and_merge

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def fai2bed(
    file_name: str,
) -> tuple[
    dict[str, list[int]], dict[str, list[int]], dict[str, list[list[str]]], list[str]
]:
    """
    This function initiates the regions and region counters based on the contigs
    in a .fa.fai file. This script will start with the whole contig regions
    here, and then iterate through each bed file to extract regions where bed
    files overlap.

    Returns:
        callableLociBoundries: dict where keys are contigs, and values are [0,
            contig_size].
        callableLociCounters: dict where keys are contigs, and values are number
            of regions overlapping this region. Values are initiated at 0.
        callableLociLabels: dict where keys are contigs, and values are list of
            bed files (or their corresponding names) overlapping them.
        orderedContig: list of contigs ordered by their apperance in the .fa.fai
            file.
    """
    with open(file_name) as gfile:
        callableLociBoundries: dict[str, list[int]] = {}
        callableLociCounters: dict[str, list[int]] = {}
        callableLociLabels: dict[str, list[list[str]]] = {}
        orderedContig: list[str] = []
        line_i = gfile.readline().rstrip("\n")
        while line_i:
            contig_match = re.match(r"([^\t]+)\t", line_i)
            if contig_match:
                # some .fai files have space after the contig for descriptions.
                contig_i = contig_match.groups()[0].split(" ")[0]
                orderedContig.append(contig_i)
                contig_size = int(line_i.split("\t")[1])
                callableLociBoundries[contig_i] = [0, contig_size]
                callableLociCounters[contig_i] = [0]
                callableLociLabels[contig_i] = [[]]
            else:
                raise FileNotFoundError(".fai file format not as expected.")

            line_i = gfile.readline().rstrip("\n")
    return (
        callableLociBoundries,
        callableLociCounters,
        callableLociLabels,
        orderedContig,
    )


def bed2regions(bed_file: str) -> dict[str, list[tuple[int, int]]]:
    """
    Returns: dict where keys are contigs, and the values are list of regions in
    a bed file.
    """
    regions: dict[str, list[tuple[int, int]]] = {}
    with open(bed_file) as gfile:
        line_i = gfile.readline().rstrip("\n")
        while line_i:
            item = line_i.split("\t")
            chrom = item[0]
            startPos = int(item[1])
            endPos = int(item[2])
            try:
                regions[chrom].append((startPos, endPos))
            except KeyError:
                regions[chrom] = []
                regions[chrom].append((startPos, endPos))
            line_i = gfile.readline().rstrip("\n")

    return regions


def collapseIdenticalBoundries(boundries, counters, labels):
    assert len(boundries) == len(counters) + 1 == len(labels) + 1

    outBoundries = []
    outCounters = []
    outLabels = []

    outBoundries.append(boundries[0])

    i = 0
    while i <= len(boundries) - 2:
        j = i + 1

        if boundries[i] != boundries[j]:
            outBoundries.append(boundries[j])
            outCounters.append(counters[j - 1])
            outLabels.append(labels[j - 1])

        i += 1

    return outBoundries, outCounters, outLabels


def countIntersectedRegions(
    original_boundry, original_counter, additional_regions, original_label, new_label
):
    secondary_boundry = []

    for region_i in additional_regions:
        secondary_boundry.append(region_i[0])
        secondary_boundry.append(region_i[1])

    newBoundry = []
    newCounter = []
    newLabel = []

    secondaryIterator = iter(secondary_boundry)
    boundry_j = next(secondaryIterator)
    j = 0
    secondaryMore = True

    for i, boundry_i in enumerate(original_boundry):
        if secondaryMore:
            while boundry_j < boundry_i:
                newBoundry.append(boundry_j)

                if j % 2 == 0:
                    # Will not reach undefined name (F821) due to flow control
                    newCounter.append(counter_i + 1)  # noqa: F821
                    label_i_copy = copy(label_i)  # noqa: F821
                    label_i_copy.append(new_label)
                    newLabel.append(label_i_copy)
                elif j % 2 == 1:
                    newCounter.append(counter_i)  # noqa: F821
                    newLabel.append(label_i)  # noqa: F821
                try:
                    boundry_j = next(secondaryIterator)
                    j += 1
                except StopIteration:
                    secondaryMore = False
                    break

        # Move onto the next original boundry
        newBoundry.append(boundry_i)
        try:
            counter_i = original_counter[i]
            label_i = original_label[i]
        except IndexError:
            counter_i = None
            label_i = None

        if not secondaryMore and counter_i is not None:
            newCounter.append(counter_i)
            newLabel.append(label_i)

        elif j % 2 == 0:
            newCounter.append(counter_i)
            newLabel.append(label_i)

        elif j % 2 == 1:
            if counter_i is not None:
                newCounter.append(counter_i + 1)
                label_i_copy = copy(label_i)
                label_i_copy.append(new_label)
                newLabel.append(label_i_copy)

    (
        consolidatedBoundries,
        consolidatedCounters,
        consolidatedLabels,
    ) = collapseIdenticalBoundries(newBoundry, newCounter, newLabel)

    return consolidatedBoundries, consolidatedCounters, consolidatedLabels


def run(fai_file, bed_files, bed_labels, bed_out):

    tempdir = tempfile.mkdtemp()
    # Start routine:
    contigBoundries, contigCounters, contigLabels, orderedContigs = fai2bed(fai_file)

    # Look at BED files
    for i, bed_file_i in enumerate(bed_files):
        bed_file_j = os.path.join(tempdir, uuid.uuid4().hex) + ".bed"
        logger.info(f"{bed_file_i} sorted and merged into {bed_file_j}.")
        bed_sort_and_merge(bed_file_i, bed_file_j, fai_file)
        bedRegions = bed2regions(bed_file_j)
        label_i = bed_labels[i]
        for chrom in bedRegions:
            (
                contigBoundries[chrom],
                contigCounters[chrom],
                contigLabels[chrom],
            ) = countIntersectedRegions(
                contigBoundries[chrom],
                contigCounters[chrom],
                bedRegions[chrom],
                contigLabels[chrom],
                label_i,
            )
    with open(bed_out, "w") as bed_out:
        for contig_i in orderedContigs:
            if contigCounters[contig_i] != [0]:
                for i, count_i in enumerate(contigCounters[contig_i]):
                    label_string = (
                        ",".join(contigLabels[contig_i][i])
                        if contigLabels[contig_i][i]
                        else "."
                    )
                    out_string = "{}\t{}\t{}\t{}\t{}".format(
                        contig_i,
                        contigBoundries[contig_i][i],
                        contigBoundries[contig_i][i + 1],
                        count_i,
                        label_string,
                    )
                    bed_out.write(out_string + "\n")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "This is a program to tally and count the overlapping regions "
            "when given multiple input bed files. A CRITICAL REQUIREMENT is that "
            "each input bed file is sorted and non-overlapping, which "
            "could be achieved with bedtools merge "
            "before they are used as input to this program."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-fai", "--fai-file", type=str, help=".fa.fai file", required=True, default=None
    )
    parser.add_argument(
        "-beds",
        "--bed-files",
        type=str,
        help=(
            "Input bed files. "
            "Each MUST be non-overlapping regions sorted to the input fai file."
        ),
        nargs="+",
        required=True,
        default=None,
    )
    parser.add_argument(
        "-out", "--bed-out", type=str, help="BED file out", required=True, default=None
    )
    parser.add_argument(
        "-labels",
        "--bed-labels",
        type=str,
        help="Use these labels instead of bed file names",
        nargs="*",
        required=False,
        default=None,
    )
    args = parser.parse_args()

    fai_file = args.fai_file
    bed_files = args.bed_files
    bed_out = args.bed_out
    bed_labels = args.bed_labels
    if bed_labels:
        assert len(bed_labels) == len(bed_files)
    else:
        bed_labels = [basename(bed_file_i) for bed_file_i in bed_files]

    ## Run the program:
    run(fai_file, bed_files, bed_labels, bed_out)


if __name__ == "__main__":
    main()
