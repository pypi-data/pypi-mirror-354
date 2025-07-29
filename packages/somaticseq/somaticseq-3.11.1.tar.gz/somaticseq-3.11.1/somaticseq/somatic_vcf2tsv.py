#!/usr/bin/env python3

import argparse
import logging
import math
import os
import re
import sys
from copy import copy

import pysam
from scipy import stats

import somaticseq.annotate_caller as annotate_caller
import somaticseq.genomic_file_parsers.genomic_file_handlers as genome
import somaticseq.sequencing_features as seq_features
from somaticseq.bam_features import BamFeatures
from somaticseq.genomic_file_parsers.read_info_extractor import (
    genomic_coordinates,
    rescale,
)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

# Header for the output data, created here so I won't have to indent this line:
out_header = "{CHROM}\t\
{POS}\t\
{ID}\t\
{REF}\t\
{ALT}\t\
{if_MuTect}\t\
{if_VarScan2}\t\
{if_JointSNVMix2}\t\
{if_SomaticSniper}\t\
{if_VarDict}\t\
{MuSE_Tier}\t\
{if_LoFreq}\t\
{if_Scalpel}\t\
{if_Strelka}\t\
{if_TNscope}\t\
{if_Platypus}\t\
{Strelka_Score}\t\
{Strelka_QSS}\t\
{Strelka_TQSS}\t\
{VarScan2_Score}\t\
{SNVMix2_Score}\t\
{Sniper_Score}\t\
{VarDict_Score}\t\
{if_dbsnp}\t\
{COMMON}\t\
{if_COSMIC}\t\
{COSMIC_CNT}\t\
{Consistent_Mates}\t\
{Inconsistent_Mates}\t\
{Seq_Complexity_Span}\t\
{Seq_Complexity_Adj}\t\
{N_DP}\t\
{nBAM_REF_MQ}\t\
{nBAM_ALT_MQ}\t\
{nBAM_p_MannWhitneyU_MQ}\t\
{nBAM_REF_BQ}\t\
{nBAM_ALT_BQ}\t\
{nBAM_p_MannWhitneyU_BQ}\t\
{nBAM_REF_NM}\t\
{nBAM_ALT_NM}\t\
{nBAM_NM_Diff}\t\
{nBAM_REF_Concordant}\t\
{nBAM_REF_Discordant}\t\
{nBAM_ALT_Concordant}\t\
{nBAM_ALT_Discordant}\t\
{nBAM_Concordance_FET}\t\
{N_REF_FOR}\t\
{N_REF_REV}\t\
{N_ALT_FOR}\t\
{N_ALT_REV}\t\
{nBAM_StrandBias_FET}\t\
{nBAM_p_MannWhitneyU_EndPos}\t\
{nBAM_REF_Clipped_Reads}\t\
{nBAM_ALT_Clipped_Reads}\t\
{nBAM_Clipping_FET}\t\
{nBAM_MQ0}\t\
{nBAM_Other_Reads}\t\
{nBAM_Poor_Reads}\t\
{nBAM_REF_InDel_3bp}\t\
{nBAM_REF_InDel_2bp}\t\
{nBAM_REF_InDel_1bp}\t\
{nBAM_ALT_InDel_3bp}\t\
{nBAM_ALT_InDel_2bp}\t\
{nBAM_ALT_InDel_1bp}\t\
{M2_NLOD}\t\
{M2_TLOD}\t\
{M2_STR}\t\
{M2_ECNT}\t\
{SOR}\t\
{MSI}\t\
{MSILEN}\t\
{SHIFT3}\t\
{MaxHomopolymer_Length}\t\
{SiteHomopolymer_Length}\t\
{T_DP}\t\
{tBAM_REF_MQ}\t\
{tBAM_ALT_MQ}\t\
{tBAM_p_MannWhitneyU_MQ}\t\
{tBAM_REF_BQ}\t\
{tBAM_ALT_BQ}\t\
{tBAM_p_MannWhitneyU_BQ}\t\
{tBAM_REF_NM}\t\
{tBAM_ALT_NM}\t\
{tBAM_NM_Diff}\t\
{tBAM_REF_Concordant}\t\
{tBAM_REF_Discordant}\t\
{tBAM_ALT_Concordant}\t\
{tBAM_ALT_Discordant}\t\
{tBAM_Concordance_FET}\t\
{T_REF_FOR}\t\
{T_REF_REV}\t\
{T_ALT_FOR}\t\
{T_ALT_REV}\t\
{tBAM_StrandBias_FET}\t\
{tBAM_p_MannWhitneyU_EndPos}\t\
{tBAM_REF_Clipped_Reads}\t\
{tBAM_ALT_Clipped_Reads}\t\
{tBAM_Clipping_FET}\t\
{tBAM_MQ0}\t\
{tBAM_Other_Reads}\t\
{tBAM_Poor_Reads}\t\
{tBAM_REF_InDel_3bp}\t\
{tBAM_REF_InDel_2bp}\t\
{tBAM_REF_InDel_1bp}\t\
{tBAM_ALT_InDel_3bp}\t\
{tBAM_ALT_InDel_2bp}\t\
{tBAM_ALT_InDel_1bp}\t\
{InDel_Length}"

extra_caller_header = ""
label_header = "{TrueVariant_or_False}"


def run() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "This is a SomaticSeq subroutine to convert a VCF file into a TSV file "
            "with all the SomaticSeq features for tumor-normal mode. "
            "Any VCF file can be used as the main input. "
            "The output will have the same variants. "
            "Also required are the tumor-normal BAM files, "
            "with additional optional inputs."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    input_sites = parser.add_mutually_exclusive_group()
    input_sites.add_argument(
        "-myvcf", "--vcf-format", type=str, help="Input file is VCF formatted."
    )
    input_sites.add_argument(
        "-mybed", "--bed-format", type=str, help="Input file is BED formatted."
    )
    input_sites.add_argument(
        "-mypos",
        "--positions-list",
        type=str,
        help="A list of positions: tab seperating contig and positions.",
    )
    parser.add_argument(
        "-nbam", "--normal-bam-file", type=str, help="Normal BAM File", required=True
    )
    parser.add_argument(
        "-tbam", "--tumor-bam-file", type=str, help="Tumor BAM File", required=True
    )

    parser.add_argument(
        "-truth", "--ground-truth-vcf", type=str, help="VCF of true hits"
    )
    parser.add_argument(
        "-dbsnp",
        "--dbsnp-vcf",
        type=str,
        help="dbSNP VCF: do not use if input VCF is annotated",
    )
    parser.add_argument(
        "-cosmic",
        "--cosmic-vcf",
        type=str,
        help="COSMIC VCF: do not use if input VCF is annotated",
    )
    parser.add_argument(
        "-mutect",
        "--mutect-vcf",
        type=str,
        help="MuTect VCF",
    )
    parser.add_argument(
        "-strelka",
        "--strelka-vcf",
        type=str,
        help="Strelka VCF",
    )
    parser.add_argument(
        "-sniper",
        "--somaticsniper-vcf",
        type=str,
        help="SomaticSniper VCF",
    )
    parser.add_argument(
        "-varscan",
        "--varscan-vcf",
        type=str,
        help="VarScan2 VCF",
    )
    parser.add_argument(
        "-jsm",
        "--jsm-vcf",
        type=str,
        help="JointSNVMix2 VCF",
    )
    parser.add_argument(
        "-vardict",
        "--vardict-vcf",
        type=str,
        help="VarDict VCF",
    )
    parser.add_argument(
        "-muse",
        "--muse-vcf",
        type=str,
        help="MuSE VCF",
    )
    parser.add_argument(
        "-lofreq",
        "--lofreq-vcf",
        type=str,
        help="LoFreq VCF",
    )
    parser.add_argument(
        "-scalpel",
        "--scalpel-vcf",
        type=str,
        help="Scalpel VCF",
    )
    parser.add_argument(
        "-tnscope",
        "--tnscope-vcf",
        type=str,
        help="TNscope VCF",
    )
    parser.add_argument(
        "-platypus",
        "--platypus-vcf",
        type=str,
        help="Platypus VCF",
    )
    parser.add_argument(
        "-arbvcfs",
        "--arbitrary-vcfs",
        type=str,
        help="Arbitrary extra VCFs",
        nargs="*",
        default=[],
    )
    parser.add_argument(
        "-ref",
        "--genome-reference",
        type=str,
        help=".fasta.fai file to get the contigs",
        required=True,
    )
    parser.add_argument(
        "-dedup",
        "--deduplicate",
        action="store_true",
        help="Do not count reads marked as duplicates. Default=False.",
        default=False,
    )
    parser.add_argument(
        "-minMQ",
        "--minimum-mapping-quality",
        type=float,
        help="Minimum mapping quality below which is considered poor",
        default=1,
    )
    parser.add_argument(
        "-minBQ",
        "--minimum-base-quality",
        type=float,
        help="Minimum base quality below which is considered poor",
        default=5,
    )
    parser.add_argument(
        "-mincaller",
        "--minimum-num-callers",
        type=float,
        help="Minimum number of tools to be considered",
        default=0,
    )

    parser.add_argument(
        "-scale", "--p-scale", type=str, help="phred, fraction, or none"
    )

    parser.add_argument(
        "-outfile",
        "--output-tsv-file",
        type=str,
        help="Output TSV Name",
        default=sys.stdout,
    )
    args = parser.parse_args()
    return args


def vcf2tsv(
    is_vcf=None,
    is_bed=None,
    is_pos=None,
    nbam_fn=None,
    tbam_fn=None,
    truth=None,
    cosmic=None,
    dbsnp=None,
    mutect=None,
    varscan=None,
    jsm=None,
    sniper=None,
    vardict=None,
    muse=None,
    lofreq=None,
    scalpel=None,
    strelka=None,
    tnscope=None,
    platypus=None,
    arbitrary_vcfs=[],
    dedup=True,
    min_mq=1,
    min_bq=5,
    min_caller=0,
    ref_fa=None,
    p_scale=None,
    outfile=None,
):
    # Convert contig_sequence to chrom_seq dict:
    fai_file = ref_fa + ".fai"
    chrom_seq = genome.faiordict2contigorder(fai_file, "fai")

    # Determine input format:
    if is_vcf:
        mysites = is_vcf
    elif is_bed:
        mysites = is_bed
    elif is_pos:
        mysites = is_pos
    else:
        mysites = fai_file
        logger.info("No position supplied. Will evaluate the whole genome.")

    # Re-scale output or not:
    if p_scale is None:
        logger.info("NO RE-SCALING")
    elif p_scale.lower() == "phred":
        p_scale = "phred"
    elif p_scale.lower() == "fraction":
        p_scale = "fraction"
    else:
        p_scale = None
        logger.info("NO RE-SCALING")

        # Define NaN and Inf:
    nan = float("nan")

    ## Running
    with genome.open_textfile(mysites) as my_sites, open(outfile, "w") as outhandle:
        my_line = my_sites.readline().rstrip()
        nbam = pysam.AlignmentFile(nbam_fn, reference_filename=ref_fa)
        tbam = pysam.AlignmentFile(tbam_fn, reference_filename=ref_fa)
        ref_fa = pysam.FastaFile(ref_fa)

        if truth:
            truth = genome.open_textfile(truth)
            truth_line = genome.skip_vcf_header(truth)

        if cosmic:
            cosmic = genome.open_textfile(cosmic)
            cosmic_line = genome.skip_vcf_header(cosmic)

        if dbsnp:
            dbsnp = genome.open_textfile(dbsnp)
            dbsnp_line = genome.skip_vcf_header(dbsnp)

        # 10 Incorporate callers: get thru the #'s
        if mutect:
            mutect = genome.open_textfile(mutect)
            mutect_line = genome.skip_vcf_header(mutect)

        if varscan:
            varscan = genome.open_textfile(varscan)
            varscan_line = genome.skip_vcf_header(varscan)

        if jsm:
            jsm = genome.open_textfile(jsm)
            jsm_line = genome.skip_vcf_header(jsm)

        if sniper:
            sniper = genome.open_textfile(sniper)
            sniper_line = genome.skip_vcf_header(sniper)

        if vardict:
            vardict = genome.open_textfile(vardict)
            vardict_line = genome.skip_vcf_header(vardict)

        if muse:
            muse = genome.open_textfile(muse)
            muse_line = genome.skip_vcf_header(muse)

        if lofreq:
            lofreq = genome.open_textfile(lofreq)
            lofreq_line = genome.skip_vcf_header(lofreq)

        if scalpel:
            scalpel = genome.open_textfile(scalpel)
            scalpel_line = genome.skip_vcf_header(scalpel)

        if strelka:
            strelka = genome.open_textfile(strelka)
            strelka_line = genome.skip_vcf_header(strelka)

        if tnscope:
            tnscope = genome.open_textfile(tnscope)
            tnscope_line = genome.skip_vcf_header(tnscope)

        if platypus:
            platypus = genome.open_textfile(platypus)
            platypus_line = genome.skip_vcf_header(platypus)

        arbitrary_file_handle = {}
        arbitrary_line = {}
        for ith_arbi, arbitrary_vcf_i in enumerate(arbitrary_vcfs):
            arbitrary_file_handle[ith_arbi] = genome.open_textfile(arbitrary_vcf_i)
            arbitrary_line[ith_arbi] = genome.skip_vcf_header(
                arbitrary_file_handle[ith_arbi]
            )

        # Get through all the headers:
        while my_line.startswith("#") or my_line.startswith("track="):
            my_line = my_sites.readline().rstrip()

        # First coordinate, for later purpose of making sure the input is sorted
        # properly
        coordinate_i = re.match(genome.PATTERN_CHR_POSITION, my_line)
        coordinate_i = coordinate_i.group() if coordinate_i else ""

        # First line:
        header_part_1 = out_header.replace("{", "").replace("}", "")

        additional_arbi_caller_numbers = sorted(arbitrary_file_handle.keys())
        for arbi_caller_num in additional_arbi_caller_numbers:
            header_part_1 = header_part_1 + "\t" + f"if_Caller_{arbi_caller_num}"

        header_last_part = label_header.replace("{", "").replace("}", "")

        outhandle.write("\t".join((header_part_1, header_last_part)) + "\n")

        while my_line:
            # If VCF, get all the variants with the same coordinate into a list:
            if is_vcf:
                my_vcf = genome.VCFVariantRecord.from_vcf_line(my_line)

                my_coordinates = [(my_vcf.chromosome, my_vcf.position)]

                variants_at_my_coordinate = []

                alt_bases = my_vcf.altbase.split(",")
                for alt_i in alt_bases:
                    vcf_i = copy(my_vcf)
                    vcf_i.altbase = alt_i
                    variants_at_my_coordinate.append(vcf_i)

                # As long as the "coordinate" stays the same, it will keep
                # reading until it's different.
                while my_coordinates[0] == (my_vcf.chromosome, my_vcf.position):
                    my_line = my_sites.readline().rstrip()
                    my_vcf = genome.VCFVariantRecord.from_vcf_line(my_line)

                    # This block is code is to ensure the input VCF file is
                    # properly sorted
                    coordinate_j = re.match(genome.PATTERN_CHR_POSITION, my_line)
                    coordinate_j = coordinate_j.group() if coordinate_j else ""

                    if genome.whoisbehind(coordinate_i, coordinate_j, chrom_seq) == 1:
                        raise Exception(
                            f"{mysites} does not seem to be properly sorted."
                        )

                    coordinate_i = coordinate_j
                    if my_coordinates[0] == (my_vcf.chromosome, my_vcf.position):
                        alt_bases = my_vcf.altbase.split(",")
                        for alt_i in alt_bases:
                            vcf_i = copy(my_vcf)
                            vcf_i.altbase = alt_i
                            variants_at_my_coordinate.append(vcf_i)

            elif is_bed:
                bed_item = my_line.split("\t")
                my_coordinates = genomic_coordinates(
                    bed_item[0], int(bed_item[1]) + 1, int(bed_item[2])
                )

            elif is_pos:
                pos_item = my_line.split("\t")
                my_coordinates = genomic_coordinates(
                    pos_item[0], int(pos_item[1]), int(pos_item[1])
                )

            elif fai_file:
                fai_item = my_line.split("\t")
                my_coordinates = genomic_coordinates(fai_item[0], 1, int(fai_item[1]))

            for my_coordinate in my_coordinates:
                # If VCF, can get ref base, variant base, as well as other
                # identifying information
                if is_vcf:
                    ref_bases = []
                    alt_bases = []
                    indel_lengths = []
                    all_my_identifiers = []

                    for variant_i in variants_at_my_coordinate:
                        ref_base = variant_i.refbase
                        first_alt = variant_i.altbase.split(",")[0]
                        indel_length = len(first_alt) - len(ref_base)

                        ref_bases.append(ref_base)
                        alt_bases.append(first_alt)
                        indel_lengths.append(indel_length)

                        # Extract these information if they exist in the VCF
                        # file, but they could be re-written if dbSNP/COSMIC are
                        # supplied.
                        if_dbsnp = (
                            1 if re.search(r"rs[0-9]+", variant_i.identifier) else 0
                        )
                        if_cosmic = (
                            1
                            if re.search(r"COS[MN][0-9]+", variant_i.identifier)
                            else 0
                        )
                        if_common = (
                            1 if variant_i.get_info_value("COMMON") == "1" else 0
                        )
                        num_cases = (
                            variant_i.get_info_value("CNT")
                            if variant_i.get_info_value("CNT")
                            else nan
                        )

                        if variant_i.identifier == ".":
                            my_identifier_i = set()
                        else:
                            my_identifier_i = variant_i.identifier.split(";")
                            my_identifier_i = set(my_identifier_i)

                        all_my_identifiers.append(my_identifier_i)

                ## If not, 1) get ref_base, first_alt from other VCF files.
                # 2 ) Create placeholders for dbSNP and COSMIC that can be
                # overwritten with dbSNP/COSMIC VCF files (if provided)
                else:
                    variants_at_my_coordinate = [
                        None
                    ]  # Just to have something to iterate
                    ref_base = first_alt = indel_length = None

                    # Could be re-written if dbSNP/COSMIC are supplied. If not,
                    # they will remain NaN.
                    if_dbsnp = if_cosmic = if_common = num_cases = nan

                # Find the same coordinate in those VCF files
                if mutect:
                    (
                        got_mutect,
                        mutect_variants,
                        mutect_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, mutect_line, mutect, chrom_seq
                    )
                if varscan:
                    (
                        got_varscan,
                        varscan_variants,
                        varscan_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, varscan_line, varscan, chrom_seq
                    )
                if jsm:
                    got_jsm, jsm_variants, jsm_line = genome.find_vcf_at_coordinate(
                        my_coordinate, jsm_line, jsm, chrom_seq
                    )
                if sniper:
                    (
                        got_sniper,
                        sniper_variants,
                        sniper_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, sniper_line, sniper, chrom_seq
                    )
                if vardict:
                    (
                        got_vardict,
                        vardict_variants,
                        vardict_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, vardict_line, vardict, chrom_seq
                    )
                if muse:
                    got_muse, muse_variants, muse_line = genome.find_vcf_at_coordinate(
                        my_coordinate, muse_line, muse, chrom_seq
                    )
                if lofreq:
                    (
                        got_lofreq,
                        lofreq_variants,
                        lofreq_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, lofreq_line, lofreq, chrom_seq
                    )
                if scalpel:
                    (
                        got_scalpel,
                        scalpel_variants,
                        scalpel_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, scalpel_line, scalpel, chrom_seq
                    )
                if strelka:
                    (
                        got_strelka,
                        strelka_variants,
                        strelka_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, strelka_line, strelka, chrom_seq
                    )
                if tnscope:
                    (
                        got_tnscope,
                        tnscope_variants,
                        tnscope_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, tnscope_line, tnscope, chrom_seq
                    )
                if platypus:
                    (
                        got_platypus,
                        platypus_variants,
                        platypus_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, platypus_line, platypus, chrom_seq
                    )
                if truth:
                    (
                        got_truth,
                        truth_variants,
                        truth_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, truth_line, truth, chrom_seq
                    )
                if dbsnp:
                    (
                        got_dbsnp,
                        dbsnp_variants,
                        dbsnp_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, dbsnp_line, dbsnp, chrom_seq
                    )
                if cosmic:
                    (
                        got_cosmic,
                        cosmic_variants,
                        cosmic_line,
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate, cosmic_line, cosmic, chrom_seq
                    )

                got_arbitraries = {}
                arbitrary_variants = {}
                for ith_arbi in arbitrary_file_handle:
                    (
                        got_arbitraries[ith_arbi],
                        arbitrary_variants[ith_arbi],
                        arbitrary_line[ith_arbi],
                    ) = genome.find_vcf_at_coordinate(
                        my_coordinate,
                        arbitrary_line[ith_arbi],
                        arbitrary_file_handle[ith_arbi],
                        chrom_seq,
                    )

                # Now, use pysam to look into the BAM file(s), variant by
                # variant from the input:
                for ith_call, my_call in enumerate(variants_at_my_coordinate):
                    if is_vcf:
                        # The particular line in the input VCF file:
                        variant_id = (
                            (my_call.chromosome, my_call.position),
                            my_call.refbase,
                            my_call.altbase,
                        )

                        ref_base = ref_bases[ith_call]
                        first_alt = alt_bases[ith_call]
                        indel_length = indel_lengths[ith_call]
                        my_identifiers = all_my_identifiers[ith_call]

                    else:
                        variant_id = (
                            (my_coordinate[0], my_coordinate[1]),
                            ref_base,
                            first_alt,
                        )

                    # Reset num_caller to 0 for each variant in the same coordinate
                    num_callers = 0

                    # Collect Caller Vcf
                    if mutect:
                        (
                            mutect_classification,
                            nlod,
                            tlod,
                            tandem,
                            ecnt,
                        ) = annotate_caller.MuTect(variant_id, mutect_variants)
                        num_callers += mutect_classification
                    else:
                        mutect_classification = nlod = tlod = tandem = ecnt = nan

                    if varscan:
                        varscan_classification = annotate_caller.VarScan(
                            variant_id, varscan_variants
                        )
                        num_callers += varscan_classification
                    else:
                        varscan_classification = nan

                    if jsm:
                        (
                            jointsnvmix2_classification,
                            score_jointsnvmix2,
                        ) = annotate_caller.JSM(variant_id, jsm_variants)
                        num_callers += jointsnvmix2_classification
                    else:
                        jointsnvmix2_classification = score_jointsnvmix2 = nan

                    if sniper:
                        (
                            sniper_classification,
                            score_somaticsniper,
                        ) = annotate_caller.SomaticSniper(variant_id, sniper_variants)
                        num_callers += sniper_classification
                    else:
                        sniper_classification = score_somaticsniper = nan

                    if vardict:
                        (
                            vardict_classification,
                            msi,
                            msilen,
                            shift3,
                            score_vardict,
                        ) = annotate_caller.VarDict(variant_id, vardict_variants)
                        num_callers += vardict_classification
                    else:
                        vardict_classification = msi = msilen = shift3 = (
                            score_vardict
                        ) = nan

                    if muse:
                        muse_classification = annotate_caller.MuSE(
                            variant_id, muse_variants
                        )
                        num_callers += muse_classification
                    else:
                        muse_classification = nan

                    if lofreq:
                        lofreq_classification = annotate_caller.LoFreq(
                            variant_id, lofreq_variants
                        )
                        num_callers += lofreq_classification
                    else:
                        lofreq_classification = nan

                    if scalpel:
                        scalpel_classification = annotate_caller.Scalpel(
                            variant_id, scalpel_variants
                        )
                        num_callers += scalpel_classification
                    else:
                        scalpel_classification = nan

                    if strelka:
                        (
                            strelka_classification,
                            somatic_evs,
                            qss,
                            tqss,
                        ) = annotate_caller.Strelka(variant_id, strelka_variants)
                        num_callers += strelka_classification
                    else:
                        strelka_classification = somatic_evs = qss = tqss = nan

                    if tnscope:
                        tnscope_classification = annotate_caller.TNscope(
                            variant_id, tnscope_variants
                        )
                        num_callers += tnscope_classification
                    else:
                        tnscope_classification = nan

                    if platypus:
                        platypus_classification = annotate_caller.countPASS(
                            variant_id, platypus_variants
                        )
                        num_callers += platypus_classification
                    else:
                        platypus_classification = nan

                    arbitrary_classifications = {}
                    for ith_arbi_var in arbitrary_file_handle:
                        arbi_classification_i = annotate_caller.anyInputVcf(
                            variant_id, arbitrary_variants[ith_arbi_var]
                        )
                        arbitrary_classifications[ith_arbi_var] = arbi_classification_i
                        num_callers += arbi_classification_i

                    # Potentially write the output only if it meets this threshold:
                    if num_callers >= min_caller:
                        # Ground truth file
                        if truth:
                            if variant_id in truth_variants:
                                judgement = 1
                                my_identifiers.add("TruePositive")
                            else:
                                judgement = 0
                                my_identifiers.add("FalsePositive")
                        else:
                            judgement = nan

                        # dbSNP. Will overwrite dbSNP info from input VCF file
                        if dbsnp:
                            if_dbsnp, if_common, rsID = annotate_caller.dbSNP(
                                variant_id, dbsnp_variants
                            )
                            for ID_i in rsID:
                                my_identifiers.add(ID_i)

                        # COSMIC. Will overwrite COSMIC info from input VCF file
                        if cosmic:
                            if_cosmic, num_cases, cosmicID = annotate_caller.COSMIC(
                                variant_id, cosmic_variants
                            )
                            for ID_i in cosmicID:
                                my_identifiers.add(ID_i)

                        # INFO EXTRACTION FROM BAM FILES
                        nbam_feature = BamFeatures.from_alignment_file(
                            bam_fh=nbam,
                            my_coordinate=my_coordinate,
                            ref_base=ref_base,
                            first_alt=first_alt,
                            min_mq=min_mq,
                            min_bq=min_bq,
                        )
                        tbam_feature = BamFeatures.from_alignment_file(
                            bam_fh=tbam,
                            my_coordinate=my_coordinate,
                            ref_base=ref_base,
                            first_alt=first_alt,
                            min_mq=min_mq,
                            min_bq=min_bq,
                        )
                        n_ref = (
                            nbam_feature.ref_call_forward
                            + nbam_feature.ref_call_reverse
                        )
                        n_alt = (
                            nbam_feature.alt_call_forward
                            + nbam_feature.alt_call_reverse
                        )
                        t_ref = (
                            tbam_feature.ref_call_forward
                            + tbam_feature.ref_call_reverse
                        )
                        t_alt = (
                            tbam_feature.alt_call_forward
                            + tbam_feature.alt_call_reverse
                        )
                        sor = seq_features.somatic_odds_ratio(
                            n_ref, n_alt, t_ref, t_alt
                        )

                        # Calculate VarScan'2 SCC directly without using
                        # VarScan2 output:
                        try:
                            score_varscan2 = genome.p2phred(
                                stats.fisher_exact(
                                    ((t_alt, n_alt), (t_ref, n_ref)),
                                    alternative="greater",
                                )[1]
                            )
                        except ValueError:
                            score_varscan2 = nan

                        # Homopolymer eval:
                        (
                            homopolymer_length,
                            site_homopolymer_length,
                        ) = seq_features.get_homopolymer_lengths(
                            ref_fa, my_coordinate, ref_base, first_alt
                        )

                        # Linguistic sequence complexity in a +/-80bp window,
                        # but substring calculation stops at 20-bp substring.
                        seq_span_80bp = ref_fa.fetch(
                            my_coordinate[0],
                            max(0, my_coordinate[1] - 41),
                            my_coordinate[1] + 40,
                        )
                        seq_left_80bp = ref_fa.fetch(
                            my_coordinate[0],
                            max(0, my_coordinate[1] - 81),
                            my_coordinate[1],
                        )
                        seq_right_80bp = ref_fa.fetch(
                            my_coordinate[0], my_coordinate[1], my_coordinate[1] + 81
                        )

                        if len(seq_span_80bp) > 20:
                            LC_spanning = (
                                seq_features.ling_seq_complexity_with_max_vocab_length(
                                    seq_span_80bp, 20
                                )
                            )
                        else:
                            LC_spanning = math.nan

                        if len(seq_left_80bp) > 20:
                            left_LC = (
                                seq_features.ling_seq_complexity_with_max_vocab_length(
                                    seq_left_80bp, 20
                                )
                            )
                        else:
                            left_LC = math.nan

                        if len(seq_right_80bp) > 20:
                            right_LC = (
                                seq_features.ling_seq_complexity_with_max_vocab_length(
                                    seq_right_80bp, 20
                                )
                            )
                        else:
                            right_LC = math.nan

                        LC_adjacent = min(left_LC, right_LC)

                        LC_spanning_phred = genome.p2phred(1 - LC_spanning, 40)
                        LC_adjacent_phred = genome.p2phred(1 - LC_adjacent, 40)

                        # Fill the ID field of the TSV/VCF
                        my_identifiers = (
                            ";".join(my_identifiers) if my_identifiers else "."
                        )
                        out_line_part_1 = out_header.format(
                            CHROM=my_coordinate[0],
                            POS=my_coordinate[1],
                            ID=my_identifiers,
                            REF=ref_base,
                            ALT=first_alt,
                            if_MuTect=mutect_classification,
                            if_VarScan2=varscan_classification,
                            if_JointSNVMix2=jointsnvmix2_classification,
                            if_SomaticSniper=sniper_classification,
                            if_VarDict=vardict_classification,
                            MuSE_Tier=muse_classification,
                            if_LoFreq=lofreq_classification,
                            if_Scalpel=scalpel_classification,
                            if_Strelka=strelka_classification,
                            if_TNscope=tnscope_classification,
                            if_Platypus=platypus_classification,
                            Strelka_Score=somatic_evs,
                            Strelka_QSS=qss,
                            Strelka_TQSS=tqss,
                            VarScan2_Score=rescale(
                                score_varscan2, "phred", p_scale, 1001
                            ),
                            SNVMix2_Score=rescale(
                                score_jointsnvmix2, "phred", p_scale, 1001
                            ),
                            Sniper_Score=rescale(
                                score_somaticsniper, "phred", p_scale, 1001
                            ),
                            VarDict_Score=rescale(
                                score_vardict, "phred", p_scale, 1001
                            ),
                            if_dbsnp=if_dbsnp,
                            COMMON=if_common,
                            if_COSMIC=if_cosmic,
                            COSMIC_CNT=num_cases,
                            Consistent_Mates=tbam_feature.consistent_mates,
                            Inconsistent_Mates=tbam_feature.inconsistent_mates,
                            Seq_Complexity_Span=LC_spanning_phred,
                            Seq_Complexity_Adj=LC_adjacent_phred,
                            N_DP=nbam_feature.dp,
                            nBAM_REF_MQ="%g" % nbam_feature.ref_mq,
                            nBAM_ALT_MQ="%g" % nbam_feature.alt_mq,
                            nBAM_p_MannWhitneyU_MQ="%g"
                            % nbam_feature.p_mannwhitneyu_mq,
                            nBAM_REF_BQ="%g" % nbam_feature.ref_bq,
                            nBAM_ALT_BQ="%g" % nbam_feature.alt_bq,
                            nBAM_p_MannWhitneyU_BQ="%g"
                            % nbam_feature.p_mannwhitneyu_bq,
                            nBAM_REF_NM="%g" % nbam_feature.ref_edit_distance,
                            nBAM_ALT_NM="%g" % nbam_feature.alt_edit_distance,
                            nBAM_NM_Diff="%g" % nbam_feature.edit_distance_difference,
                            nBAM_REF_Concordant=nbam_feature.ref_concordant_reads,
                            nBAM_REF_Discordant=nbam_feature.ref_discordant_reads,
                            nBAM_ALT_Concordant=nbam_feature.alt_concordant_reads,
                            nBAM_ALT_Discordant=nbam_feature.alt_discordant_reads,
                            nBAM_Concordance_FET=rescale(
                                nbam_feature.concordance_fet,
                                "fraction",
                                p_scale,
                                1001,
                            ),
                            N_REF_FOR=nbam_feature.ref_call_forward,
                            N_REF_REV=nbam_feature.ref_call_reverse,
                            N_ALT_FOR=nbam_feature.alt_call_forward,
                            N_ALT_REV=nbam_feature.alt_call_reverse,
                            nBAM_StrandBias_FET=rescale(
                                nbam_feature.strandbias_fet,
                                "fraction",
                                p_scale,
                                1001,
                            ),
                            nBAM_p_MannWhitneyU_EndPos="%g"
                            % nbam_feature.p_mannwhitneyu_endpos,
                            nBAM_REF_Clipped_Reads=nbam_feature.ref_soft_clipped_reads,
                            nBAM_ALT_Clipped_Reads=nbam_feature.alt_soft_clipped_reads,
                            nBAM_Clipping_FET=rescale(
                                nbam_feature.clipping_fet, "fraction", p_scale, 1001
                            ),
                            nBAM_MQ0=nbam_feature.mq0_reads,
                            nBAM_Other_Reads=nbam_feature.noise_read_count,
                            nBAM_Poor_Reads=nbam_feature.poor_read_count,
                            nBAM_REF_InDel_3bp=nbam_feature.ref_indel_3bp,
                            nBAM_REF_InDel_2bp=nbam_feature.ref_indel_2bp,
                            nBAM_REF_InDel_1bp=nbam_feature.ref_indel_1bp,
                            nBAM_ALT_InDel_3bp=nbam_feature.alt_indel_3bp,
                            nBAM_ALT_InDel_2bp=nbam_feature.alt_indel_2bp,
                            nBAM_ALT_InDel_1bp=nbam_feature.alt_indel_1bp,
                            M2_NLOD=nlod,
                            M2_TLOD=tlod,
                            M2_STR=tandem,
                            M2_ECNT=ecnt,
                            SOR=sor,
                            MSI=msi,
                            MSILEN=msilen,
                            SHIFT3=shift3,
                            MaxHomopolymer_Length=homopolymer_length,
                            SiteHomopolymer_Length=site_homopolymer_length,
                            T_DP=tbam_feature.dp,
                            tBAM_REF_MQ="%g" % tbam_feature.ref_mq,
                            tBAM_ALT_MQ="%g" % tbam_feature.alt_mq,
                            tBAM_p_MannWhitneyU_MQ="%g"
                            % tbam_feature.p_mannwhitneyu_mq,
                            tBAM_REF_BQ="%g" % tbam_feature.ref_bq,
                            tBAM_ALT_BQ="%g" % tbam_feature.alt_bq,
                            tBAM_p_MannWhitneyU_BQ="%g"
                            % tbam_feature.p_mannwhitneyu_bq,
                            tBAM_REF_NM="%g" % tbam_feature.ref_edit_distance,
                            tBAM_ALT_NM="%g" % tbam_feature.alt_edit_distance,
                            tBAM_NM_Diff="%g" % tbam_feature.edit_distance_difference,
                            tBAM_REF_Concordant=tbam_feature.ref_concordant_reads,
                            tBAM_REF_Discordant=tbam_feature.ref_discordant_reads,
                            tBAM_ALT_Concordant=tbam_feature.alt_concordant_reads,
                            tBAM_ALT_Discordant=tbam_feature.alt_discordant_reads,
                            tBAM_Concordance_FET=rescale(
                                tbam_feature.concordance_fet,
                                "fraction",
                                p_scale,
                                1001,
                            ),
                            T_REF_FOR=tbam_feature.ref_call_forward,
                            T_REF_REV=tbam_feature.ref_call_reverse,
                            T_ALT_FOR=tbam_feature.alt_call_forward,
                            T_ALT_REV=tbam_feature.alt_call_reverse,
                            tBAM_StrandBias_FET=rescale(
                                tbam_feature.strandbias_fet,
                                "fraction",
                                p_scale,
                                1001,
                            ),
                            tBAM_p_MannWhitneyU_EndPos="%g"
                            % tbam_feature.p_mannwhitneyu_endpos,
                            tBAM_REF_Clipped_Reads=tbam_feature.ref_soft_clipped_reads,
                            tBAM_ALT_Clipped_Reads=tbam_feature.alt_soft_clipped_reads,
                            tBAM_Clipping_FET=rescale(
                                tbam_feature.clipping_fet, "fraction", p_scale, 1001
                            ),
                            tBAM_MQ0=tbam_feature.mq0_reads,
                            tBAM_Other_Reads=tbam_feature.noise_read_count,
                            tBAM_Poor_Reads=tbam_feature.poor_read_count,
                            tBAM_REF_InDel_3bp=tbam_feature.ref_indel_3bp,
                            tBAM_REF_InDel_2bp=tbam_feature.ref_indel_2bp,
                            tBAM_REF_InDel_1bp=tbam_feature.ref_indel_1bp,
                            tBAM_ALT_InDel_3bp=tbam_feature.alt_indel_3bp,
                            tBAM_ALT_InDel_2bp=tbam_feature.alt_indel_2bp,
                            tBAM_ALT_InDel_1bp=tbam_feature.alt_indel_1bp,
                            InDel_Length=indel_length,
                        )
                        additional_caller_columns = []
                        for arbi_key_i in additional_arbi_caller_numbers:
                            additional_caller_columns.append(
                                str(arbitrary_classifications[arbi_key_i])
                            )
                        additional_caller_columns = "\t".join(additional_caller_columns)

                        label_column = label_header.format(
                            TrueVariant_or_False=judgement
                        )

                        if len(additional_arbi_caller_numbers) > 0:
                            out_line = "\t".join(
                                (
                                    out_line_part_1,
                                    additional_caller_columns,
                                    label_column,
                                )
                            )
                        else:
                            out_line = "\t".join((out_line_part_1, label_column))

                        # Print it out to stdout:
                        outhandle.write(out_line + "\n")

            # Read into the next line:
            if not is_vcf:
                my_line = my_sites.readline().rstrip()

        ##########  Close all open files if they were opened  ##########
        opened_files = [
            ref_fa,
            nbam,
            tbam,
            truth,
            cosmic,
            dbsnp,
            mutect,
            varscan,
            jsm,
            sniper,
            vardict,
            muse,
            lofreq,
            scalpel,
            strelka,
            tnscope,
            platypus,
        ]
        [
            opened_files.append(extra_opened_file)
            for extra_opened_file in arbitrary_file_handle.values()
        ]
        [opened_file.close() for opened_file in opened_files if opened_file]


def main() -> None:
    run_params = run()
    vcf2tsv(
        is_vcf=run_params.vcf_format,
        is_bed=run_params.bed_format,
        is_pos=run_params.positions_list,
        nbam_fn=run_params.normal_bam_file,
        tbam_fn=run_params.tumor_bam_file,
        truth=run_params.ground_truth_vcf,
        cosmic=run_params.cosmic_vcf,
        dbsnp=run_params.dbsnp_vcf,
        mutect=run_params.mutect_vcf,
        varscan=run_params.varscan_vcf,
        jsm=run_params.jsm_vcf,
        sniper=run_params.somaticsniper_vcf,
        vardict=run_params.vardict_vcf,
        muse=run_params.muse_vcf,
        lofreq=run_params.lofreq_vcf,
        scalpel=run_params.scalpel_vcf,
        strelka=run_params.strelka_vcf,
        tnscope=run_params.tnscope_vcf,
        platypus=run_params.platypus_vcf,
        arbitrary_vcfs=run_params.arbitrary_vcfs,
        dedup=run_params.deduplicate,
        min_mq=run_params.minimum_mapping_quality,
        min_bq=run_params.minimum_base_quality,
        min_caller=run_params.minimum_num_callers,
        ref_fa=run_params.genome_reference,
        p_scale=run_params.p_scale,
        outfile=run_params.output_tsv_file,
    )


if __name__ == "__main__":
    main()
