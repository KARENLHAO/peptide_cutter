#!/data/PRG/tools/Biomolecules/miniconda3/bin/python
"""
Peptide Cleavage Site Recognition Program
Based on ExPASy PeptideCutter cleavage rules
"""

import re
import argparse
import sys
from typing import List, Tuple, Dict


class PeptideCutter:
    """蛋白质酶切位点识别器"""
    
    def __init__(self):
        self.enzymes = self._init_enzyme_rules()
    
    def _init_enzyme_rules(self) -> Dict:
        """初始化所有酶的切割规则"""
        return {
            "Arg-C": {
                "desc": "Arg-C proteinase",
                "pattern": r"R",
                "cut_after": True
            },
            "Asp-N": {
                "desc": "Asp-N endopeptidase",
                "pattern": r"(?=[D])",
                "cut_after": False
            },
            "Asp-N_Glu": {
                "desc": "Asp-N endopeptidase + N-terminal Glu",
                "pattern": r"(?=[DE])",
                "cut_after": False
            },
            "BNPS-Skatole": {
                "desc": "BNPS-Skatole",
                "pattern": r"W",
                "cut_after": True
            },
            "Caspase_1": {
                "desc": "Caspase 1",
                "pattern": r"[FWYL][HAT]D(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_2": {
                "desc": "Caspase 2",
                "pattern": r"DVAD(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_3": {
                "desc": "Caspase 3",
                "pattern": r"DMQD(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_4": {
                "desc": "Caspase 4",
                "pattern": r"LEVD(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_5": {
                "desc": "Caspase 5",
                "pattern": r"[LW]EHD",
                "cut_after": True
            },
            "Caspase_6": {
                "desc": "Caspase 6",
                "pattern": r"VE[HI]D(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_7": {
                "desc": "Caspase 7",
                "pattern": r"DEVD(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_8": {
                "desc": "Caspase 8",
                "pattern": r"[IL]ETD(?![PEDQKR])",
                "cut_after": True
            },
            "Caspase_9": {
                "desc": "Caspase 9",
                "pattern": r"LEHD",
                "cut_after": True
            },
            "Caspase_10": {
                "desc": "Caspase 10",
                "pattern": r"IEAD",
                "cut_after": True
            },
            "Chymotrypsin_high": {
                "desc": "Chymotrypsin (high specificity)",
                "pattern": r"[FY](?!P)|W(?![MP])",
                "cut_after": True
            },
            "Chymotrypsin_low": {
                "desc": "Chymotrypsin (low specificity)",
                "pattern": r"[FLY](?!P)|W(?![MP])|M(?![PY])|H(?![DMPW])",
                "cut_after": True
            },
            "Clostripain": {
                "desc": "Clostripain",
                "pattern": r"R",
                "cut_after": True
            },
            "CNBr": {
                "desc": "CNBr",
                "pattern": r"M",
                "cut_after": True
            },
            "Enterokinase": {
                "desc": "Enterokinase",
                "pattern": r"[DE][DE][DE]K",
                "cut_after": True
            },
            "Factor_Xa": {
                "desc": "Factor Xa",
                "pattern": r"[AFGILTVM][DE]GR",
                "cut_after": True
            },
            "Formic_acid": {
                "desc": "Formic acid",
                "pattern": r"D",
                "cut_after": True
            },
            "Glutamyl_endopeptidase": {
                "desc": "Glutamyl endopeptidase",
                "pattern": r"E",
                "cut_after": True
            },
            "Granzyme_B": {
                "desc": "Granzyme B",
                "pattern": r"IEPD",
                "cut_after": True
            },
            "Hydroxylamine": {
                "desc": "Hydroxylamine",
                "pattern": r"NG",
                "cut_after": False
            },
            "Iodosobenzoic_acid": {
                "desc": "Iodosobenzoic acid",
                "pattern": r"W",
                "cut_after": True
            },
            "LysC": {
                "desc": "LysC",
                "pattern": r"K",
                "cut_after": True
            },
            "LysN": {
                "desc": "LysN",
                "pattern": r"(?=K)",
                "cut_after": False
            },
            "Neutrophil_elastase": {
                "desc": "Neutrophil elastase",
                "pattern": r"[AV]",
                "cut_after": True
            },
            "NTCB": {
                "desc": "NTCB",
                "pattern": r"(?=C)",
                "cut_after": False
            },
            "Pepsin_pH1.3": {
                "desc": "Pepsin (pH1.3)",
                "pattern": r"[FL](?!P)",
                "cut_after": True
            },
            "Pepsin_pH2": {
                "desc": "Pepsin (pH>2)",
                "pattern": r"[FLWY](?!P)",
                "cut_after": True
            },
            "Proline_endopeptidase": {
                "desc": "Proline endopeptidase",
                "pattern": r"[HKR]P(?!P)",
                "cut_after": True
            },
            "Proteinase_K": {
                "desc": "Proteinase K",
                "pattern": r"[AEFILTVWY]",
                "cut_after": True
            },
            "Staphylococcal_peptidase": {
                "desc": "Staphylococcal peptidase I",
                "pattern": r"(?<!E)E",
                "cut_after": True
            },
            "Thermolysin": {
                "desc": "Thermolysin",
                "pattern": r"(?<![DE])(?=[AFILMV])",
                "cut_after": False
            },
            "Thrombin": {
                "desc": "Thrombin",
                "pattern": r"GR(?=G)",
                "cut_after": True
            },
            "Trypsin": {
                "desc": "Trypsin",
                "pattern": r"[KR](?!P)",
                "cut_after": True
            }
        }
    
    def find_cleavage_sites(self, sequence: str, enzyme: str) -> List[Tuple[int, str]]:
        """
        在序列中查找指定酶的切割位点
        
        参数:
            sequence: 蛋白质序列(单字母代码)
            enzyme: 酶名称
        
        返回:
            切割位点列表,每个元素为(位置, 上下文序列)
        """
        if enzyme not in self.enzymes:
            raise ValueError(f"Unknown enzyme: {enzyme}")
        
        rule = self.enzymes[enzyme]
        pattern = rule["pattern"]
        cut_after = rule["cut_after"]
        
        sites = []
        sequence = sequence.upper()
        
        # 查找所有匹配位置
        for match in re.finditer(pattern, sequence):
            if cut_after:
                pos = match.end()
            else:
                pos = match.start()
            
            # 获取切割位点的上下文(前后各5个氨基酸)
            start = max(0, pos - 5)
            end = min(len(sequence), pos + 5)
            context = sequence[start:end]
            
            # 添加切割标记
            cut_pos_in_context = pos - start
            context_with_cut = context[:cut_pos_in_context] + "|" + context[cut_pos_in_context:]
            
            sites.append((pos, context_with_cut))
        
        return sites
    
    def cut_sequence(self, sequence: str, enzyme: str) -> List[str]:
        """
        根据指定酶切割序列
        
        参数:
            sequence: 蛋白质序列
            enzyme: 酶名称
        
        返回:
            切割后的肽段列表
        """
        sites = self.find_cleavage_sites(sequence, enzyme)
        if not sites:
            return [sequence]
        
        fragments = []
        last_pos = 0
        
        for pos, _ in sites:
            fragments.append(sequence[last_pos:pos])
            last_pos = pos
        
        # 添加最后一个片段
        if last_pos < len(sequence):
            fragments.append(sequence[last_pos:])
        
        return [f for f in fragments if f]  # 移除空片段
    
    def list_enzymes(self) -> List[str]:
        """返回所有可用的酶名称列表"""
        return sorted(self.enzymes.keys())


def read_fasta_file(filepath: str) -> Dict[str, str]:
    """从FASTA文件读取序列"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        sequences = {}
        current_id = None
        current_seq = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('>'):
                # 保存上一个序列
                if current_id is not None:
                    sequences[current_id] = ''.join(current_seq)
                # 开始新序列
                current_id = line[1:].split()[0]  # 取第一个词作为ID
                current_seq = []
            else:
                current_seq.append(line)
        
        # 保存最后一个序列
        if current_id is not None:
            sequences[current_id] = ''.join(current_seq)
        
        # 如果没有FASTA格式的header，作为单一序列处理
        if not sequences:
            sequence = ''.join(line.strip() for line in lines if line.strip())
            sequences['sequence'] = sequence
        
        return sequences
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Peptide Cleavage Site Recognition Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available enzymes
  %(prog)s --list
  
  # Analyze sequence with Trypsin
  %(prog)s -s MKTAYIAKQRQISFVK -e Trypsin
  
  # Analyze sequence from FASTA file with multiple enzymes
  %(prog)s -f sequence.fasta -e Trypsin LysC Arg-C
  
  # Show all cleavage sites (no limit)
  %(prog)s -s MKTAYIAKQRQISFVK -e Trypsin --show-all-sites
  
  # Show limited cleavage sites and fragments
  %(prog)s -s MKTAYIAKQRQISFVK -e Trypsin --show-sites --show-fragments --max-sites 5
        """
    )
    
    parser.add_argument('-s', '--sequence', type=str,
                        help='Input protein sequence (single letter code)')
    parser.add_argument('-f', '--file', type=str,
                        help='Input sequence file (FASTA format supported)')
    parser.add_argument('-e', '--enzyme', type=str, nargs='+',
                        help='Enzyme name(s) for cleavage analysis')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List all available enzymes')
    parser.add_argument('--show-sites', action='store_true',
                        help='Show detailed cleavage sites with context')
    parser.add_argument('--show-all-sites', action='store_true',
                        help='Show ALL cleavage sites (no limit)')
    parser.add_argument('--show-fragments', action='store_true',
                        help='Show all peptide fragments')
    parser.add_argument('--max-sites', type=int, default=10,
                        help='Maximum number of sites to display (default: 10, use with --show-sites)')
    parser.add_argument('--max-fragments', type=int, default=10,
                        help='Maximum number of fragments to display (default: 10)')
    
    args = parser.parse_args()
    
    cutter = PeptideCutter()
    
    # 列出所有酶
    if args.list:
        print("Available enzymes:")
        print("=" * 60)
        for enzyme in cutter.list_enzymes():
            desc = cutter.enzymes[enzyme]['desc']
            print(f"  {enzyme:<30} {desc}")
        return
    
    # 检查是否提供了序列
    if not args.sequence and not args.file:
        parser.print_help()
        print("\nError: Please provide a sequence using -s or -f option.")
        sys.exit(1)
    
    # 获取序列
    sequences = {}
    if args.file:
        sequences = read_fasta_file(args.file)
        print(f"Sequence(s) loaded from file: {args.file}")
        if len(sequences) > 1:
            print(f"Found {len(sequences)} sequences in the file")
    else:
        sequences['input'] = args.sequence
    
    # 检查是否提供了酶
    if not args.enzyme:
        print("Error: Please specify at least one enzyme using -e option.")
        print("Use --list to see all available enzymes.")
        sys.exit(1)
    
    # 处理每个序列
    for seq_id, sequence in sequences.items():
        sequence = sequence.upper().strip()
        
        if len(sequences) > 1:
            print("\n" + "=" * 70)
            print(f"Sequence ID: {seq_id}")
            print("=" * 70)
        
        print(f"Sequence length: {len(sequence)} amino acids")
        print()
        
        # 分析每个酶
        for enzyme in args.enzyme:
            if enzyme not in cutter.enzymes:
                print(f"Warning: Unknown enzyme '{enzyme}', skipping...")
                continue
            
            print("=" * 70)
            print(f"Enzyme: {enzyme}")
            print(f"Description: {cutter.enzymes[enzyme]['desc']}")
            print("-" * 70)
            
            try:
                sites = cutter.find_cleavage_sites(sequence, enzyme)
                fragments = cutter.cut_sequence(sequence, enzyme)
                
                print(f"Number of cleavage sites: {len(sites)}")
                print(f"Number of peptide fragments: {len(fragments)}")
                
                # 显示所有切割位点
                if args.show_all_sites and sites:
                    print("\nAll cleavage sites:")
                    for i, (pos, context) in enumerate(sites, 1):
                        print(f"  {i:3d}. Position {pos:4d}: {context}")
                # 显示部分切割位点
                elif args.show_sites and sites:
                    print("\nCleavage sites:")
                    for i, (pos, context) in enumerate(sites[:args.max_sites], 1):
                        print(f"  {i:3d}. Position {pos:4d}: {context}")
                    if len(sites) > args.max_sites:
                        print(f"  ... and {len(sites) - args.max_sites} more sites")
                        print(f"  (Use --show-all-sites to display all sites)")
                
                # 显示片段
                if args.show_fragments and fragments:
                    print("\nPeptide fragments:")
                    for i, frag in enumerate(fragments[:args.max_fragments], 1):
                        print(f"  {i:3d}. Length {len(frag):4d}: {frag}")
                    if len(fragments) > args.max_fragments:
                        print(f"  ... and {len(fragments) - args.max_fragments} more fragments")
                
                # 片段长度统计
                if fragments:
                    lengths = [len(f) for f in fragments]
                    print(f"\nFragment length statistics:")
                    print(f"  Min: {min(lengths)}, Max: {max(lengths)}, "
                          f"Average: {sum(lengths)/len(lengths):.1f}")
                
                print()
                
            except Exception as e:
                print(f"Error analyzing with {enzyme}: {e}")
                print()


if __name__ == "__main__":
    main()
