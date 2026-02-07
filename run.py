#!/data/PRG/tools/Biomolecules/miniconda3/bin/python

import argparse
import sys
from subprocess import Popen

PYTHON_BIN = "/home/vscode/.conda/envs/peptide-cutter/bin/python"
PEPTIDE_CUTTER_SCRIPT = "/data/PRG/tools/Biomolecules/miniconda3/bin/peptide-cutter"


def run_ext_cmder(cmds: list, query: str = None) -> str:
    """功能: 执行外部命令行工具
    - cmds: 待执行命令, List格式[cmder, option, value...]
    - query: 可交互执行程序命令组合, 使用\\n标记回车
    """
    print("Run External Cmd: " + " ".join(cmds))
    process = Popen(cmds, stdout=sys.stdout, stderr=sys.stderr)
    retcode = process.wait()
    if retcode:
        raise RuntimeError("Run Ext Cmd Faile")
    return ""


def main():
    parser = argparse.ArgumentParser(description="Peptide Cutter Tool Wrapper")
    parser.add_argument(
        "--input",
        required=True,
        help="Input file in FASTA format.",
    )
    parser.add_argument(
        "--enzymes",
        type=str,
        default="all",
        help="Enzyme names or abbreviations. Use 'all' for all enzymes. "
        "Multiple enzymes can be provided as a semicolon-separated string.",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: .).",
    )
    parser.add_argument(
        "--line-width",
        type=int,
        default=60,
        help="Line width for sequence display and Part 4 blocks (10-60).",
    )
    args = parser.parse_args()

    cmd = [
        PYTHON_BIN,
        PEPTIDE_CUTTER_SCRIPT,
        "--fasta",
        args.input,
        "--out",
        args.output,
        "--enzymes",
        args.enzymes,
        "--line-width",
        str(args.line_width),
        "--cleanup-tmp",
    ]

    run_ext_cmder(cmd)
