import gzip
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from Bio import SeqIO

@dataclass
class AnnotationFeature:
    """Standardized annotation feature data structure."""
    seq_id: str
    start: int
    end: int
    feature_type: str
    strand: Optional[int] # +1 for forward, -1 for reverse, None for unknown
    attributes: Dict[str, str] = field(default_factory=dict)
    id: Optional[str] = None

def _open_file(file_path: Path):
    """Open a file, handling .gz compression."""
    if file_path.suffix == ".gz":
        return gzip.open(file_path, "rt")
    return open(file_path, "r")

def parse_gff(gff_file: Path, target_seq_id: str) -> List[AnnotationFeature]:
    """Parses a GFF3 file and returns a list of AnnotationFeature objects."""
    features = []
    with _open_file(gff_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split('\t')
            if len(parts) != 9:
                continue
            if parts[0] != target_seq_id:
                continue

            attributes_str = parts[8]
            attributes = {
                k: v for k, v in [attr.split('=', 1) for attr in attributes_str.split(';') if '=' in attr]
            }
            
            strand_map = {'.': None, '?': None, '+': 1, '-': -1}

            features.append(AnnotationFeature(
                seq_id=parts[0],
                start=int(parts[3]),
                end=int(parts[4]),
                feature_type=parts[2],
                strand=strand_map.get(parts[6]),
                attributes=attributes,
                id=attributes.get("ID") or attributes.get("Name")
            ))
    return features

def parse_gbk(gbk_file: Path, target_seq_id: str) -> List[AnnotationFeature]:
    """Parses a GenBank file using BioPython."""
    features = []
    with _open_file(gbk_file) as f:
        for record in SeqIO.parse(f, "genbank"):
            # Match record ID, name, or accession against target ID from BLAST
            if not (record.id == target_seq_id or record.name == target_seq_id or target_seq_id in record.annotations.get('accessions', [])):
                continue

            for feature in record.features:
                qualifiers = {k: v[0] for k, v in feature.qualifiers.items() if v}
                
                # Take the first available identifier
                primary_id = (qualifiers.get("locus_tag") or 
                              qualifiers.get("gene") or 
                              qualifiers.get("protein_id"))

                features.append(AnnotationFeature(
                    seq_id=record.id,
                    start=int(feature.location.start) + 1, # Biopython is 0-based
                    end=int(feature.location.end),
                    feature_type=feature.type,
                    strand=feature.location.strand,
                    attributes=qualifiers,
                    id=primary_id
                ))
            break # Assume first matching record is the correct one
    return features

def parse_annotations(annotation_file: Path, target_seq_id: str) -> List[AnnotationFeature]:
    """Determines file type and calls the appropriate parser."""
    ext = annotation_file.suffix.lower()
    if ".gz" in annotation_file.suffixes:
        ext = annotation_file.suffixes[-2].lower() # e.g., .gff.gz -> .gff
        
    if ext in ['.gff', '.gff3']:
        return parse_gff(annotation_file, target_seq_id)
    elif ext in ['.gb', '.gbk', '.gbff', '.genbank']:
        return parse_gbk(annotation_file, target_seq_id)
    else:
        raise ValueError(f"Unsupported annotation file format: {ext}. Please use GFF3 or GenBank.")
