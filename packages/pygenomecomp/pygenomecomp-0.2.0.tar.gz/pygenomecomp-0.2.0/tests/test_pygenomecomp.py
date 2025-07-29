import subprocess
import tempfile
#import shutil
import os

REFERENCE_FASTA = """>ref_contig_1
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAAC
"""
QUERY1_FASTA = """>query_A
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTGGTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGACAGATAAAAATTACAGAGTACACAACATCCATGAAAC
"""
QUERY2_FASTA = """>query_B_reversed
CCTGTACACCAGCACGGTTTGTTTGGGCAAATTCCTGATCGACGAAAGTTTTCAATTGCGCCAGCGGGAACCCCGGCTGGGCGGCGGCGAGTCCCGTCAAAAGTTCGGCAAAAATACGTTCGGCATCGCTGATATTGGGTAAAGCATCCTGGCCGCTAATGGTTTTTTCAATCATCGCCACCAGGTGGTTGGTGAT
"""
ANNOTATIONS_GFF3 = """##gff-version 3
ref_contig_1	Prokka	gene	350	450	.	+	.	ID=gene01;Name=ABC_transporter
ref_contig_1	Prokka	CDS	350	450	.	+	0	ID=cds01;Parent=gene01;product=ATP-binding cassette transporter
ref_contig_1	Prokka	rRNA	120	220	.	-	.	ID=rrna01;product=16S ribosomal RNA
"""

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def test_minimal_working_example():
    with tempfile.TemporaryDirectory() as tmpdir:
        ref = os.path.join(tmpdir, "reference.fasta")
        q1 = os.path.join(tmpdir, "query1.fasta")
        q2 = os.path.join(tmpdir, "query2.fasta")
        ann = os.path.join(tmpdir, "annotations.gff3")
        outdir = os.path.join(tmpdir, "my_comparison_results")

        write_file(ref, REFERENCE_FASTA)
        write_file(q1, QUERY1_FASTA)
        write_file(q2, QUERY2_FASTA)
        write_file(ann, ANNOTATIONS_GFF3)

        # Run the CLI
        result = subprocess.run([
            "pygenomecomp",
            "--reference", ref,
            "--queries", q1, q2,
            "--annotations", ann,
            "--output_dir", outdir
        ], capture_output=True, text=True)

        # For debugging on CI
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        assert result.returncode == 0, f"pygenomecomp failed: {result.stderr}"

        # Check output directory and expected SVG
        plot_path = os.path.join(outdir, "comparison_plot.svg")
        assert os.path.isdir(outdir), "Output directory was not created"
        assert os.path.isfile(plot_path), "SVG plot was not generated"

        # Optionally, check that the SVG file is not empty/minimal
        with open(plot_path) as f:
            svg = f.read()
            assert "<svg" in svg, "SVG output does not contain <svg> tag"

# If you want to run with pytest, add this at the end:
if __name__ == "__main__":
    import pytest
    pytest.main([__file__])