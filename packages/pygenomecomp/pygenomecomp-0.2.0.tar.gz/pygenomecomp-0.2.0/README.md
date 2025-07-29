# PyGenomeComp

[![PyPI version](https://badge.fury.io/py/pygenomecomp.svg)](https://badge.fury.io/py/pygenomecomp)

A Python command-line tool to visualize whole-genome comparisons. `pygenomecomp` aligns one or more query genomes against a reference genome and generates a circular plot showing sequence identity, with an optional track for reference genome annotations.

### Key Features

* Aligns multiple query genomes to a reference using BLAST+.
* Parses GFF3 and GenBank files to display reference annotations.
* Generates a clear, publication-quality SVG circular plot.
* Customizable alignment filters (min. identity, min. length, e-value).
* **NEW:** Optionally display gene names as text labels on the plot.

---

## Installation

*Install instructions here...*

---

## Usage

Create the following four files in a new directory:

`reference.fasta`
```
>ref_contig_1
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAAC
```
`query1.fasta`
```
>query_A
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAAT
```
`query2.fasta`
```
>query_B
TAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAAC
```
`query3.fasta`
```
>query_C
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAAC
```
`annotations.gff3`
```
##gff-version 3
ref_contig_1	Prokka	gene	350	450	.	+	.	ID=gene01;Name=ABC_transporter
ref_contig_1	Prokka	CDS	350	450	.	+	0	ID=cds01;Parent=gene01;product=ATP-binding cassette transporter
ref_contig_1	Prokka	rRNA	120	220	.	-	.	ID=rrna01;product=16S ribosomal RNA
```

##### 2. Run the Tool
Open your terminal in the directory containing these files and run the following command:
```
pygenomecomp \
  --reference reference.fasta \
  --queries query1.fasta query2.fasta query3.fasta \
  --annotations annotations.gff3 \
  --output_dir my_comparison_results
```

##### 3. Show gene names on the plot (optional)
To display gene names as text labels on the annotation ring of the plot, add the `--show_gene_names` option:
```
pygenomecomp \
  --reference reference.fasta \
  --queries query1.fasta query2.fasta query3.fasta \
  --annotations annotations.gff3 \
  --output_dir my_comparison_results \
  --show_gene_names
```

##### 4. Check the Output
A new directory named `my_comparison_results` will be created. Inside, you will find:

- Intermediate BLAST database and result files.
- The final visualization: `comparison_plot.svg`.

Open `comparison_plot.svg` in a web browser or vector graphics editor. It will show a central reference ring with annotation features, and two or more outer rings corresponding to the query sequences, with arcs colored by sequence identity.

If `--show_gene_names` is set, gene names from the annotation file will be rendered as labels near their corresponding arcs.

---

#### Command-Line Usage

```
$ pygenomecomp --help
usage: pygenomecomp [-h] -r REFERENCE -q QUERIES [QUERIES ...]
                    [--annotations ANNOTATIONS] [-o OUTPUT_DIR]
                    [--plot_file PLOT_FILE] [--min_identity MIN_IDENTITY]
                    [--min_length MIN_LENGTH] [--evalue EVALUE]
                    [--show_gene_names]

Genome Assembly Comparison Tool with Annotation Ring.

options:
  -h, --help            show this help message and exit
  -r REFERENCE, --reference REFERENCE
                        Reference genome assembly in FASTA format.
  -q QUERIES [QUERIES ...], --queries QUERIES [QUERIES ...]
                        One or more query genome assemblies in FASTA format.
  --annotations ANNOTATIONS
                        Optional: Reference genome annotation file (GFF3 or
                        GBFF/GenBank format).
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory for BLAST results and plot.
  --plot_file PLOT_FILE
                        Output SVG plot file name.
  --min_identity MIN_IDENTITY
                        Minimum BLAST percentage identity.
  --min_length MIN_LENGTH
                        Minimum BLAST alignment length.
  --evalue EVALUE       BLAST e-value cutoff.
  --show_gene_names     Show gene names as text labels on the plot annotation ring.
```

#### License
This project is licensed under the MIT License
