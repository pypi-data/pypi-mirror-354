import argparse
import sys
from pathlib import Path
from pygenomecomp import blast, annotation, plot

def main():
    """Main function to run the genome comparison tool."""
    parser = argparse.ArgumentParser(
        description="Genome Assembly Comparison Tool with Annotation Ring.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-r", "--reference", type=Path, required=True,
        help="Reference genome assembly in FASTA format."
    )
    parser.add_argument(
        "-q", "--queries", type=Path, required=True, nargs='+',
        help="One or more query genome assemblies in FASTA format."
    )
    parser.add_argument(
        "--annotations", type=Path,
        help="Optional: Reference genome annotation file (GFF3 or GBFF/GenBank format)."
    )
    parser.add_argument(
        "-o", "--output_dir", type=Path, default="genome_comp_output",
        help="Output directory for BLAST results and plot."
    )
    parser.add_argument(
        "--plot_file", type=str, default="comparison_plot.svg",
        help="Output SVG plot file name."
    )
    parser.add_argument(
        "--min_identity", type=float, default=70.0,
        help="Minimum BLAST percentage identity."
    )
    parser.add_argument(
        "--min_length", type=int, default=100,
        help="Minimum BLAST alignment length."
    )
    parser.add_argument(
        "--evalue", type=float, default=1e-5,
        help="BLAST e-value cutoff."
    )
    parser.add_argument(
        "--show_gene_names",
        action="store_true",
        help="Show gene names as text labels on the annotation ring of the plot."
    )
    args = parser.parse_args()

    # --- 1. Validate inputs and create output directory ---
    if not args.reference.exists():
        print(f"Error: Reference genome file not found: {args.reference}", file=sys.stderr)
        sys.exit(1)
    for query_file in args.queries:
        if not query_file.exists():
            print(f"Error: Query genome file not found: {query_file}", file=sys.stderr)
            sys.exit(1)
    if args.annotations and not args.annotations.exists():
        print(f"Error: Annotation file not found: {args.annotations}", file=sys.stderr)
        sys.exit(1)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {args.output_dir.resolve()}")
    except OSError as e:
        print(f"Error: Could not create output directory {args.output_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    # --- 2. Prepare BLAST database for the reference genome ---
    print(f"Preparing BLAST database for reference: {args.reference}")
    db_prefix = args.output_dir / args.reference.stem
    try:
        blast.make_blast_db(args.reference, db_prefix)
        print(f"BLAST database created with prefix: {db_prefix}")
    except RuntimeError as e:
        print(f"Error creating BLAST database: {e}", file=sys.stderr)
        sys.exit(1)

    # --- 3. Run BLAST for each query genome ---
    all_blast_hits = []
    primary_reference_seq_id = None
    reference_length = None

    for i, query_file in enumerate(args.queries):
        print(f"Running BLAST for query: {query_file}")
        blast_output_file = args.output_dir / f"{query_file.stem}_vs_{args.reference.stem}.blast.tsv"
        try:
            blast.run_blastn(query_file, db_prefix, blast_output_file, args.evalue, args.min_identity)
            print(f"BLAST output for {query_file.name} saved to: {blast_output_file}")
            
            hits = blast.parse_blast_output(blast_output_file, args.min_identity, args.min_length)
            print(f"Parsed {len(hits)} significant hits for {query_file.name}")

            for hit in hits:
                hit['query_index'] = i # Add query index for plotting
                all_blast_hits.append(hit)
                if primary_reference_seq_id is None:
                    primary_reference_seq_id = hit['sseqid']
                if reference_length is None and 'slen' in hit and hit['slen']:
                    reference_length = int(hit['slen'])

        except (RuntimeError, FileNotFoundError) as e:
            print(f"Error running or parsing BLAST for query {query_file}: {e}", file=sys.stderr)
            continue
    
    # --- 4. Parse Annotations ---
    parsed_annotations = None
    if args.annotations:
        if primary_reference_seq_id:
            print(f"Parsing annotations from {args.annotations} for reference ID: {primary_reference_seq_id}")
            try:
                parsed_annotations = annotation.parse_annotations(args.annotations, primary_reference_seq_id)
                print(f"Successfully parsed {len(parsed_annotations)} annotation features.")
            except Exception as e:
                print(f"Warning: Could not parse annotation file {args.annotations}: {e}. Plot will be generated without annotations.", file=sys.stderr)
        else:
            print("Warning: Annotation file provided, but no reference sequence ID could be determined from BLAST. Annotations will not be plotted.", file=sys.stderr)
    
    # --- 5. Generate Plot ---
    if not all_blast_hits and not parsed_annotations:
        print("No BLAST hits or annotations found to plot.")
    else:
        plot_path = args.output_dir / args.plot_file
        print(f"Generating plot: {plot_path}")
        
        if reference_length is None:
            # Attempt to get length from reference fasta if BLAST failed to provide it
            try:
                from Bio import SeqIO
                with open(args.reference, "r") as handle:
                    first_record = next(SeqIO.parse(handle, "fasta"))
                    reference_length = len(first_record.seq)
                    if primary_reference_seq_id is None:
                        primary_reference_seq_id = first_record.id
                    print(f"Determined reference length from FASTA file: {reference_length} bp")
            except (ImportError, StopIteration, FileNotFoundError) as e:
                 print(f"Warning: Could not determine reference length from BLAST 'slen' field or by reading FASTA file ({e}). Plot may be inaccurate.", file=sys.stderr)
                 reference_length = 1_000_000 # Fallback default
        
        ref_display_name = primary_reference_seq_id or args.reference.name

        # *** KEY CHANGE IS HERE ***
        # Create a list of query names from the Path objects
        query_names_list = [q.name for q in args.queries]

        try:
            # Call the plot function with the new 'query_names' argument
            plot.generate_plot(
                blast_hits=all_blast_hits,
                annotations=parsed_annotations,
                reference_length=reference_length,
                query_names=query_names_list, # Pass the list of names
                output_path=plot_path,
                reference_display_name=ref_display_name,
                show_gene_names=args.show_gene_names,  # <-- Pass the new option
            )
            print(f"Plot generated successfully: {plot_path}")
        except Exception as e:
            print(f"Error generating plot: {e}", file=sys.stderr)
            sys.exit(1)

    print("Processing complete.")
    sys.exit(0)

if __name__ == '__main__':
    main()
