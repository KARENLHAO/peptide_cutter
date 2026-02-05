# Cleavage Rules and References

This document summarizes enzyme/chemical cleavage behavior and references used by PeptideCutter.

## Cleavage Rules (Narrative)

### Arg-C proteinase
The Arg-C proteinase preferentially cleaves at Arg in position P1. The cleavage behaviour seems to be only moderately affected by residues in position P1' (Keil, 1992).

### Asp-N endopeptidase
Cleaves specifically bonds with Asp in position P1' (Keil, 1992).

### Asp-N endopeptidase + N-terminal Glu
Cleaves specifically bonds with Asp or Glu in position P1' (Keil, 1992).

### BNPS-Skatole
BNPS-skatole [2-(2-nitrophenylsulfenyl)-3-methylindole] is a mild oxidant and brominating reagent that leads to polypeptide cleavage on the C-terminal side of tryptophan residues.

### Caspase 1
Caspase-1 acts on Interleukin-1 beta [Precursor] (P01584) to release it by specific cleavage at 116-Asp-|-Ala-117 (YVHDA) and 27-Asp-|-Gly-28 (EADG) bonds. It also hydrolyzes small-molecule substrates such as Ac-Tyr-Val-Ala-Asp-|-NHMec. Generally the substrate/enzyme interaction is located between positions P4 and P1'. Various patterns were proposed such as YEVD|X (Talanian et al., 1997) or WEHD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997). The pattern implemented for PeptideCutter considers an extended rule based on Earnshaw et al., 1999, and is described in the table at the end of this document.

### Caspase 2
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are DVAD|X (Talanian et al., 1997) or DEHD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 3
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are DMQD|X (Talanian et al., 1997) or DEVD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 4
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are LEVD|X (Talanian et al., 1997) or (W/L)EHD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 5
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are (W/L)EHD|X (Thornberry et al., 1997).

### Caspase 6
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are VEID|X (Talanian et al., 1997) or VEHD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 7
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are DEVD|X (Talanian et al., 1997; Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 8
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are IETD|X (Talanian et al., 1997) or LETD|X (Thornberry et al., 1997), where X is any amino acid but Pro, Glu, Asp, Gln, Lys, Arg (Stennicke et al., 2000; Talanian et al., 1997).

### Caspase 9
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are LEHD|X (Thornberry et al., 1997).

### Caspase 10
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are IEAD|X (Talanian et al., 1997).

### Chymotrypsin
Chymotrypsin preferentially cleaves at Trp, Tyr and Phe in position P1 (high specificity) and, to a lesser extent (low specificity), at Leu, Met and His in position P1 (Keil, 1992). Exceptions: when Trp is in P1, cleavage is blocked if Met or Pro is in P1'. Pro in P1' nearly fully blocks cleavage independent of P1. When Met is in P1, cleavage is blocked by Tyr in P1'. When His is in P1, cleavage is blocked by Asp, Met or Trp.

### Clostripain (Clostridiopeptidase B)
Clostripain cleaves preferentially at the carboxyl group of Arg in position P1 (Keil, 1992). This cleavage is not strict, especially when proteolysis time is short or when using specific native substrates. Cleavage at Lys is rare. Clostripain accepts Lys instead of Arg, but reaction rates are very low. The enzyme is sensitive to substrate-site composition; no strict rules can be defined. Glu and Asp in position P1' may protect against cleavage, as well as accumulation of positive charge in positions P1' to P4'.

### CNBr
CNBr cleaves at Met in position P1 (information from the Cutter of the Prolysis program/Universite de Tours). When CNBr is not applied in large excess, cleavage may be incomplete. Resistance can result from Ser or Thr in P1' (Met converts to homoserine, preventing cleavage) or P2 (Schroeder et al., 1969). This blocking can be prevented by using CNBr in large excess relative to Met residues.

### Enterokinase
Enterokinase recognizes -Asp-Asp-Asp-Asp-Lys-|-X with high specificity and activates trypsinogen by cleavage at the C-terminal end of this sequence. Asp may be substituted by Glu. PeptideCutter does not consider position P5, so the implemented motif is [DE][DE][DE]K-X.

### Factor Xa
Coagulation factor Xa is prepared by activation of its precursor Factor X via hydrolysis of a specific peptide bond in the amino-terminal region of the heavy chain (Fujikawa et al., 1975). Highly specific for cleavage at Arg (P1) and Gly (P2). In general, P3 is negatively charged (Glu or Asp) and P4 may be hydrophobic (Ile or Ala). P'-site composition does not strongly influence cleavage.

### Formic acid
Cleaves at Asp in position P1 (Li et al., 2001).

### Glutamyl endopeptidase
Three main types are commercially available (Birktoft and Breddam, 1994): GluBl (Bacillus licheniformis), GluSGB (Streptomyces griseus), GluV8 (Streptococcus aureus, strain V8). All preferentially cleave at Glu in P1. When Glu and Asp are adjacent, cleavage at Glu is preferred 100-fold (GluSGB) to around 1000-fold (others) compared to Asp in P1. Buffer composition (bicarbonate vs phosphate) affects overall reactivity but not the ratio (Houmard and Drapeau, 1972). Preferred cleavage-site composition: Asp in P4; Ala/Val in P3; Pro/Val in P2 (GluSGB) or Phe in P2 (GluBl/GluV8). Cleavage is disfavored by Pro in P3, P1', and P2', and by Asp at P1'.

### Granzyme B
The present version of PeptideCutter considers only preferred substrate sites (Earnshaw et al., 1999): cleavage preferentially occurs at sites where positions P4 to P1' are IEPD|X (Thornberry et al., 1997).

### Hydroxylamine (NH2OH)
Cleaves at Asn in position P1 and Gly in position P1' (Bornstein & Balian, 1977).

### Iodosobenzoic acid
Cleaves at Trp in position P1 (Han et al., 1983).

### LysC (Lysyl endopeptidase; Achromobacter proteinase I)
Cleaves at Lys in position P1 (Keil, 1992).

### LysN (Peptidyl-Lys metalloendopeptidase)
Cleaves at Lys in position P1' (Keil, 1992).

### Neutrophil elastase
Cleaves at Val or Ala in position P1 (EC 3.4.21.37).

### NTCB +Ni (2-nitro-5-thiocyanobenzoic acid)
Cleaves at Cys in position P1' (Degani and Patchornik, 1974).

### Pepsin
Pepsin preferentially cleaves at Phe, Tyr, Trp and Leu in position P1 or P1' (Keil, 1992). Negative effects on cleavage are exerted by Arg, Lys and His in position P3 and Arg in position P1. Pro has favorable effects when located in P4 and P3, but unfavorable effects when found in positions P2 to P3'. Cleavage is more specific at pH 1.3. At pH 1.3, pepsin preferentially cleaves at Phe and Leu in P1 with negligible cleavage for other amino acids in P1. This specificity is lost at pH >= 2.

### Proline-endopeptidase
Proline-endopeptidase preferentially cleaves at Pro in position P1 (Keil, 1992). It may also accept Ala in P1. With Pro in P1, activity is blocked when another Pro is at P1'. In most cases a basic amino acid (Lys, His, Arg) is found in P2; this feature is suggested to be obligatory. Some discrepancies were observed, possibly due to impurities or different sources of Pro-endopeptidases.

NOTE: Proline-endopeptidase was reported to cleave only substrates whose sequences do not exceed 30 amino acids. An unusual beta-propeller domain regulates proteolysis: see Fulop et al., 1998.

### Proteinase K
Proteinase K preferentially cleaves at aliphatic or aromatic amino acid residues in position P1 (Keil, 1992). Ala in position P2 enhances cleavage. Specificity is not always unambiguous.

### Staphylococcal peptidase I
Preferentially cleaves at Glu in position P1, but also, to a lesser extent, at Asp in position P1 (Keil, 1992). In rare cases Ser can be accepted in P1. Specificity depends strongly on experimental conditions; buffer exchange (not necessarily pH) can change cleavage behavior. When two Glu residues are adjacent, Staphylococcal peptidase I prefers to cut at Glu in P1 with another Glu in P1' rather than the second Glu in P2.

### Tobacco etch virus protease
TEV protease (27 kDa catalytic domain of the NIa protein) recognizes a linear epitope of the form E-Xaa-Xaa-Y-Xaa-Q-(G/S), with cleavage between Q and G or Q and S. The most commonly used sequence is ENLYFQG (Waugh, 2002; TEV protease FAQ). PeptideCutter does not take into account positions P5 and P6, so the implemented motif is XYXQ-[GS].

### Thermolysin
Thermolysin preferentially cleaves sites with bulky and aromatic residues (Ile, Leu, Val, Ala, Met, Phe) in position P1' (Keil, 1992). Cleavage is favored with aromatic sites in position P1 but hindered by acidic residues in P1. Pro blocks when located in position P2' but not when found in P1.

### Thrombin
Preferentially cleaves at Arg in position P1 (Keil, 1992). The natural substrate is fibrinogen. Optimum cleavage sites include Arg in P1 and Gly in P2 and P1'. Likewise, hydrophobic residues in P4 and P3, Pro in P2, Arg in P1, and non-acidic amino acids in P1' and P2' are favored. A very important residue for its natural substrate fibrinogen is Asp in P10 (neglected in PeptideCutter).

### Trypsin
Preferentially cleaves at Arg and Lys in P1 with higher rates for Arg (Keil, 1992), especially at high pH (treated equally in the program). Pro usually blocks action when found in P1', but not when Lys is in P1 and Trp is in P2 at the same time. This blocking is also negligible when Arg is in P1 and Met is in P2 (other reports say the block can be circumvented by Glu in P2).

Furthermore, if Lys is found in P1, the following situations considerably block trypsin: Asp in P2 and Asp in P1', or Cys in P2 and Asp in P1', or Cys in P2 and His in P1', or Cys in P2 and Tyr in P1'. A likewise considerable block occurs when Arg is in P1 and the following situations are found: Arg in P2 and His in P1', or Cys in P2 and Lys in P1', or Arg in P2 and Arg in P1'.

This Arg/Lys specificity is seen with pure alpha- and beta-trypsins. Trypsin preparations with traces of "pseudotrypsin" also cleave at P1 residues such as Phe (except with Glu or Pro in P1'), Tyr (except with Pro and Arg in P1'), Trp (except with Ile, Lys, Pro, Val and Trp in P1'), Met (with Ala, His, Met, Gln, Ser, Val and Trp in P1') and Cys (with Phe, Gly, Ile, Leu, Val and Trp in P1').

## Comprehensive Protease and Chemical Cleavage Rules (Table)

| Enzyme / Chemical Name | P4 | P3 | P2 | P1 | P1' | P2' |
| --- | --- | --- | --- | --- | --- | --- |
| Arg-C proteinase | - | - | - | R | - | - |
| Asp-N endopeptidase | - | - | - | - | D | - |
| Asp-N endopeptidase + N-terminal Glu | - | - | - | - | D or E | - |
| BNPS-Skatole | - | - | - | W | - | - |
| Caspase 1 | F,W,Y or L | - | H,A or T | D | not P,E,D,Q,K or R | - |
| Caspase 2 | D | V | A | D | not P,E,D,Q,K or R | - |
| Caspase 3 | D | M | Q | D | not P,E,D,Q,K or R | - |
| Caspase 4 | L | E | V | D | not P,E,D,Q,K or R | - |
| Caspase 5 | L or W | E | H | D | - | - |
| Caspase 6 | V | E | H or I | D | not P,E,D,Q,K or R | - |
| Caspase 7 | D | E | V | D | not P,E,D,Q,K or R | - |
| Caspase 8 | I or L | E | T | D | not P,E,D,Q,K or R | - |
| Caspase 9 | L | E | H | D | - | - |
| Caspase 10 | I | E | A | D | - | - |
| Chymotrypsin-high specificity (C-term to [FYW], not before P) | - | - | - | F or Y | not P | - |
|  | - | - | - | W | not M or P | - |
| Chymotrypsin-low specificity (C-term to [FYWML], not before P) | - | - | - | F,L or Y | not P | - |
|  | - | - | - | W | not M or P | - |
|  | - | - | - | M | not P or Y | - |
|  | - | - | - | H | not D,M,P or W | - |
| Clostripain (Clostridiopeptidase B) | - | - | - | R | - | - |
| CNBr | - | - | - | M | - | - |
| Enterokinase | D or E | D or E | D or E | K | - | - |
| Factor Xa | A,F,G,I,L,T,V or M | D or E | G | R | - | - |
| Formic acid | - | - | - | D | - | - |
| Glutamyl endopeptidase | - | - | - | E | - | - |
| GranzymeB | I | E | P | D | - | - |
| Hydroxylamine (NH2OH) | - | - | - | N | G | - |
| Iodosobenzoic acid | - | - | - | W | - | - |
| LysC | - | - | - | K | - | - |
| LysN | - | - | - | - | K | - |
| Neutrophil elastase | - | - | - | A or V | - | - |
| NTCB (2-nitro-5-thiocyanobenzoic acid) | - | - | - | - | C | - |
| Pepsin (pH1.3) | - | not H,K or R | not P | not R | F or L | not P |
|  | - | not H,K or R | not P | F or L | - | not P |
| Pepsin (pH>2) | - | not H,K or R | not P | not R | F,L,W or Y | not P |
|  | - | not H,K or R | not P | F,L,W or Y | - | not P |
| Proline-endopeptidase[*] | - | - | H,K or R | P | not P | - |
| Proteinase K | - | - | - | A,E,F,I,L,T,V,W or Y | - | - |
| Staphylococcal peptidase I | - | - | not E | E | - | - |
| Tobacco etch virus protease | - | Y | - | Q | G or S | - |
| Thermolysin | - | - | - | not D or E | A,F,I,L,M or V | not P |
| Thrombin | - | - | G | R | G | - |
|  | A,F,G,I,L,T,V or M | A,F,G,I,L,T,V,W or R | P | R | not D or E | not D or E |
| Trypsin | - | - | - | K or R | not P | - |
|  | - | - | W | K | P | - |
|  | - | - | M | R | P | - |

*注：脯氨酸内肽酶仅能切割序列不超过30个氨基酸的底物。一种特殊的β螺旋结构域调控蛋白质水解：参见 Fulop 等，1998 年。

## Trypsin Exceptions (Blocking Rules)

| Enzyme Name | P4 | P3 | P2 | P1 | P1' | P2' |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Trypsin | - | - | C or D | K | D | - |
| Trypsin | - | - | C | K | H or Y | - |
| Trypsin | - | - | C | R | K | - |
| Trypsin | - | - | R | R | H or R | - |

## References

### PeptideCutter tool reference
Gasteiger E., Hoogland C., Gattiker A., Duvaud S., Wilkins M.R., Appel R.D., Bairoch A.;  
Protein Identification and Analysis Tools on the Expasy Server;  
(In) John M. Walker (ed): The Proteomics Protocols Handbook, Humana Press (2005).  
Full text - Copyright Humana Press.

### Protease references
Barrett A., Rawlings N.D., Woessner J.F.  
Handbook of proteolytic enzymes.  
Academic Press (1998).

Birktoft J.J., Breddam K.  
Glutamyl endopeptidases.  
Methods of Enzymology (1994) 244: 114-126. [PubMed](https://pubmed.ncbi.nlm.nih.gov/7845201/)

Bornstein P., Balian G.  
Cleavage at Asn-Gly bonds with hydroxylamine.  
Methods in Enzymology (1977) 47: 132-144.

Degani Y., Patchornik A.  
Cyanylation of sulfhydryl groups by 2-nitro-5-thiocyanobenzoic acid. High-yield modification and cleavage of peptides at cysteine residues.  
Biochemistry (1974) 13: 1-11. [PubMed](https://pubmed.ncbi.nlm.nih.gov/4808702/)

Earnshaw W.C., Martins L.M., Kaufmann S.H.  
Mammalian caspases: Structure, activation, substrates, and functions during apoptosis.  
Annual Review of Biochemistry (1999) 68: 383-424. [PubMed](https://pubmed.ncbi.nlm.nih.gov/10872455/)

Fulop V., Bocskei Z., Polgar L.  
Prolyl oligopeptidase: an unusual beta-propeller domain regulates proteolysis.  
Cell (1998) 94: 161-170. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9695945/)

Fujikawa K., Titani K., Davie E.W.  
Activation of bovine factor X (Stuart factor): conversion of factor Xa alpha to factor Xa beta.  
Proceedings of the National Academy of Science of the United States of America (1975) 72: 3359-3363. [PubMed](https://pubmed.ncbi.nlm.nih.gov/1059122/)

Houmard J., Drapeau G.R.  
Staphylococcal protease: a proteolytic enzyme specific for glutamoyl bonds.  
Proceedings of the National Academy of Science of the United States of America (1972) 69: 3506-3509. [PubMed](https://pubmed.ncbi.nlm.nih.gov/4509307/)

Han K.K., et al.  
Current developments in chemical cleavage of proteins.  
International Journal of Biochemistry (1983) 15(7): 875-884. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0020711X83901623?via%3Dihub)

Keil B.  
Protein and Nucleic Acid Enzymology (1986) 6: 11.

Keil B.  
Proteolysis Data Bank: specificity of alpha-chymotrypsin from computation of protein cleavages.  
Protein Sequence Data Analysis (1987) 1: 13-21. [PubMed](https://pubmed.ncbi.nlm.nih.gov/3447153/)

Keil B.  
Specificity of proteolysis.  
Springer-Verlag Berlin-Heidelberg-New York, pp. 335. (1992)

Keil B., Tong T.N.  
LYSIS.  
Springer-Verlag Berlin-Heidelberg-New York, diskette set. (1992)

Li A., et al.  
Chemical cleavage at aspartyl residues for protein identification.  
Anal Chem. (2001) 73: 5395-5402. [PubMed](https://pubmed.ncbi.nlm.nih.gov/11816565/)

Roche  
Enterokinase product description.  
http://www.roche-applied-science.com/proddata/gpip/3_1_3_7_10_1.html

Schechter I., Berger A.  
On the size of the active site in proteases. I. Papain.  
Biochemical and Biophysical Research Communication (1967) 27: 157. [PubMed](https://pubmed.ncbi.nlm.nih.gov/5682314/)

Schechter I., Berger A.  
On the active site of proteases. 3. Mapping the active site of papain; specific peptide inhibitors of papain.  
Biochemical and Biophysical Research Communication (1968) 32: 898. [PubMed](https://pubmed.ncbi.nlm.nih.gov/5682314/)

Schroeder W.A., Shelton J.B., Shelton J.R.  
An examination of conditions for the cleavage of polypeptide chains with cyanogen bromide: application to catalase.  
Archives of Biochemistry and Biophysics (1969) 130: 551-556. [PubMed](https://pubmed.ncbi.nlm.nih.gov/4892021/)

Stennicke H.R., Renatus M., Meldal M., Salvesen G.S.  
Internally quenched fluorescent peptide substrates disclose the subsite preferences of human caspases 1, 3, 6, 7 and 8.  
Biochem. J. (2000) 350: 563-568. [PubMed](https://pubmed.ncbi.nlm.nih.gov/10947972/)

Talanian R.V., Quinlan C., Trautz S., Hackett M.C., Mankovich J.A., Banach D., Ghayur T., Brady K.D., Wong W.W.  
Substrate specificities of caspase family proteases.  
Journal of Biological Chemistry (1997) 272: 9677-9682. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9092497/)

Thornberry N.A., Rano T.A., Peterson E.P., Rasper D.M., Timkey T., et al.  
A combinatorial approach defines specificities of members of the caspase family and Granzyme B.  
Journal of Biological Chemistry (1997) 272: 17907-17911. [PubMed](https://pubmed.ncbi.nlm.nih.gov/9218414/)

Kapust R.B., Tozser J., Copeland T.D., Waugh D.S.  
The P1' specificity of tobacco etch virus protease.  
Biochem Biophys Res Commun. (2002) 294: 949-955. [PubMed] [PubMed](https://pubmed.ncbi.nlm.nih.gov/12074568/)

Waugh D.S.  
TEV protease FAQ.  
http://mcl1.ncifcrf.gov/waugh_tech/faq/tev.pdf
