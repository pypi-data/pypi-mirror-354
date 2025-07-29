import subprocess
import shutil
import pandas as pd
from pathlib import Path

def _run_command(cmd):
    """Run an external command and handle errors."""
    if not shutil.which(cmd[0]):
        raise FileNotFoundError(
            f"Command '{cmd[0]}' not found. Please ensure BLAST+ is installed and in your PATH."
        )
    process = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if process.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {process.returncode}:\n"
            f"Command: {' '.join(map(str, cmd))}\n"
            f"Stderr: {process.stderr}"
        )
    return process

def make_blast_db(reference_fasta: Path, db_prefix: Path):
    """Creates a BLAST database from a reference FASTA file."""
    cmd = [
        "makeblastdb",
        "-in", str(reference_fasta),
        "-dbtype", "nucl",
        "-out", str(db_prefix),
        "-parse_seqids"
    ]
    _run_command(cmd)

def run_blastn(query_fasta: Path, db_prefix: Path, output_file: Path, evalue: float, min_identity: float):
    """Runs blastn and saves the output in tabular format."""
    outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen"
    cmd = [
        "blastn",
        "-query", str(query_fasta),
        "-db", str(db_prefix),
        "-out", str(output_file),
        "-outfmt", outfmt,
        "-evalue", str(evalue),
        "-perc_identity", str(min_identity)
    ]
    _run_command(cmd)

def parse_blast_output(blast_output_file: Path, min_identity: float, min_length: int) -> list[dict]:
    """Parses BLAST tabular output into a list of dictionaries using pandas."""
    col_names = [
        "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", 
        "qstart", "qend", "sstart", "send", "evalue", "bitscore", "qlen", "slen"
    ]
    try:
        df = pd.read_csv(blast_output_file, sep='\t', header=None, names=col_names)
        
        # Filter based on identity and length
        filtered_df = df[(df['pident'] >= min_identity) & (df['length'] >= min_length)]
        
        # Convert to a list of dictionaries for easier processing
        return filtered_df.to_dict('records')
    except pd.errors.EmptyDataError:
        return [] # Return empty list if blast output is empty
    except Exception as e:
        raise RuntimeError(f"Failed to parse BLAST output file {blast_output_file}: {e}")
