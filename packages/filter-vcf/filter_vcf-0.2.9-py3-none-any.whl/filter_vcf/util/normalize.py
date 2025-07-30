from logging import Logger
import os

from filter_vcf.util.detectVcf import detect_vcf
from filter_vcf.util.convertChrName import convert_chr_name
from filter_vcf.util.execSubprocess import exec_subprocess


def normalize(in_file: str, ref_file: str, tmp_dir: str, filter_contig: bool, log: Logger):
    vcfChr = detect_vcf(in_file)
    log.info(f"Input vcf file <{in_file}> has type <{ vcfChr }>")

    if vcfChr == "chr":
        log.info("Converting chr to num")
        convert_chr_name(in_file, "num")
        if os.path.exists(f"{in_file}.tbi"):
            os.remove(f"{in_file}.tbi")
        log.info("Indexing with tabix")
        exec_subprocess(f"tabix -p vcf {in_file}", log)
        log.info("Normalizing")
        exec_subprocess(
            f"vt normalize -n -r {ref_file} {in_file} -o {tmp_dir}/normalized.vcf",
            log,
        )
        log.info("Gzipping")
        exec_subprocess(f"gzip {tmp_dir}/normalized.vcf", log)
        os.rename(f"{tmp_dir}/normalized.vcf.gz", in_file)
        log.info("Converting num to chr")
        convert_chr_name(in_file, "chr")

    else:
        if not filter_contig:
            log.info("Indexing with tabix")
            exec_subprocess(f"tabix -p vcf {in_file}", log)
        log.info("Normalizing")
        exec_subprocess(
            f"vt normalize -n -r {ref_file} {in_file} -o {tmp_dir}/normalized.vcf",
            log,
        )
        log.info("Gzipping")
        exec_subprocess(f"gzip {tmp_dir}/normalized.vcf", log)
        os.rename(f"{tmp_dir}/normalized.vcf.gz", in_file)
