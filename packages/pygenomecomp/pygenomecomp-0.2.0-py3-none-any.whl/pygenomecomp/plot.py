import math
import svgwrite
from pathlib import Path
from typing import List, Optional, Dict
import colorsys
from .annotation import AnnotationFeature

# --- Constants for visual layout ---
SVG_WIDTH, SVG_HEIGHT = 1200, 1000  # Increased width for legend
CENTER_X, CENTER_Y = 500, 500       # Center of the circular plot
REFERENCE_RING_RADIUS = 200.0
ANNOTATION_RING_RADIUS_OUTER = REFERENCE_RING_RADIUS - 5.0
ANNOTATION_RING_THICKNESS = 15.0
ANNOTATION_RING_RADIUS_INNER = ANNOTATION_RING_RADIUS_OUTER - ANNOTATION_RING_THICKNESS
BLAST_HIT_BASE_RADIUS = REFERENCE_RING_RADIUS + 10.0
BLAST_RING_THICKNESS = 18.0
BLAST_RING_SPACING = 8.0

def get_query_base_color(query_index, n_queries):
    """Assigns a unique base color (hue) to each query."""
    hue = (query_index / max(1, n_queries)) % 1.0  # [0,1)
    return hue

def get_blast_hit_color(query_index, n_queries, identity):
    """
    Returns a color for a BLAST hit:
      - Unique hue per query,
      - Light (low identity) to dark (high identity) within that hue.
    """
    hue = get_query_base_color(query_index, n_queries)
    s = 0.85  # Keep saturation high for colorfulness
    # Value goes from 1.0 (light) at 70% identity to 0.45 (dark) at 100% identity
    min_identity = 70
    max_identity = 100
    min_value = 0.45
    max_value = 1.0
    # Cap identity within the range
    identity = max(min_identity, min(max_identity, identity))
    # Invert: lower identity = lighter, higher identity = darker
    value = max_value - ((identity - min_identity) / (max_identity - min_identity)) * (max_value - min_value)
    r, g, b = colorsys.hsv_to_rgb(hue, s, value)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def get_annotation_feature_color(feature_type: str) -> str:
    """Maps annotation feature type to a specific color."""
    ft_lower = feature_type.lower()
    if ft_lower == "cds": return "#4682B4"      # SteelBlue
    if ft_lower == "gene": return "#3CB371"     # MediumSeaGreen
    if ft_lower == "trna": return "#FF6347"     # Tomato
    if ft_lower == "rrna": return "#EE82EE"     # Violet
    return "#808080"  # Gray for other types

def draw_arc_segment(dwg, center_x, center_y, r_inner, r_outer, start_rad, end_rad, color, opacity=1.0):
    """Draws a filled arc segment, the core visual element for all features."""
    large_arc_flag = 1 if abs(end_rad - start_rad) > math.pi else 0

    # Outer arc start and end points
    x_start_outer = center_x + r_outer * math.cos(start_rad)
    y_start_outer = center_y + r_outer * math.sin(start_rad)
    x_end_outer = center_x + r_outer * math.cos(end_rad)
    y_end_outer = center_y + r_outer * math.sin(end_rad)

    # Inner arc start and end points
    x_start_inner = center_x + r_inner * math.cos(start_rad)
    y_start_inner = center_y + r_inner * math.sin(start_rad)
    x_end_inner = center_x + r_inner * math.cos(end_rad)
    y_end_inner = center_y + r_inner * math.sin(end_rad)

    path_data = (
        f"M {x_start_outer} {y_start_outer} "
        f"A {r_outer} {r_outer} 0 {large_arc_flag} 1 {x_end_outer} {y_end_outer} "
        f"L {x_end_inner} {y_end_inner} "
        f"A {r_inner} {r_inner} 0 {large_arc_flag} 0 {x_start_inner} {y_start_inner} Z"
    )
    dwg.add(dwg.path(d=path_data, fill=color, stroke='grey', stroke_width=0.2, opacity=opacity))

def generate_plot(blast_hits: List[Dict], annotations: Optional[List[AnnotationFeature]],
                  reference_length: int, query_names: List[str], output_path: Path,
                  reference_display_name: str,
                  show_gene_names: bool = False):  # <-- Add new parameter with default):
    """
    Generates the final SVG plot, including a detailed legend.

    Args:
        blast_hits: List of BLAST hit dictionaries.
        annotations: List of AnnotationFeature objects.
        reference_length: The total length of the reference sequence.
        query_names: A list of query filenames for the legend.
        output_path: The path to save the output SVG file.
        reference_display_name: The name of the reference sequence for display.
    """
    if reference_length == 0:
        raise ValueError("Reference length cannot be zero.")

    dwg = svgwrite.Drawing(str(output_path), size=(f"{SVG_WIDTH}px", f"{SVG_HEIGHT}px"), profile='full')
    dwg.add(dwg.style("text { font-family: Arial, sans-serif; }"))

    # --- Draw Reference Ring and Scale Ticks ---
    dwg.add(dwg.circle(center=(CENTER_X, CENTER_Y), r=REFERENCE_RING_RADIUS, fill='none', stroke='#333333', stroke_width=1.5))
    dwg.add(dwg.text(f"Ref: {reference_display_name} ({reference_length:,} bp)", insert=(CENTER_X, CENTER_Y), text_anchor='middle', alignment_baseline='middle', font_size='14px', fill='#333'))

    num_major_ticks = 12
    for i in range(num_major_ticks):
        angle_rad = (i / num_major_ticks) * 2 * math.pi - math.pi / 2
        pos_bp = (i / num_major_ticks) * reference_length
        label = f"{pos_bp/1e6:.1f}Mb" if reference_length > 2e6 else f"{pos_bp/1e3:.0f}kb"
        tick_len = 10.0
        x1 = CENTER_X + REFERENCE_RING_RADIUS * math.cos(angle_rad)
        y1 = CENTER_Y + REFERENCE_RING_RADIUS * math.sin(angle_rad)
        x2 = CENTER_X + (REFERENCE_RING_RADIUS + tick_len) * math.cos(angle_rad)
        y2 = CENTER_Y + (REFERENCE_RING_RADIUS + tick_len) * math.sin(angle_rad)
        dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke='darkgrey', stroke_width=0.75))
        x_text = CENTER_X + (REFERENCE_RING_RADIUS + tick_len + 15) * math.cos(angle_rad)
        y_text = CENTER_Y + (REFERENCE_RING_RADIUS + tick_len + 15) * math.sin(angle_rad)
        dwg.add(dwg.text(label, insert=(x_text, y_text), text_anchor='middle', alignment_baseline='middle', font_size='10px'))

    # --- Draw Annotation Ring ---
    if annotations:
        for feature in annotations:
            map_start, map_end = feature.start - 1, feature.end
            start_rad = (map_start / reference_length) * 2 * math.pi - math.pi / 2
            end_rad = (map_end / reference_length) * 2 * math.pi - math.pi / 2
            if abs(end_rad - start_rad) < 1e-6:
                continue
            color = get_annotation_feature_color(feature.feature_type)
            draw_arc_segment(
                dwg, CENTER_X, CENTER_Y,
                ANNOTATION_RING_RADIUS_INNER, ANNOTATION_RING_RADIUS_OUTER,
                start_rad, end_rad, color, opacity=0.85
            )
            # --- Draw gene name if enabled and type is gene ---
            if show_gene_names and feature.feature_type.lower() == "gene":
                mid_rad = (start_rad + end_rad) / 2
                # Place label further outside the annotation ring for visibility
                label_radius = ANNOTATION_RING_RADIUS_OUTER - 30  # Offset label inwards
                x = CENTER_X + label_radius * math.cos(mid_rad)
                y = CENTER_Y + label_radius * math.sin(mid_rad)
                gene_name = (
                    feature.attributes.get("Name") or feature.id or feature.attributes.get("gene") or ""
                )
                if gene_name and abs(end_rad - start_rad) > 0.12:  # Only show for longer arcs
                    dwg.add(dwg.text(
                        gene_name,
                        insert=(x, y),
                        font_size="9px",
                        text_anchor="middle",
                        alignment_baseline="middle",
                        fill="#222",
                        stroke="red",
                        stroke_width=0.8,
                        #paint_order="stroke fill",
                        style="pointer-events:none",
                    ))

    # --- Draw BLAST Hit Rings ---
    for hit in blast_hits:
        outer_r = BLAST_HIT_BASE_RADIUS + (hit['query_index'] * (BLAST_RING_THICKNESS + BLAST_RING_SPACING)) + BLAST_RING_THICKNESS
        inner_r = outer_r - BLAST_RING_THICKNESS

        s_start, s_end = min(hit['sstart'], hit['send']), max(hit['sstart'], hit['send'])
        start_rad = ((s_start - 1) / reference_length) * 2 * math.pi - math.pi / 2
        end_rad = ((s_end - 1) / reference_length) * 2 * math.pi - math.pi / 2
        if abs(end_rad - start_rad) < 1e-6: continue

        color = get_blast_hit_color(hit['query_index'], len(query_names), hit['pident'])
        draw_arc_segment(dwg, CENTER_X, CENTER_Y, inner_r, outer_r, start_rad, end_rad, color, opacity=0.9)

    # =========================================================================
    # --- COMPLETE LEGEND IMPLEMENTATION ---
    # =========================================================================
    legend_x = SVG_WIDTH - 180
    legend_y = 50
    box_size = 12
    item_height = 20

    # --- Query base color legend ---
    dwg.add(dwg.text("Queries (Outer Rings)", insert=(legend_x, legend_y), font_weight='bold', font_size='12px'))
    legend_y += item_height
    for i, name in enumerate(query_names):
        # Base color for this query (at mid identity for visibility)
        base_color = get_blast_hit_color(i, len(query_names), 85)
        dwg.add(dwg.rect(insert=(legend_x + 5, legend_y), size=(box_size, box_size), fill=base_color))
        dwg.add(dwg.text(f"Ring {i+1}: {name}", insert=(legend_x + 25, legend_y + box_size), font_size='11px'))
        legend_y += item_height
    legend_y += item_height * 0.5

    # --- Per-query identity gradient legend ---
    dwg.add(dwg.text("Identity gradient (per query)", insert=(legend_x, legend_y), font_weight='bold', font_size='12px'))
    legend_y += item_height
    gradient_width = 75
    gradient_height = 12
    for i, name in enumerate(query_names):
        grad_id = f"identgrad_query{i}"
        gradient = dwg.linearGradient(start=(0, 0), end=(1, 0), id=grad_id)
        # From light (70%) to dark (100%)
        for frac, ident in zip([0, 0.33, 0.66, 1], [70, 85, 95, 100]):
            color = get_blast_hit_color(i, len(query_names), ident)
            gradient.add_stop_color(offset=frac, color=color)
        dwg.defs.add(gradient)
        # Draw the gradient bar
        dwg.add(dwg.rect(insert=(legend_x + 5, legend_y), size=(gradient_width, gradient_height), fill=f"url(#{grad_id})"))
        # Add label
        dwg.add(dwg.text(f"{name}", insert=(legend_x + 5 + gradient_width + 10, legend_y + gradient_height),
                         font_size='10px', alignment_baseline='middle'))
        legend_y += gradient_height + 6
    # Add percentage labels below the gradient
    dwg.add(dwg.text("70%", insert=(legend_x + 5, legend_y), font_size='9px'))
    dwg.add(dwg.text("100%", insert=(legend_x + 5 + gradient_width - 20, legend_y), font_size='9px'))
    legend_y += item_height

    # --- Annotation Legend ---
    dwg.add(dwg.text("Annotations (Inner Ring)", insert=(legend_x, legend_y), font_weight='bold', font_size='12px'))
    legend_y += item_height
    annotation_types = [("CDS", get_annotation_feature_color("cds")),
                        ("gene", get_annotation_feature_color("gene")),
                        ("tRNA", get_annotation_feature_color("trna")),
                        ("rRNA", get_annotation_feature_color("rrna"))]
    for label, color in annotation_types:
        dwg.add(dwg.rect(insert=(legend_x + 5, legend_y), size=(box_size, box_size), fill=color))
        dwg.add(dwg.text(label, insert=(legend_x + 25, legend_y + box_size), font_size='11px'))
        legend_y += item_height
    legend_y += item_height * 0.5 # Spacer

    # --- (Optional) Any other legend items can follow here ---

    dwg.save(pretty=True)
