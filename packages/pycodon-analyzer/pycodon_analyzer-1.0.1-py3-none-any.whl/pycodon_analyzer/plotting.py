# src/pycodon_analyzer/plotting.py
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Gabriel Falque
# Distributed under the terms of the MIT License.
# (See accompanying file LICENSE or copy at https://opensource.org/license/mit/)

"""
Functions for generating plots related to codon usage and sequence properties.
Uses Matplotlib and Seaborn for plotting.
"""
from pathlib import Path
import re
import os
import sys
import logging # <-- Import logging
import traceback # Keep for detailed error logging if needed via logger.exception
from typing import List, Dict, Optional, Any, Tuple, Set, Union, TYPE_CHECKING


# Third-party library imports with error handling for optional ones
try:
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes # For type hinting
    from matplotlib.figure import Figure # For type hinting
    from matplotlib.collections import PathCollection # For type hinting scatter plot object
    from matplotlib.text import Text as MatplotlibText # For type hinting plt.Text
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    # Critical dependency, log and exit might be too late if logger not set.
    print("CRITICAL ERROR: matplotlib is required but not installed. Please install it (`pip install matplotlib`).", file=sys.stderr)
    MATPLOTLIB_AVAILABLE = False
    sys.exit(1)

try:
    import seaborn as sns
    SNS_AVAILABLE = True
except ImportError:
    print("CRITICAL ERROR: seaborn is required but not installed. Please install it (`pip install seaborn`).", file=sys.stderr)
    SNS_AVAILABLE = False
    sys.exit(1)

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    print("CRITICAL ERROR: pandas is required but not installed. Please install it (`pip install pandas`).", file=sys.stderr)
    PANDAS_AVAILABLE = False
    sys.exit(1)

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    print("CRITICAL ERROR: numpy is required but not installed. Please install it (`pip install numpy`).", file=sys.stderr)
    NUMPY_AVAILABLE = False
    sys.exit(1)

if TYPE_CHECKING:
    from scipy import stats as scipy_stats_module # For type checking if used
    SCIPY_AVAILABLE = True
    # ScipyStatsModule = type(scipy.stats) # More precise if needed
else:
    try:
        from scipy import stats as scipy_stats_module
        SCIPY_AVAILABLE = True
    except ImportError:
        SCIPY_AVAILABLE = False
        scipy_stats_module = None # Runtime check

if TYPE_CHECKING:
    import prince
    PrinceCA = prince.CA
    from scipy import stats as scipy_stats_module # For type hints
    PRINCE_AVAILABLE = True
else:
    PrinceCA = Any
    try:
        import prince
        PRINCE_AVAILABLE = True
    except ImportError:
        PRINCE_AVAILABLE = False
        prince = None
    try:
        from scipy import stats as scipy_stats_module
    except ImportError:
        scipy_stats_module = None

# Import adjustText and set ADJUSTTEXT_AVAILABLE
try:
    from adjustText import adjust_text
    ADJUSTTEXT_AVAILABLE = True
except ImportError:
    ADJUSTTEXT_AVAILABLE = False

# --- Configure logging for this module ---
# Gets the logger instance configured in cli.py (or root logger if run standalone)
logger = logging.getLogger(__name__)

from . import utils as plot_utils # Assuming sanitize_filename is in utils

# Set default seaborn theme (optional, place where it's guaranteed to run once)
try:
    sns.set_theme(style="ticks", palette="deep")
except Exception as e:
    logger.warning(f"Could not set default seaborn theme: {e}")


# --- AA Code Mapping (Unchanged) ---
AA_1_TO_3: Dict[str, str] = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'Q': 'Gln', 'E': 'Glu', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
}
AA_3_TO_1: Dict[str, str] = {v: k for k, v in AA_1_TO_3.items()}
AA_ORDER: List[str] = sorted(AA_1_TO_3.keys())

# === Aggregate Plots ===

def plot_rscu(rscu_df: pd.DataFrame,
              output_filepath: str) -> None:
    """
    Generates a bar plot of aggregate Relative Synonymous Codon Usage (RSCU) values,
    grouped by amino acid.

    Args:
        rscu_df (pd.DataFrame): DataFrame containing RSCU values. Must include
                                'AminoAcid', 'Codon', and 'RSCU' columns.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/rscu_plot.svg').
    """
    required_cols = ['AminoAcid', 'Codon', 'RSCU']
    if rscu_df is None or rscu_df.empty or not all(col in rscu_df.columns for col in required_cols):
        logger.warning("Cannot plot RSCU. DataFrame is missing, empty, or lacks required columns (AminoAcid, Codon, RSCU).")
        return

    fig: Optional[Figure] = None # Initialize fig object for finally block
    try:
        # Filter out NaN RSCU values and sort for consistent plotting
        rscu_df_plot = rscu_df.dropna(subset=['RSCU', 'AminoAcid']).copy()
        # Ensure Codon and AA are suitable for plotting
        rscu_df_plot['Codon'] = rscu_df_plot['Codon'].astype(str)
        rscu_df_plot['AminoAcid'] = rscu_df_plot['AminoAcid'].astype(str)
        # Ensure RSCU is numeric
        rscu_df_plot['RSCU'] = pd.to_numeric(rscu_df_plot['RSCU'], errors='coerce')
        rscu_df_plot.dropna(subset=['RSCU'], inplace=True) # Drop if conversion failed

        rscu_df_plot.sort_values(by=['AminoAcid', 'Codon'], inplace=True)

        if rscu_df_plot.empty:
            logger.warning("No non-NaN RSCU data available to plot after filtering.")
            return

        fig, ax = plt.subplots(figsize=(18, 7)) # Create figure and axes

        # Use seaborn barplot
        sns.barplot(x='Codon', y='RSCU', hue='AminoAcid',
                    data=rscu_df_plot,
                    dodge=False, # Ensure bars for different amino acids are not dodged (side-by-side)
                    palette='tab20', ax=ax)

        ax.set_title('Relative Synonymous Codon Usage (RSCU)', fontsize=16)
        ax.set_xlabel('Codon', fontsize=12)
        ax.set_ylabel('RSCU Value', fontsize=12)
        ax.tick_params(axis='x', rotation=90, labelsize=8)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Improve legend
        try:
            ax.legend(title='Amino Acid', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
            # Adjust layout to make space for the legend outside the plot area
            plt.tight_layout(rect=[0, 0, 0.9, 1])
        except Exception as legend_err:
            logger.warning(f"Could not optimally place RSCU plot legend: {legend_err}. Using default layout.")
            plt.tight_layout()

        # Save the plot
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"RSCU plot saved to: {output_path_obj}")

    except (ValueError, TypeError) as data_err:
        logger.error(f"Data error during RSCU plot generation (check data types/values): {data_err}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during RSCU plot generation: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_codon_frequency(rscu_df: pd.DataFrame,
                         output_filepath: str) -> None:
    """
    Generates a bar plot of aggregate codon frequencies.

    Args:
        rscu_df (pd.DataFrame): DataFrame containing codon frequency values. Must include
                                'Codon' and 'Frequency' columns.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/codon_frequency.svg').
    """
    required_cols = ['Codon', 'Frequency']
    if rscu_df is None or rscu_df.empty or not all(col in rscu_df.columns for col in required_cols):
        logger.warning("Cannot plot Codon Frequency. DataFrame is missing, empty, or lacks required columns (Codon, Frequency).")
        return

    fig: Optional[Figure] = None
    try:
        # Prepare data for plotting
        freq_df_plot = rscu_df[['Codon', 'Frequency']].dropna().copy()
        freq_df_plot['Codon'] = freq_df_plot['Codon'].astype(str)
        freq_df_plot['Frequency'] = pd.to_numeric(freq_df_plot['Frequency'], errors='coerce')
        freq_df_plot.dropna(subset=['Frequency'], inplace=True)
        freq_df_plot.sort_values(by='Codon', inplace=True)

        if freq_df_plot.empty:
            logger.warning("No valid Codon Frequency data available to plot after filtering.")
            return

        fig, ax = plt.subplots(figsize=(16, 6))
        sns.barplot(x='Codon', y='Frequency', data=freq_df_plot, color='skyblue', ax=ax)

        ax.set_title('Codon Frequency', fontsize=16)
        ax.set_xlabel('Codon', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.tick_params(axis='x', rotation=90, labelsize=8)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save the plot
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Codon frequency plot saved to: {output_path_obj}")

    except (ValueError, TypeError) as data_err:
        logger.error(f"Error preparing data or plotting Codon Frequency: {data_err}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during Codon Frequency plot generation: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_dinucleotide_freq(dinucl_freqs: Dict[str, float],
                           output_filepath: str) -> None:
    """
    Plots relative dinucleotide frequencies as a bar chart.

    Args:
        dinucl_freqs (Dict[str, float]): Dictionary where keys are dinucleotide strings
                                        (e.g., 'AA', 'AT') and values are their
                                        corresponding frequencies.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/dinucleotide_frequency.svg').
    """
    if not dinucl_freqs:
        logger.warning("No dinucleotide frequency data provided to plot.")
        return

    fig: Optional[Figure] = None
    try:
        # Convert dict to DataFrame
        freq_df = pd.DataFrame.from_dict(dinucl_freqs, orient='index', columns=['Frequency'])
        freq_df['Frequency'] = pd.to_numeric(freq_df['Frequency'], errors='coerce')
        freq_df.dropna(inplace=True)
        freq_df.sort_index(inplace=True)

    except (ValueError, TypeError) as df_err:
         logger.error(f"Error creating DataFrame for dinucleotide plot: {df_err}")
         return

    if freq_df.empty:
        logger.warning("Dinucleotide frequency data is empty or all NaN after conversion.")
        return

    try:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=freq_df.index, y=freq_df['Frequency'], palette='coolwarm', ax=ax)

        ax.set_title('Relative Dinucleotide Frequencies')
        ax.set_xlabel('Dinucleotide')
        ax.set_ylabel('Frequency')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Dinucleotide frequency plot saved to: {output_path_obj}")

    except Exception as e:
         logger.exception(f"Error during seaborn barplot generation for Dinucleotides: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_gc_means_barplot(per_sequence_df: pd.DataFrame,
                          output_filepath: str,
                          group_by: str = 'Gene') -> None:
    """
    Plots a grouped bar chart of mean GC%, GC1-3%, and GC12 values,
    aggregated by a specified grouping column (e.g., 'Gene').

    Args:
        per_sequence_df (pd.DataFrame): DataFrame containing per-sequence metrics.
                                        Must include 'GC', 'GC1', 'GC2', 'GC3', 'GC12'
                                        and the `group_by` column.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/gc_means_barplot.svg').
        group_by (str): The column name in `per_sequence_df` to use for grouping
                        the data (e.g., 'Gene', 'Species'). Defaults to 'Gene'.
    """
    gc_cols: List[str] = ['GC', 'GC1', 'GC2', 'GC3', 'GC12']
    if per_sequence_df is None or per_sequence_df.empty:
         logger.warning("Input DataFrame is empty for GC means barplot.")
         return
    if group_by not in per_sequence_df.columns:
         logger.error(f"Grouping column '{group_by}' not found for GC means plot.")
         return
    missing_gc_cols = [col for col in gc_cols if col not in per_sequence_df.columns]
    if missing_gc_cols:
        logger.error(f"Missing required GC columns ({', '.join(missing_gc_cols)}) for GC means plot.")
        return

    fig: Optional[Figure] = None
    try:
        # Ensure GC columns are numeric
        df_numeric = per_sequence_df.copy()
        for col in gc_cols:
            df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')

        # Calculate mean GC values per group
        mean_gc_df = df_numeric.groupby(group_by)[gc_cols].mean().reset_index()

        if mean_gc_df.empty:
            logger.warning(f"No data after grouping by '{group_by}' for GC means plot.")
            return

        # Melt for easy plotting
        mean_gc_melted = mean_gc_df.melt(id_vars=[group_by], var_name='GC_Type', value_name='Mean_GC_Content')
        mean_gc_melted.dropna(subset=['Mean_GC_Content'], inplace=True)

        if mean_gc_melted.empty:
             logger.warning("No valid mean GC data after melting/filtering for GC means plot.")
             return

        # Sort groups for consistent order
        unique_groups = mean_gc_melted[group_by].unique()
        group_order = sorted([g for g in unique_groups if g != 'complete'])
        if 'complete' in unique_groups: group_order.append('complete')

        fig, ax = plt.subplots(figsize=(max(8, len(group_order) * 0.8), 6))

        sns.barplot(data=mean_gc_melted, x=group_by, y='Mean_GC_Content', hue='GC_Type',
                    order=group_order, palette='viridis', ax=ax)

        ax.set_title(f'Mean GC Content by {group_by}', fontsize=14)
        ax.set_xlabel(group_by, fontsize=12)
        ax.set_ylabel('Mean GC Content (%)', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        try:
            ax.legend(title='GC Type', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
            plt.tight_layout(rect=[0, 0, 0.88, 1])
        except Exception as legend_err:
             logger.warning(f"Could not place GC means plot legend optimally: {legend_err}.")
             plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"GC means barplot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during GC means plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating GC means barplot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_neutrality(per_sequence_df: pd.DataFrame,
                    output_filepath: str,
                    group_by_col: Optional[str] = None,
                    palette: Optional[Dict[str, Any]] = None,
                    plot_title_prefix: str = ""
                    ) -> None:
    """
    Generates a Neutrality Plot, visualizing the relationship between GC12 and GC3 content.
    This plot helps assess the influence of mutational bias versus natural selection on codon usage.

    Optionally, points can be colored based on a specified grouping column (e.g., 'Gene' or a metadata column).
    A linear regression line is fitted to the data, and its R-squared value is displayed.

    Args:
        per_sequence_df (pd.DataFrame): DataFrame containing per-sequence metrics.
                                        Must include 'GC12' and 'GC3' columns.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/neutrality_plot.svg').
        group_by_col (Optional[str]): The column name in `per_sequence_df` to use for
                                      coloring (hueing) the data points. If None, no hue is applied.
                                      Defaults to None.
        palette (Optional[Dict[str, Any]]): A dictionary mapping group names (from `group_by_col`)
                                            to specific colors. If None, Seaborn's default palette
                                            will be used. Defaults to None.
        plot_title_prefix (str): An optional prefix to add to the plot title (e.g., "Species X: ").
                                 Defaults to an empty string.
    """
    required_cols = ['GC12', 'GC3']
    if per_sequence_df is None or per_sequence_df.empty:
         logger.warning("Input DataFrame empty for Neutrality plot.")
         return
    missing_cols = [col for col in required_cols if col not in per_sequence_df.columns]
    if missing_cols:
        logger.error(f"Missing required columns ({', '.join(missing_cols)}) for Neutrality plot.")
        return
    if group_by_col and group_by_col not in per_sequence_df.columns:
        logger.warning(f"{plot_title_prefix}Grouping column '{group_by_col}' not found for Neutrality plot. Plotting without grouping.") #
        group_by_col = None # Disable grouping

    fig: Optional[Figure] = None
    scatter_plot_object: Optional[PathCollection] = None

    try:
        plot_df = per_sequence_df.copy()
        plot_df['GC3_num'] = pd.to_numeric(plot_df['GC3'], errors='coerce')
        plot_df['GC12_num'] = pd.to_numeric(plot_df['GC12'], errors='coerce')
        plot_df_valid = plot_df.dropna(subset=['GC3_num', 'GC12_num'])

        if len(plot_df_valid) < 2: # Need at least 2 points for linear regression
            logger.warning(f"{plot_title_prefix}Not enough valid data points (>=2) for Neutrality Plot regression/correlation. Skipping.")
            return

        # Determine grouping possibility for hueing
        # A hue column is used if provided, exists in data, is not all null, and has more than one unique value.
        hue_column_actual = group_by_col if group_by_col and not plot_df_valid[group_by_col].isnull().all() and plot_df_valid[group_by_col].nunique() > 0 else None
        legend_title = group_by_col if hue_column_actual else "Group" # Title for the legend

        fig, ax = plt.subplots(figsize=(8, 8))

        # Scatter plot
        scatter_plot_object = sns.scatterplot(
            data=plot_df_valid, 
            x='GC3_num', y='GC12_num', 
            hue=hue_column_actual,
            alpha=0.7, s=60, 
            palette=palette, 
            legend='full' if hue_column_actual else False, 
            ax=ax) 

        # Overall regression line (only if enough points)
        slope, intercept, r_value, p_value, std_err = np.nan, np.nan, np.nan, np.nan, np.nan
        r_squared = np.nan
        if len(plot_df_valid) >= 2 and scipy_stats_module is not None: # Check if scipy.stats was imported
            try:
                 slope, intercept, r_value, p_value, std_err = scipy_stats_module.linregress(plot_df_valid['GC3_num'], plot_df_valid['GC12_num'])
                 r_squared = r_value**2 if pd.notna(r_value) else np.nan
                 x_range = np.array([plot_df_valid['GC3_num'].min(), plot_df_valid['GC3_num'].max()])
                 y_vals = intercept + slope * x_range
                 ax.plot(x_range, y_vals, color="black", lw=1.5, ls='--', label=f"Overall (R²={r_squared:.3f})")
            except (ValueError, TypeError) as lin_reg_err:
                 logger.warning(f"Could not calculate overall regression for Neutrality plot: {lin_reg_err}")
                 slope, r_squared = np.nan, np.nan
        elif len(plot_df_valid) >= 2 and scipy_stats_module is None:
             logger.warning("Cannot calculate regression line for Neutrality plot: scipy.stats not available.")


        # Plotting customizations
        title = f'{plot_title_prefix}Neutrality Plot (GC12 vs GC3)'
        if hue_column_actual:
            title += f' (by {legend_title})'
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('GC3 Content (%)', fontsize=12)
        ax.set_ylabel('GC12 Content (%)', fontsize=12)
        ax.grid(True, linestyle=':', alpha=0.6)
        if not np.isnan(slope):
             # Display the calculated slope on the plot
             ax.text(0.05, 0.95, f'Overall Slope={slope:.3f}', transform=ax.transAxes, va='top',
                      bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

        # Adjust Axis Limits to provide some padding around the data
        min_gc3_val, max_gc3_val = plot_df_valid['GC3_num'].min(), plot_df_valid['GC3_num'].max()
        min_gc12_val, max_gc12_val = plot_df_valid['GC12_num'].min(), plot_df_valid['GC12_num'].max()
        x_padding = max((max_gc3_val - min_gc3_val) * 0.05, 2) # At least 2% padding
        y_padding = max((max_gc12_val - min_gc12_val) * 0.05, 2) # At least 2% padding
        x_limits = (max(0, min_gc3_val - x_padding), min(100, max_gc3_val + x_padding))
        y_limits = (max(0, min_gc12_val - y_padding), min(100, max_gc12_val + y_padding))
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        # Add a diagonal line (y=x) to represent neutrality
        diag_limits = [max(x_limits[0], y_limits[0]), min(x_limits[1], y_limits[1])]
        ax.plot(diag_limits, diag_limits, 'gray', linestyle=':', alpha=0.7, lw=1, label='y=x')
        ax.tick_params(axis='both', which='major', labelsize=10)

        # --- Add Adjusted Group Labels ---
        if hue_column_actual:
            texts: List[MatplotlibText] = []
            group_data_iter = plot_df_valid.groupby(hue_column_actual) # group_data renamed to group_data_iter
            for name, group_df in group_data_iter:
                if not group_df.empty:
                    mean_x, mean_y = group_df['GC3_num'].mean(), group_df['GC12_num'].mean()
                    text_color_val = palette.get(name, 'darkgrey') if palette and isinstance(palette, dict) else 'darkgrey' # group_color renamed text_color_val
                    txt = ax.text(mean_x, mean_y, str(name), fontsize=8, alpha=0.9, color=text_color_val,
                                  ha='center', va='center',
                                  bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))
                    texts.append(txt)
            if texts:
                if ADJUSTTEXT_AVAILABLE: # Check availability
                    try:
                        adjust_text(texts, ax=ax, add_objects=[scatter_plot_object] if scatter_plot_object else [],
                                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.6),
                                    force_points=(0.6, 0.8), force_text=(0.4, 0.6), expand_points=(1.3, 1.3))
                    except Exception as adj_err:
                        logger.warning(f"{plot_title_prefix}adjustText failed for Neutrality Plot labels: {adj_err}. Labels might overlap.")
                else: # Log if not available
                    logger.info(f"{plot_title_prefix}adjustText library not installed. Group labels on Neutrality Plot may overlap.")

        # Legend handling
        handles, plot_labels = ax.get_legend_handles_labels()
        if handles:
            try:
                if hue_column_actual:
                    ax.legend(title=legend_title, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
                    plt.tight_layout(rect=[0, 0, 0.85, 1])
                else:
                    ax.legend(loc='best') # Show legend for "y=x" and "Overall" if no hue
                    plt.tight_layout()
            except Exception as legend_err:
                logger.warning(f"{plot_title_prefix}Could not place Neutrality plot legend optimally: {legend_err}.")
                plt.tight_layout()
        else:
             plt.tight_layout()

        # Saving
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Neutrality plot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during Neutrality plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating Neutrality plot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_enc_vs_gc3(per_sequence_df: pd.DataFrame,
                    output_filepath: str,
                    group_by_col: Optional[str] = None,
                    palette: Optional[Dict[str, Any]] = None,
                    plot_title_prefix: str = ""
                   ) -> None:
    """
    Generates an Effective Number of Codons (ENC) vs. GC3 content plot,
    including Wright's theoretical expected curve. This plot helps to assess
    the degree of codon usage bias and the influence of GC content.

    Optionally, points can be colored based on a specified grouping column (e.g., 'Gene' or a metadata column).

    Args:
        per_sequence_df (pd.DataFrame): DataFrame containing per-sequence metrics.
                                        Must include 'ENC' and 'GC3' columns.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/enc_vs_gc3_plot.svg').
        group_by_col (Optional[str]): The column name in `per_sequence_df` to use for
                                      coloring (hueing) the data points. If None, no hue is applied.
                                      Defaults to None.
        palette (Optional[Dict[str, Any]]): A dictionary mapping group names (from `group_by_col`)
                                            to specific colors. If None, Seaborn's default palette
                                            will be used. Defaults to None.
        plot_title_prefix (str): An optional prefix to add to the plot title (e.g., "Gene X: ").
                                 Defaults to an empty string.
    """
    required_cols = ['ENC', 'GC3']
    if per_sequence_df is None or per_sequence_df.empty:
         logger.warning("Input DataFrame empty for ENC vs GC3 plot.")
         return
    missing_cols = [col for col in required_cols if col not in per_sequence_df.columns]
    if missing_cols:
        logger.error(f"Missing required columns ({', '.join(missing_cols)}) for ENC vs GC3 plot.")
        return
    if group_by_col and group_by_col not in per_sequence_df.columns:
        logger.warning(f"{plot_title_prefix}Grouping column '{group_by_col}' not found for ENC vs GC3 plot. Plotting without grouping.")
        group_by_col = None # Disable grouping if column not found

    fig: Optional[Figure] = None
    scatter_plot_object: Optional[PathCollection] = None

    try:
        plot_df = per_sequence_df.copy()
        # Ensure columns are numeric
        plot_df['ENC_num'] = pd.to_numeric(plot_df['ENC'], errors='coerce')
        plot_df['GC3_num'] = pd.to_numeric(plot_df['GC3'], errors='coerce')
        # Use GC3 fraction for Wright's curve comparison
        plot_df['GC3_frac'] = plot_df['GC3_num'] / 100.0
        plot_df_valid = plot_df.dropna(subset=['ENC_num', 'GC3_frac'])

        if plot_df_valid.empty:
            logger.warning("No valid ENC and GC3 data (after dropping NaNs) to plot.")
            return

        # Calculate Wright's theoretical expected ENC curve based on GC3 content (s_values)
        # Formula: ENC = 2 + s + 29 / (s^2 + (1-s)^2)
        # where s is the GC3 content (fraction)
        s_values = np.linspace(0.01, 0.99, 200) # GC3 fraction from 0.01 to 0.99
        denominator = (s_values**2 + (1 - s_values)**2)
        expected_enc = np.full_like(s_values, np.nan)
        # Avoid division by zero or very small numbers
        valid_denom = denominator > 1e-9
        expected_enc[valid_denom] = 2 + s_values[valid_denom] + (29 / denominator[valid_denom])
        # Replace any non-finite values (e.g., from division by zero if valid_denom check was insufficient) with NaN
        expected_enc = np.where(np.isfinite(expected_enc), expected_enc, np.nan)

        # Determine actual hue column and legend title
        hue_column_actual = group_by_col if group_by_col and not plot_df_valid[group_by_col].isnull().all() else None
        legend_title = group_by_col if hue_column_actual else "Group"

        fig, ax = plt.subplots(figsize=(9, 7))

        # Plot expected curve
        ax.plot(s_values, expected_enc, color='red', linestyle='--', lw=1.5, label="Expected ENC (No Selection)")

        # Plot scatter points
        scatter_plot_object =  sns.scatterplot(
            data=plot_df_valid, x='GC3_frac', y='ENC_num',
            hue=hue_column_actual, # Use the validated hue column
            alpha=0.7, s=60,
            palette=palette, # Use the passed palette
            legend='full' if hue_column_actual else False, # Show legend only if hueing
            ax=ax)
        
        # Customizations
        title = f'{plot_title_prefix}ENC vs GC3 Plot'
        if hue_column_actual:
            title += f' (by {legend_title})'
        ax.set_title(title, fontsize=14)        
        ax.set_xlabel('GC3 Content (Fraction)', fontsize=12)
        ax.set_ylabel('Effective Number of Codons (ENC)', fontsize=12)
        ax.set_xlim(0, 1)
        # Set Y-axis limits, ensuring a reasonable range for ENC values (typically 20-61)
        min_enc = max(15, plot_df_valid['ENC_num'].min() - 2) if not plot_df_valid.empty else 15
        max_enc = min(65, plot_df_valid['ENC_num'].max() + 2) if not plot_df_valid.empty else 65
        ax.set_ylim(min_enc, max_enc)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.tick_params(axis='both', which='major', labelsize=10)

        # --- Add Adjusted Groups Labels ---
        # Text labels for groups (e.g., mean point of each group) to avoid overlap
        if hue_column_actual:
            texts: List[MatplotlibText] = [] # Use the imported MatplotlibText for type hinting
            group_data = plot_df_valid.groupby(hue_column_actual)
            for name, group_df in group_data:
                if not group_df.empty:
                    mean_x = group_df['GC3_frac'].mean()
                    mean_y = group_df['ENC_num'].mean()
                    # Determine color for the text label based on the palette
                    text_color = 'darkgrey' # Default color if not found in palette
                    if isinstance(palette, dict) and name in palette:
                        text_color = palette[name]
                    # If palette is a seaborn named palette (str), seaborn handles colors internally.
                    # For text labels, we might need to manually map or use a default.
                    # For simplicity, we stick to default if palette is a string name.

                    txt = ax.text(mean_x, mean_y, str(name), fontsize=8, alpha=0.9, color=text_color,
                                  ha='center', va='center',
                                  bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7))
                    texts.append(txt)
            if texts:
                if ADJUSTTEXT_AVAILABLE: # Check if adjustText library is installed
                    try:
                        adjust_text(texts, ax=ax, add_objects=[scatter_plot_object] if scatter_plot_object else [],
                                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.6),
                                    force_points=(0.6,0.8), force_text=(0.4,0.6), expand_points=(1.3,1.3))
                    except Exception as adj_err:
                        logger.warning(f"adjustText failed for ENC vs GC3 labels: {adj_err}.")
                else: # Log if adjustText is not available
                    logger.info("adjustText library not installed. Group labels on ENC vs GC3 plot may overlap.")

        # Legend handling
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            try:
                if hue_column_actual:
                    ax.legend(title=legend_title, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
                    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust for external legend
                else: # Only "Expected ENC" legend
                    ax.legend(loc='best')
                    plt.tight_layout()
            except Exception as legend_err:
                 logger.warning(f"Could not place ENC vs GC3 plot legend optimally: {legend_err}.")
                 plt.tight_layout()
        else:
            plt.tight_layout()

        # Saving
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"ENC vs GC3 plot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during ENC vs GC3 plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating ENC vs GC3 plot: {e}")
    finally:
        if fig is not None: plt.close(fig)

# --- Function for per-gene dinucleotide abundance by metadata ---
def plot_per_gene_dinucleotide_abundance_by_metadata(
    per_sequence_oe_ratios_df: pd.DataFrame,
    metadata_hue_col: str,
    output_filepath: str,
    palette: Optional[Dict[str, Any]],
    gene_name: str,
) -> None:
    """
    Plots per-gene dinucleotide Observed/Expected (O/E) ratios, with lines and points
    aggregated and colored by a specified metadata column. This helps visualize
    how dinucleotide abundance patterns vary across different metadata categories
    for a given gene.

    Args:
        per_sequence_oe_ratios_df (pd.DataFrame): DataFrame containing per-sequence
            O/E ratios. Must include 'Dinucleotide', 'RelativeAbundance', and the
            column specified by `metadata_hue_col`.
        metadata_hue_col (str): The name of the column in `per_sequence_oe_ratios_df`
                                to use for coloring (hueing) the lines and points.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/gene_X_dinucleotide_oe.svg').
        palette (Optional[Dict[str, Any]]): A dictionary mapping metadata categories (from
                                            `metadata_hue_col`) to specific colors. If None,
                                            Seaborn's default palette will be used.
        gene_name (str): The name of the gene for which the plot is being generated.
                         Used in the plot title and logging.
    """
    logger.debug(f"Plotting dinucleotide O/E for gene '{gene_name}', hue by '{metadata_hue_col}'")
    fig: Optional[Figure] = None
    
    required_cols = ['Dinucleotide', 'RelativeAbundance', metadata_hue_col]
    if per_sequence_oe_ratios_df.empty or not all(col in per_sequence_oe_ratios_df.columns for col in required_cols):
        logger.warning(f"Insufficient data or missing columns for per-gene dinucleotide plot for '{gene_name}'. "
                       f"Required: {required_cols}. Has: {per_sequence_oe_ratios_df.columns.tolist()}. Skipping.")
        return

    try:
        plot_data = per_sequence_oe_ratios_df.copy()
        plot_data['RelativeAbundance'] = pd.to_numeric(plot_data['RelativeAbundance'], errors='coerce')
        plot_data.dropna(subset=['RelativeAbundance', 'Dinucleotide', metadata_hue_col], inplace=True)

        if plot_data.empty:
            logger.warning(f"No valid data remaining for per-gene dinucleotide plot for '{gene_name}' after filtering NaNs.")
            return

        # Ensure consistent order for dinucleotides
        dinucl_order = sorted(plot_data['Dinucleotide'].unique())
        
        # Sort metadata categories if possible (e.g., alphanumeric, or by count if desired)
        # For now, rely on seaborn's default or order from palette if it's a list of keys.
        hue_order = sorted(plot_data[metadata_hue_col].unique())


        fig_width = max(10, len(dinucl_order) * 0.65)
        fig, ax = plt.subplots(figsize=(fig_width, 6))

        # Use lineplot to show mean trend per metadata category
        # Standard error bands can be added by seaborn if desired (ci='sd' or ci=95)
        sns.lineplot(
            data=plot_data,
            x='Dinucleotide',
            y='RelativeAbundance',
            hue=metadata_hue_col,
            hue_order=hue_order,
            palette=palette, # Use the provided palette for metadata categories
            marker='o', # Add markers to lines
            markersize=5,
            errorbar=None, # Disable error bands for cleaner look, or use 'sd'
            ax=ax,
            legend='full'
        )

        ax.axhline(1.0, color='grey', linestyle='--', linewidth=1.2, label='Expected (O/E = 1.0)')
        
        title = f"Dinucleotide O/E Ratios for Gene: {gene_name}\nGrouped by {metadata_hue_col}"
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Dinucleotide', fontsize=12)
        ax.set_ylabel('Mean Relative Abundance (O/E)', fontsize=12) # Assuming lineplot shows mean
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle=':', alpha=0.7)

        # Legend handling
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            try:
                # Put legend outside plot
                ax.legend(title=metadata_hue_col, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
                plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust for external legend
            except Exception as legend_err:
                logger.warning(f"Could not place dinucleotide plot legend optimally for {gene_name}: {legend_err}.")
                plt.tight_layout()
        else:
            plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Per-gene dinucleotide abundance plot saved to: {output_path_obj}")

    except Exception as e:
        logger.exception(f"Error generating per-gene dinucleotide abundance plot for '{gene_name}': {e}")
    finally:
        if fig is not None:
            plt.close(fig)


def plot_ca_contribution(ca_results: PrinceCA,
                         dimension: int,
                         n_top: int,
                         output_filepath: str) -> None:
    """
    Generates a bar plot showing the percentage contribution of the top N variables (codons)
    to a specific dimension of a Correspondence Analysis (CA). This helps identify which
    codons are most influential in shaping a particular CA axis.

    Args:
        ca_results (PrinceCA): A fitted Correspondence Analysis (CA) object from the
                               'prince' library, containing the results of the CA.
        dimension (int): The 0-indexed CA dimension to analyze (e.g., 0 for Dimension 1,
                         1 for Dimension 2).
        n_top (int): The number of top contributing variables (codons) to display in the plot.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/ca_dim1_contribution.svg').
    """
    if prince is None or ca_results is None or not isinstance(ca_results, prince.CA): # Runtime check against imported module
        logger.warning("No valid CA results (or prince library missing) available for contribution plot.")
        return
    if not hasattr(ca_results, 'column_contributions_'):
        logger.error("CA results object missing 'column_contributions_'. Cannot plot contribution.")
        return

    fig: Optional[Figure] = None
    try:
        # Check if requested dimension exists
        if dimension >= ca_results.column_contributions_.shape[1]:
            logger.error(f"Requested dimension {dimension} exceeds available dimensions "
                         f"({ca_results.column_contributions_.shape[1]}) in CA results.")
            return

        # Get contributions for the specified dimension (%)
        contributions = pd.to_numeric(ca_results.column_contributions_.iloc[:, dimension] * 100, errors='coerce')
        contributions.dropna(inplace=True) # Remove codons if contribution couldn't be calculated

        if contributions.empty:
             logger.warning(f"No valid contribution data found for CA dimension {dimension+1}.")
             return

        # Sort by contribution descending and select top N
        top_contributors = contributions.sort_values(ascending=False).head(n_top)

        fig, ax = plt.subplots(figsize=(8, max(5, n_top * 0.4))) # Adjust height based on N

        # Barplot (horizontal for better codon label readability)
        sns.barplot(
            x=top_contributors.values, 
            y=top_contributors.index,
            palette='viridis',
            hue=top_contributors.index,
            legend=False,
            orient='h', 
            ax=ax)
        # Removed hue=top_contributors.index and legend=False as simple palette works better

        ax.set_title(f'Top {n_top} Contributing Codons to CA Dimension {dimension+1}', fontsize=14)
        ax.set_xlabel('Contribution (%)', fontsize=12)
        ax.set_ylabel('Codon', fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=9)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        # Add text labels for percentage values
        try:
            for i, v in enumerate(top_contributors.values):
                if pd.notna(v):
                    # Position text slightly to the right of the bar end
                    ax.text(v + contributions.max()*0.01, i, f'{v:.2f}%', color='black', va='center', fontsize=8)
        except Exception as text_err:
             logger.warning(f"Could not add text labels to CA contribution plot: {text_err}")

        plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"CA contribution plot for Dim {dimension+1} saved to: {output_path_obj}")

    except AttributeError as ae:
         logger.error(f"AttributeError accessing CA results for contribution plot: {ae}")
    except (ValueError, TypeError) as data_err:
         logger.error(f"Data error during CA contribution plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating CA contribution plot for Dim {dimension+1}: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_ca_variance(ca_results: PrinceCA,
                     n_dims: int,
                     output_filepath: str) -> None:
    """
    Generates a bar plot showing the percentage of variance explained by the
    first N dimensions of a Correspondence Analysis (CA). This plot helps
    determine the optimal number of dimensions to retain for further analysis.

    Args:
        ca_results (PrinceCA): A fitted Correspondence Analysis (CA) object from the
                               'prince' library, containing the eigenvalues summary.
        n_dims (int): The maximum number of CA dimensions to display in the plot.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/ca_variance_explained.svg').
    """
    if prince is None or ca_results is None or not isinstance(ca_results, prince.CA): # Runtime check against imported module
        logger.warning("No valid CA results (or prince library missing) available for contribution plot.")
        return
    if not hasattr(ca_results, 'eigenvalues_summary'):
        logger.error("CA results object missing 'eigenvalues_summary'. Cannot plot variance.")
        return

    fig: Optional[Figure] = None
    try:
        variance_summary = ca_results.eigenvalues_summary
        variance_col_name = '% of variance' # Expected column name
        if variance_col_name not in variance_summary.columns:
            # Try alternative common names if primary name not found
            alt_names = ['% variance', 'explained_variance_ratio']
            found = False
            for name in alt_names:
                 if name in variance_summary.columns:
                     variance_col_name = name
                     found = True
                     break
            if not found:
                logger.error(f"Could not find variance column ('{variance_col_name}' or alternatives) in eigenvalues_summary.")
                return

        # Clean and convert variance percentage column
        try:
            variance_pct_raw = variance_summary[variance_col_name]
            # Convert to string, remove '%', strip whitespace, then convert to numeric
            variance_pct = pd.to_numeric(
                variance_pct_raw.astype(str).str.replace('%', '', regex=False).str.strip(),
                errors='coerce' # Turn errors into NaN
            )
        except (KeyError, TypeError, ValueError) as conv_err:
            logger.error(f"Error accessing or converting variance column '{variance_col_name}': {conv_err}")
            return

        variance_pct.dropna(inplace=True) # Remove NaNs from conversion errors

        if variance_pct.empty:
             logger.warning("No valid numeric variance data found after cleaning/conversion.")
             return

        n_dims_actual = min(n_dims, len(variance_pct)) # Number of dims to actually plot
        if n_dims_actual < 1:
            logger.warning("No dimensions available to plot for CA variance.")
            return

        variance_to_plot = variance_pct.head(n_dims_actual)
        dims = np.arange(1, n_dims_actual + 1) # Dimension numbers (1, 2, ...)

        fig, ax = plt.subplots(figsize=(max(6, n_dims_actual * 0.7), 5))

        # Barplot
        sns.barplot(x=dims, 
                    y=variance_to_plot.values, 
                    palette='mako',
                    hue=dims,
                    legend=False,
                    ax=ax)

        ax.set_title(f'Variance Explained by First {n_dims_actual} CA Dimensions', fontsize=14)
        ax.set_xlabel('Dimension', fontsize=12)
        ax.set_ylabel('Variance Explained (%)', fontsize=12)
        ax.set_xticks(np.arange(n_dims_actual)) # Set ticks to 0, 1, ...
        ax.set_xticklabels(dims) # Set labels to 1, 2, ...
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.set_ylim(0, max(variance_to_plot.max() * 1.1, 10)) # Adjust y limit
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Add text labels above bars
        try:
            for i, v in enumerate(variance_to_plot.values):
                 if pd.notna(v):
                      ax.text(i, v + ax.get_ylim()[1]*0.01, f'{v:.2f}%', ha='center', va='bottom', fontsize=9)
        except Exception as text_err:
            logger.warning(f"Could not add text labels to CA variance plot: {text_err}")

        plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"CA variance explained plot saved to: {output_path_obj}")

    except AttributeError as ae:
        logger.error(f"AttributeError accessing CA results for variance plot: {ae}")
    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during CA variance plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating CA variance explained plot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_ca(
    ca_results: PrinceCA,
    ca_input_df: pd.DataFrame,
    output_filepath: str,
    comp_x: int = 0,
    comp_y: int = 1,
    groups: Optional[pd.Series] = None,
    palette: Optional[Dict[str, Any]] = None,
    plot_title_prefix: str = ""
) -> None:
    """
    Generates a Correspondence Analysis (CA) biplot, visualizing the relationships
    between rows (e.g., sequences/genes) and columns (e.g., codons) in a reduced
    dimensional space.

    Optionally, row points can be colored based on a provided `groups` Series
    (e.g., metadata categories like species or lineage). Labels for these groups
    are added and adjusted to minimize overlap.

    Args:
        ca_results (PrinceCA): A fitted Correspondence Analysis (CA) object from the
                               'prince' library, containing the CA results.
        ca_input_df (pd.DataFrame): The original DataFrame used as input for fitting
                                    the CA model. This is used to extract row and
                                    column coordinates.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/ca_biplot.svg').
        comp_x (int): The 0-indexed CA component to plot on the X-axis (e.g., 0 for Dim 1).
                      Defaults to 0.
        comp_y (int): The 0-indexed CA component to plot on the Y-axis (e.g., 1 for Dim 2).
                      Defaults to 1.
        groups (Optional[pd.Series]): A pandas Series containing grouping information for
                                      the rows (sequences/genes). Its index should align
                                      with the index of `ca_input_df`. If provided, row
                                      points will be colored by these groups. Defaults to None.
        palette (Optional[Dict[str, Any]]): A dictionary mapping group names (from `groups`)
                                            to specific colors. If None, Seaborn's default palette
                                            will be used. Defaults to None.
        plot_title_prefix (str): An optional prefix to add to the plot title (e.g., "Species X: ").
                                 Defaults to an empty string.
    """
    if prince is None or ca_results is None or not isinstance(ca_results, prince.CA): 
        logger.warning(f"{plot_title_prefix}No valid CA results (or prince library missing) to plot. Skipping.") 
        return
    if ca_input_df is None or ca_input_df.empty: 
         logger.error(f"{plot_title_prefix}CA input DataFrame for coordinates is missing or empty. Skipping.") 
         return

    fig: Optional[Figure] = None
    row_scatter_object: Optional[PathCollection] = None

    try:
        # Get coordinates using the input df used for fitting
        row_coords_raw: Optional[pd.DataFrame] = None
        col_coords_raw: Optional[pd.DataFrame] = None
        try:
             row_coords_raw = ca_results.row_coordinates(ca_input_df) 
             col_coords_raw = ca_results.column_coordinates(ca_input_df) 
        except Exception as coord_err: #
             logger.error(f"{plot_title_prefix}Error getting coordinates from CA object: {coord_err}. Skipping.") 
             return

        # Filter out non-finite coordinates
        coords_to_plot: List[int] = [comp_x, comp_y] 
        row_coords: Optional[pd.DataFrame] = None
        col_coords: Optional[pd.DataFrame] = None

        if row_coords_raw is not None:
            try:
                row_coords = row_coords_raw.replace([np.inf, -np.inf], np.nan).dropna(subset=coords_to_plot) 
            except KeyError: 
                 logger.error(f"{plot_title_prefix}Requested CA components for rows ({comp_x}, {comp_y}) not found. Skipping.") 
                 row_coords = pd.DataFrame() # Empty
        if col_coords_raw is not None:
            try:
                col_coords = col_coords_raw.replace([np.inf, -np.inf], np.nan).dropna(subset=coords_to_plot) 
            except KeyError: 
                 logger.warning(f"{plot_title_prefix}Requested CA components for columns ({comp_x}, {comp_y}) not found for plot.") 
                 col_coords = pd.DataFrame() # Empty

        if (row_coords is None or row_coords.empty) and (col_coords is None or col_coords.empty): 
             logger.warning(f"{plot_title_prefix}No finite CA coordinates found after filtering. Skipping CA plot.") 
             return

        # Get variance explained for axis labels
        x_label_val, y_label_val = f'Component {comp_x+1}', f'Component {comp_y+1}'
        try:
            if hasattr(ca_results, 'eigenvalues_summary'): 
                variance_explained = ca_results.eigenvalues_summary 
                variance_col_name = '% of variance'
                if variance_col_name not in variance_explained.columns: 
                     alt_names_list = ['% variance', 'explained_variance_ratio']
                     for name_iter in alt_names_list:
                          if name_iter in variance_explained.columns: variance_col_name = name_iter; break
                if variance_col_name in variance_explained.columns and comp_x < len(variance_explained) and comp_y < len(variance_explained):
                    x_var_str = str(variance_explained.loc[comp_x, variance_col_name]).replace('%','').strip()
                    y_var_str = str(variance_explained.loc[comp_y, variance_col_name]).replace('%','').strip()
                    x_variance = float(x_var_str)
                    y_variance = float(y_var_str)
                    x_label_val = f'Component {comp_x+1} ({x_variance:.2f}%)'
                    y_label_val = f'Component {comp_y+1} ({y_variance:.2f}%)'
                else:
                     logger.warning("Could not retrieve or format variance explained for CA plot labels.")
            else:
                 logger.warning("'eigenvalues_summary' not found in CA results. Using default axis labels.")
        except (AttributeError, KeyError, ValueError, TypeError) as fmt_err:
             logger.warning(f"{plot_title_prefix}Could not format variance explained for CA plot labels: {fmt_err}. Using default labels.")

        fig, ax = plt.subplots(figsize=(10, 10))

        # Logic to determine if hueing (coloring by groups) should be performed
        perform_hueing = False
        legend_title = "Group" # Default legend title
        groups_for_hue: Optional[pd.Series] = None # Series to hold the actual group data for hueing

        if groups is not None and isinstance(groups, pd.Series) and row_coords is not None and not row_coords.empty:
            try:
                # Align the 'groups' Series with the filtered 'row_coords' index to ensure matching data points
                groups_aligned = groups.reindex(row_coords.index).dropna()
                # Proceed with hueing only if there are valid groups and more than one unique category
                if not groups_aligned.empty and groups_aligned.nunique() > 0:
                    perform_hueing = True
                    # Use the name of the groups Series as the legend title, or a default "Category"
                    legend_title = groups_aligned.name if groups_aligned.name else "Category"
                    groups_for_hue = groups_aligned
                elif not groups_aligned.empty:
                     logger.info(f"{plot_title_prefix}Only one unique group found for CA plot points after filtering. Coloring will be uniform for rows.")
            except Exception as group_err:
                logger.warning(f"{plot_title_prefix}Error processing groups for CA plot: {group_err}. Plotting rows without hue.")
                perform_hueing = False

        # Plot row points (sequences/genes)
        if row_coords is not None and not row_coords.empty:
            # Create a temporary DataFrame for plotting with hue to avoid modifying the original row_coords
            plot_data_rows = row_coords.copy()
            if perform_hueing and groups_for_hue is not None:
                # Assign the groups data to a new column in the temporary DataFrame for seaborn's hue parameter
                # Ensure the hue column name is unique and does not clash with existing columns
                hue_col_name = legend_title if legend_title not in plot_data_rows.columns else f"{legend_title}_hue"
                plot_data_rows[hue_col_name] = groups_for_hue
                row_scatter_object = sns.scatterplot(
                    data=plot_data_rows, x=comp_x, y=comp_y, hue=hue_col_name,
                    ax=ax, s=60, alpha=0.7, palette=palette, legend='full')
            else:
                # If no hueing, plot all row points with a default color
                row_scatter_object = ax.scatter(row_coords[comp_x], row_coords[comp_y], s=60, alpha=0.7, label='Rows (Sequences)', color='blue')

        # Plot column points (codons) - currently commented out to reduce clutter and focus on row points.
        # If re-enabled, consider adding adjust_text for column labels as well.
        # """
        # if col_coords is not None and not col_coords.empty:
        #     ax.scatter(col_coords[comp_x], col_coords[comp_y], marker='x', s=40, alpha=0.6, c='dimgray', label='Cols (Codons)')
        #     if len(col_coords) < 30: # Add labels for codons only if not too many, to avoid clutter
        #         texts_col_labels: List[MatplotlibText] = []
        #         for idx, txt_val in enumerate(col_coords.index):
        #              texts_col_labels.append(ax.text(col_coords.iloc[idx, comp_x], col_coords.iloc[idx, comp_y], txt_val, fontsize=7, color='darkred', alpha=0.8))
        #         if ADJUSTTEXT_AVAILABLE and texts_col_labels:
        #             try: adjust_text(texts_col_labels, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.5))
        #             except Exception as adj_err_col: logger.warning(f"adjustText for CA column labels failed: {adj_err_col}")
        #         elif not ADJUSTTEXT_AVAILABLE and texts_col_labels:
        #             logger.info(f"{plot_title_prefix}adjustText library not installed. CA column labels may overlap.")
        # """

        # Add Adjusted Row Labels (if hueing by groups)
        # Encapsulate adjust_text usage for row labels
        if perform_hueing and groups_for_hue is not None and row_coords is not None:
            texts_row_labels: List[MatplotlibText] = []
            # Use plot_data_rows which has the hue column
            temp_label_df_ca = plot_data_rows.copy() # plot_data_rows already created if perform_hueing is True

            group_data_ca_iter = temp_label_df_ca.groupby(legend_title) # Group by the actual hue column name
            for name_val, group_df_ca in group_data_ca_iter:
                if not group_df_ca.empty:
                    mean_x_ca, mean_y_ca = group_df_ca[comp_x].mean(), group_df_ca[comp_y].mean()
                    # Determine the text color for the group label, prioritizing the provided palette
                    text_color_ca = palette.get(name_val, 'darkgrey') if palette and isinstance(palette, dict) else 'darkgrey'
                    txt_obj = ax.text(mean_x_ca, mean_y_ca,
                                      str(name_val), fontsize=8, alpha=0.9,
                                      color=text_color_ca,
                                      ha='center', va='center',
                                      bbox=dict(boxstyle='round,pad=0.2',
                                                fc='white', ec='none', alpha=0.7))
                    texts_row_labels.append(txt_obj)
            if texts_row_labels:
                if ADJUSTTEXT_AVAILABLE: # Check if adjustText library is installed
                    try:
                        adjust_text(texts_row_labels, ax=ax,
                                    add_objects=[row_scatter_object] if row_scatter_object else [],
                                    arrowprops=dict(arrowstyle='-', color='gray',
                                                    lw=0.5, alpha=0.6),
                                    force_points=(0.7, 0.9), force_text=(0.6, 0.8),
                                    expand_points=(1.3,1.3))
                    except Exception as adj_err_row:
                        logger.warning(f"{plot_title_prefix}adjustText for CA row group labels failed: {adj_err_row}.")
                else: # Log if adjustText is not available
                    logger.info(f"{plot_title_prefix}adjustText library not installed. CA row group labels may overlap.")

        # Customizations
        plot_main_title = f'{plot_title_prefix}Correspondence Analysis (Components {comp_x+1} & {comp_y+1})'
        if perform_hueing:
            plot_main_title += f' by {legend_title}'
        ax.set_title(plot_main_title, fontsize=14)
        ax.set_xlabel(x_label_val, fontsize=12)
        ax.set_ylabel(y_label_val, fontsize=12)
        ax.axhline(0, color='grey', lw=0.7, linestyle='--')
        ax.axvline(0, color='grey', lw=0.7, linestyle='--')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Adjust layout
        current_handles, current_labels = ax.get_legend_handles_labels() # Get handles and labels after all plotting
        if current_handles:
            try:
                # If hueing by groups, the legend title is already set by seaborn if legend='full'
                # If not hueing by groups, or if we want to customize, we can do it here.
                if perform_hueing: # If hueing by groups, seaborn's legend is usually sufficient
                    ax.legend(title=legend_title, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
                    # Adjust layout to make space for the external legend
                    plt.tight_layout(rect=[0, 0, 0.85, 1])
                else: # If no hueing, show legend for 'Rows' and 'y=x' line if present
                    ax.legend(loc='best')
                    plt.tight_layout()
            except Exception as legend_err:
                logger.warning(f"{plot_title_prefix}Could not place CA plot legend optimally: {legend_err}")
                plt.tight_layout()
        else:
            plt.tight_layout()

        # Saving
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"CA biplot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError, AttributeError) as data_err:
         logger.error(f"{plot_title_prefix}Data error during CA plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"{plot_title_prefix}Error generating CA plot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_usage_comparison(agg_usage_df: pd.DataFrame,
                          reference_data: pd.DataFrame,
                          output_filepath: str) -> None:
    """
    Generates a scatter plot comparing observed RSCU values against reference RSCU values.
    A regression line and R-squared value are included to quantify the correlation.

    Args:
        agg_usage_df (pd.DataFrame): DataFrame containing the calculated aggregate RSCU values.
                                    Must include 'Codon' and 'RSCU' columns.
        reference_data (pd.DataFrame): DataFrame containing reference RSCU values.
                                      Its index should be 'Codon' and it must have an 'RSCU' column.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/rscu_comparison.svg').
    """
    if reference_data is None or 'RSCU' not in reference_data.columns:
        logger.warning("Cannot plot RSCU comparison: reference RSCU data not available or missing 'RSCU' column.")
        return
    if agg_usage_df is None or agg_usage_df.empty or 'RSCU' not in agg_usage_df.columns or 'Codon' not in agg_usage_df.columns:
        logger.warning("Cannot plot RSCU comparison: calculated aggregate RSCU data invalid or missing columns.")
        return

    fig: Optional[Figure] = None
    try:
        # Prepare dataframes for merging
        obs_rscu = agg_usage_df[['Codon', 'RSCU']].rename(columns={'RSCU': 'Observed_RSCU'})
        ref_rscu = reference_data[['RSCU']].rename(columns={'RSCU': 'Reference_RSCU'}) # Assumes 'Codon' is index

        # Merge observed and reference RSCU on Codon
        comp_df = pd.merge(obs_rscu, ref_rscu, left_on='Codon', right_index=True, how='inner')
        comp_df.dropna(inplace=True) # Drop codons where either RSCU is NaN

        if comp_df.empty:
            logger.warning("No common codons with valid RSCU values found for comparison plot.")
            return

        # Ensure data is numeric
        comp_df['Observed_RSCU'] = pd.to_numeric(comp_df['Observed_RSCU'], errors='coerce')
        comp_df['Reference_RSCU'] = pd.to_numeric(comp_df['Reference_RSCU'], errors='coerce')
        comp_df.dropna(inplace=True)

        if len(comp_df) < 2:
            logger.warning("Not enough comparable RSCU points (>=2) for scatter plot.")
            return

        # Calculate correlation
        correlation = comp_df['Reference_RSCU'].corr(comp_df['Observed_RSCU'])
        r_squared = correlation**2 if pd.notna(correlation) else np.nan

        # Plot scatter with regression line
        fig, ax = plt.subplots(figsize=(7, 7))
        sns.regplot(x='Reference_RSCU', y='Observed_RSCU', data=comp_df,
                     line_kws={"color": "blue", "lw": 1},
                     scatter_kws={"alpha": 0.6, "s": 50}, ax=ax)

        ax.set_title('Observed vs Reference RSCU Comparison')
        ax.set_xlabel('Reference RSCU')
        ax.set_ylabel('Observed RSCU')
        ax.grid(True, linestyle='--', alpha=0.6)
        if pd.notna(r_squared):
             ax.text(0.05, 0.95, f'R²={r_squared:.3f}', transform=ax.transAxes, va='top',
                      bbox=dict(boxstyle='round,pad=0.3', fc='lightcyan', alpha=0.7))

        # Add a diagonal line (y=x) to indicate perfect correlation
        all_vals = pd.concat([comp_df['Reference_RSCU'], comp_df['Observed_RSCU']])
        # Determine plot limits based on data, with a small padding, ensuring non-negative values
        lim_min = max(0, all_vals.min() - 0.1) if not all_vals.empty else 0
        lim_max = all_vals.max() + 0.1 if not all_vals.empty else 1.0
        lims = [lim_min, lim_max]
        ax.plot(lims, lims, 'k--', alpha=0.7, lw=1, label='y=x')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.legend()
        plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"RSCU comparison plot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during RSCU comparison plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating RSCU comparison plot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_relative_dinucleotide_abundance(rel_abund_df: pd.DataFrame,
                                         output_filepath: str,
                                         palette: Optional[Dict[str, Any]] = None
                                         ) -> None:
    """
    Plots the relative dinucleotide abundance (Observed/Expected ratio) per gene
    using a line plot. Each line represents a gene, showing how the O/E ratio
    varies across different dinucleotides.

    Args:
        rel_abund_df (pd.DataFrame): DataFrame in long format containing relative
                                     dinucleotide abundance data. Must include
                                     'Gene', 'Dinucleotide', and 'RelativeAbundance' columns.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/relative_dinucleotide_abundance.svg').
        palette (Optional[Dict[str, Any]]): A dictionary mapping gene names to specific colors.
                                            If None, Seaborn's default palette will be used.
                                            Defaults to None.
    """
    required_cols = ['Gene', 'Dinucleotide', 'RelativeAbundance']
    if rel_abund_df is None or rel_abund_df.empty:
        logger.warning("No relative dinucleotide abundance data to plot.")
        return
    if not all(col in rel_abund_df.columns for col in required_cols):
        logger.error(f"Missing required columns ({', '.join(required_cols)}) for relative dinucleotide plot.")
        return

    fig: Optional[Figure] = None
    try:
        # Ensure numeric and drop NaNs (where O/E might be undefined)
        plot_data = rel_abund_df.copy()
        plot_data['RelativeAbundance'] = pd.to_numeric(plot_data['RelativeAbundance'], errors='coerce')
        plot_data.dropna(subset=['RelativeAbundance'], inplace=True)

        if plot_data.empty:
            logger.warning("No valid relative dinucleotide abundance data remaining after filtering NaN.")
            return

        # Ensure consistent order
        dinucl_order = sorted(plot_data['Dinucleotide'].unique())
        unique_genes = plot_data['Gene'].unique()
        gene_order = sorted([g for g in unique_genes if g != 'complete'])
        if 'complete' in unique_genes: gene_order.append('complete')

        # Determine figure width dynamically based on the number of dinucleotides to ensure readability
        fig_width = max(10, len(dinucl_order) * 0.6)
        fig, ax = plt.subplots(figsize=(fig_width, 6))

        # Use lineplot to connect points for each gene
        sns.lineplot(
            data=plot_data, x='Dinucleotide', y='RelativeAbundance',
            hue='Gene', style='Gene', hue_order=gene_order, style_order=gene_order,
            markers=True, markersize=7, palette=palette, legend='full', ax=ax)

        # Add horizontal line at y=1.0 (Expected ratio)
        ax.axhline(1.0, color='grey', linestyle='--', linewidth=1, label='Expected (O/E = 1)')

        ax.set_title('Relative Dinucleotide Abundance (Observed/Expected)', fontsize=14)
        ax.set_xlabel('Dinucleotide', fontsize=12)
        ax.set_ylabel('Relative Abundance (O/E Ratio)', fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(axis='y', linestyle=':', alpha=0.7)

        # Adjust legend position
        try:
            ax.legend(title='Gene', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
            plt.tight_layout(rect=[0, 0, 0.88, 1])
        except Exception as legend_err:
             logger.warning(f"Could not place relative dinuc abundance legend optimally: {legend_err}.")
             plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Relative dinucleotide abundance plot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during relative dinucleotide abundance plot generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating relative dinucleotide abundance plot: {e}")
    finally:
        if fig is not None: plt.close(fig)


def plot_rscu_boxplot_per_gene(
    long_rscu_df: pd.DataFrame,
    agg_rscu_df: pd.DataFrame,
    gene_name: str,
    output_filepath: str
) -> None:
    """
    Generates a box plot visualizing the distribution of RSCU values for each codon
    within a specific gene. Codons are grouped by their corresponding amino acid on the x-axis.
    The x-axis labels for codons are colored to highlight those with the highest (red)
    and lowest (blue) mean RSCU values within their synonymous family, based on aggregate data.

    Args:
        long_rscu_df (pd.DataFrame): DataFrame containing RSCU values in a "long" format,
                                     typically with columns like 'SeqID', 'Codon', 'RSCU',
                                     'AminoAcid', and 'Gene'. This is used for the boxplot distributions.
        agg_rscu_df (pd.DataFrame): DataFrame containing aggregate (mean) RSCU values per codon.
                                     Must include 'Codon', 'AminoAcid', and 'RSCU' columns.
                                     This data is used to determine the coloring of x-axis labels.
        gene_name (str): The name of the gene for which the plot is being generated.
                         Used in the plot title and logging.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/gene_X_rscu_boxplot.svg').
    """
    long_req_cols = ['Codon', 'AminoAcid', 'RSCU']
    agg_req_cols = ['Codon', 'AminoAcid', 'RSCU']

    if long_rscu_df is None or long_rscu_df.empty or not all(c in long_rscu_df.columns for c in long_req_cols):
        logger.warning(f"Skipping RSCU boxplot for '{gene_name}'. Input distribution data invalid.")
        return
    if agg_rscu_df is None or agg_rscu_df.empty or not all(c in agg_rscu_df.columns for c in agg_req_cols):
        logger.warning(f"Skipping RSCU boxplot label coloring for '{gene_name}'. Input aggregate data invalid.")
        # Proceed with boxplot but without coloring if agg data is bad
        color_ref_data = pd.DataFrame() # Use empty df for coloring logic
    else:
        color_ref_data = agg_rscu_df.copy()

    fig: Optional[Figure] = None
    try:
        # Prepare data for boxplot (long format)
        plot_data = long_rscu_df.dropna(subset=['RSCU', 'AminoAcid']).copy()
        plot_data = plot_data[plot_data['AminoAcid'] != '*'] # Exclude stops
        plot_data['RSCU'] = pd.to_numeric(plot_data['RSCU'], errors='coerce')
        plot_data.dropna(subset=['RSCU'], inplace=True)

        if plot_data.empty:
             logger.warning(f"Skipping RSCU boxplot for '{gene_name}'. No valid RSCU data for coding codons in long format.")
             return

        # Prepare aggregate data for label coloring (use color_ref_data)
        # This logic identifies the most and least preferred codons within each synonymous family
        # based on their aggregate RSCU values, to color the x-axis labels.
        codon_colors: Dict[str, str] = {}
        if not color_ref_data.empty:
            color_ref_data = color_ref_data.dropna(subset=['RSCU', 'AminoAcid']).copy()
            color_ref_data = color_ref_data[color_ref_data['AminoAcid'] != '*'] # Exclude stop codons from coloring logic
            color_ref_data['RSCU'] = pd.to_numeric(color_ref_data['RSCU'], errors='coerce')
            color_ref_data.dropna(subset=['RSCU'], inplace=True)

            if not color_ref_data.empty:
                # Group by AminoAcid to find max/min RSCU within each synonymous family
                aa_groups_for_color = color_ref_data.groupby('AminoAcid')
                for aa, group in aa_groups_for_color:
                    if len(group) > 1 and group['RSCU'].notna().any(): # Only if multiple codons and valid RSCU
                        max_rscu = group['RSCU'].max()
                        min_rscu = group['RSCU'].min()
                        if not np.isclose(max_rscu, min_rscu): # Only color if there's variation
                            for _, row in group.iterrows():
                                codon, rscu_val = row['Codon'], row['RSCU']
                                if pd.notna(rscu_val):
                                    if np.isclose(rscu_val, max_rscu): codon_colors[codon] = 'red' # Most preferred
                                    elif np.isclose(rscu_val, min_rscu): codon_colors[codon] = 'blue' # Least preferred
                                    else: codon_colors[codon] = 'black' # Others
                                else: codon_colors[codon] = 'black' # Fallback for NaN RSCU
                        else: # All values are the same or only one codon for this AA
                            for codon in group['Codon']: codon_colors[codon] = 'black'
                    else: # Single codon or no valid RSCU for this AA
                        for codon in group['Codon']: codon_colors[codon] = 'black'
            else:
                logger.debug(f"No valid aggregate data for label coloring for '{gene_name}'.")


        # Get AA codes and sort plot_data for consistent axis order
        plot_data['AA3'] = plot_data['AminoAcid'].map(AA_1_TO_3)
        # Ensure consistent Amino Acid ordering using the predefined AA_ORDER
        plot_data['AminoAcid'] = pd.Categorical(plot_data['AminoAcid'], categories=AA_ORDER, ordered=True)
        plot_data.sort_values(by=['AminoAcid', 'Codon'], inplace=True)
        # Determine the final order of codons for the x-axis based on the sorted data
        codon_order: List[str] = plot_data['Codon'].unique().tolist()

        # Calculate bounds for vertical separator lines and positions for AA labels
        aa_group_bounds: Dict[str, Dict[str, Union[float, int]]] = {}
        current_aa: Optional[str] = None
        # Create a temporary mapping from sorted unique codons back to their amino acid
        temp_aa_map = plot_data.drop_duplicates(subset=['Codon'])[['Codon', 'AminoAcid']].set_index('Codon')['AminoAcid']
        for i, codon in enumerate(codon_order):
            aa = temp_aa_map.get(codon)
            if aa is None: continue # Should not happen if codon_order comes from plot_data
            aa = str(aa) # Ensure string key for dictionary
            if aa != current_aa:
                if current_aa is not None and current_aa in aa_group_bounds:
                    aa_group_bounds[current_aa]['end'] = i - 0.5 # End of previous AA group
                    aa_group_bounds[current_aa]['mid'] = (aa_group_bounds[current_aa]['start_idx'] + i - 1) / 2 # Midpoint for label
                current_aa = aa
                if current_aa not in aa_group_bounds: aa_group_bounds[current_aa] = {}
                aa_group_bounds[current_aa]['start'] = i - 0.5 # Start of current AA group
                aa_group_bounds[current_aa]['start_idx'] = i # Index of first codon in group
        # Finalize the last group's bounds
        if current_aa is not None and current_aa in aa_group_bounds and 'start_idx' in aa_group_bounds[current_aa]:
            aa_group_bounds[current_aa]['end'] = len(codon_order) - 0.5
            aa_group_bounds[current_aa]['mid'] = (aa_group_bounds[current_aa]['start_idx'] + len(codon_order) - 1) / 2


        # --- Plotting ---
        fig, ax1 = plt.subplots(figsize=(18, 7))

        # Box plot for RSCU distributions per codon
        sns.boxplot(
            data=plot_data, x='Codon', y='RSCU', order=codon_order, ax=ax1,
            palette="vlag", fliersize=2, linewidth=0.8, showmeans=False,
            hue='Codon', legend=False # Use hue to map colors to individual codons but disable its legend
            )

        # Set primary X-axis ticks and labels (Codons)
        ax1.set_xticks(np.arange(len(codon_order)))
        ax1.set_xticklabels(codon_order, rotation=90, fontsize=8)

        # Color the codon tick labels based on preferred/least preferred status
        for ticklabel, codon in zip(ax1.get_xticklabels(), codon_order):
            ticklabel.set_color(codon_colors.get(codon, 'black')) # Default to black if no specific color

        ax1.set_ylabel('RSCU Value Distribution', fontsize=12)
        ax1.set_xlabel('Codon', fontsize=12)
        ax1.set_title(f'RSCU Distribution for Gene: {gene_name}', fontsize=14)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        ax1.set_xlim(-0.7, len(codon_order) - 0.3)
        ax1.set_ylim(bottom=max(0, plot_data['RSCU'].min() - 0.1)) # Adjust bottom limit slightly below min if needed
        ax1.tick_params(axis='x', which='major', pad=1)

        # Add vertical separator lines between Amino Acid groups
        valid_bounds = [b for b in aa_group_bounds.values() if 'start' in b]
        for bounds in valid_bounds:
            if bounds['start'] > -0.5: ax1.axvline(x=bounds['start'], color='grey', linestyle=':', linewidth=1.2)
        ax1.axvline(x=len(codon_order) - 0.5, color='grey', linestyle=':', linewidth=1.2) # Final line at the end of the last group


        # Add centered Amino Acid labels using a secondary x-axis (twiny)
        ax2: Axes = ax1.twiny() # Create secondary axis sharing the y-axis
        ax2.set_xlim(ax1.get_xlim()) # Ensure secondary axis has same x-limits as primary
        aa_ticks: List[float] = []
        aa_labels_3_letter: List[str] = []
        # Ensure AAs are added in the canonical order (AA_ORDER) for consistent display
        sorted_aa_keys = sorted(aa_group_bounds.keys(), key=lambda aa: AA_ORDER.index(aa) if aa in AA_ORDER else float('inf'))
        for aa_1_letter in sorted_aa_keys:
            bounds = aa_group_bounds[aa_1_letter]
            if aa_1_letter in AA_1_TO_3 and 'mid' in bounds and pd.notna(bounds['mid']):
                aa_ticks.append(float(bounds['mid'])) # Position the tick at the midpoint of the AA group
                aa_labels_3_letter.append(AA_1_TO_3[aa_1_letter]) # Use 3-letter AA code for label

        if aa_ticks and aa_labels_3_letter:
            ax2.set_xticks(aa_ticks)
            ax2.set_xticklabels(aa_labels_3_letter, fontsize=10, fontweight='bold')
        else: # If no AA ticks/labels, hide them
            ax2.set_xticks([])
            ax2.set_xticklabels([])

        # Style the secondary axis to be clean (no ticks, no spines)
        ax2.tick_params(axis='x', which='both', length=0, top=False, labeltop=True)
        for spine in ax2.spines.values(): spine.set_visible(False)

        # Adjust layout to prevent labels/titles from overlapping
        plt.tight_layout(rect=[0, 0.03, 1, 0.97]) # Adjust layout slightly to make space for top labels

        # Save the plot
        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"RSCU boxplot saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during RSCU boxplot generation for '{gene_name}': {data_err}")
    except Exception as e:
        logger.exception(f"Error generating RSCU boxplot for '{gene_name}': {e}")
    finally:
        if fig is not None: plt.close(fig)


# --- plot_correlation_heatmap (already refactored in previous example, included again for completeness) ---
def plot_correlation_heatmap(
    df: pd.DataFrame,
    features: List[str],
    output_filepath: str,
    method: str = 'spearman'
) -> None:
    """
    Generates a heatmap of the correlation matrix for a specified list of features
    within a DataFrame. This visualizes the pairwise relationships between features.

    Args:
        df (pd.DataFrame): The input DataFrame containing the features for which
                           correlations are to be calculated.
        features (List[str]): A list of column names (features) from the DataFrame
                              to include in the correlation matrix.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/feature_correlation_heatmap.svg').
        method (str): The correlation method to use. Can be 'spearman' (Spearman's rank
                      correlation) or 'pearson' (Pearson's linear correlation).
                      Defaults to 'spearman'.
    """
    if df is None or df.empty:
         logger.warning("Input DataFrame is empty. Cannot plot correlation heatmap.")
         return

    available_features = [f for f in features if f in df.columns]
    if len(available_features) < 2:
         logger.warning(f"Need at least two available features for correlation. Found: {available_features}. Skipping heatmap.")
         return

    if method not in ['spearman', 'pearson']:
        logger.warning(f"Invalid correlation method '{method}'. Using 'spearman'.")
        method = 'spearman'

    fig: Optional[Figure] = None
    try:
        # Select data and ensure numeric, drop rows with NaNs in selected columns
        corr_data = df[available_features].copy()
        for col in available_features:
             corr_data[col] = pd.to_numeric(corr_data[col], errors='coerce')
        corr_data.dropna(inplace=True)

        if len(corr_data) < 2:
             logger.warning("Not enough data rows remaining after handling NaNs for correlation heatmap.")
             return
        if corr_data.shape[1] < 2: # Check if enough columns remain
             logger.warning("Not enough valid feature columns remaining after handling NaNs for correlation heatmap.")
             return

        # Calculate correlation matrix
        corr_matrix = corr_data.corr(method=method)

        # Plot heatmap
        fig_width = max(8, len(available_features) * 0.9)
        fig_height = max(6, len(available_features) * 0.7)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        sns.heatmap(
            corr_matrix,
            annot=True, cmap='coolwarm', fmt=".2f",
            linewidths=.5, linecolor='lightgray', cbar=True,
            square=False, annot_kws={"size": 8}, ax=ax
        )
        ax.set_title(f'{method.capitalize()} Correlation Between Features', fontsize=14)
        x_fontsize = 9 if len(available_features) < 15 else 7
        y_fontsize = 9 if len(available_features) < 15 else 7
        ax.tick_params(axis='x', rotation=45, labelsize=x_fontsize)
        ax.tick_params(axis='y', rotation=0, labelsize=y_fontsize)
        plt.tight_layout()

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"Feature correlation heatmap saved to: {output_path_obj}")

    except (ValueError, TypeError, KeyError) as data_err:
        logger.error(f"Data error during correlation heatmap generation: {data_err}")
    except Exception as e:
        logger.exception(f"Error generating correlation heatmap: {e}")
    finally:
        if fig is not None: plt.close(fig)

def plot_ca_axes_feature_correlation(
    ca_dims_df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    rscu_df: pd.DataFrame,
    output_filepath: str,
    significance_threshold: float = 0.05,
    method_name: str = "Spearman",
    features_to_correlate: Optional[List[str]] = None
    ) -> None:
    """
    Generates a heatmap showing the correlation coefficients between Correspondence Analysis (CA)
    axes (e.g., Dim1, Dim2) and other calculated sequence features (metrics and RSCU values).
    Significant correlations (based on a p-value threshold) are highlighted with an asterisk.

    This plot helps to interpret the biological meaning of the CA dimensions by identifying
    which sequence properties or codon usage patterns are strongly associated with each axis.

    Args:
        ca_dims_df (pd.DataFrame): DataFrame containing the CA dimension coordinates for each
                                   sequence/gene. Expected columns are 'CA_Dim1', 'CA_Dim2', etc.,
                                   and its index should uniquely identify sequences/genes
                                   (e.g., 'gene__sequenceID').
        metrics_df (pd.DataFrame): DataFrame containing various per-sequence metrics (e.g., GC%, ENC, CAI).
                                   Its index should align with `ca_dims_df` and `rscu_df`.
        rscu_df (pd.DataFrame): DataFrame containing per-sequence RSCU values, with codons as columns.
                                Its index should align with `ca_dims_df` and `metrics_df`.
        output_filepath (str): Full path (including filename and extension) where the plot
                               will be saved (e.g., 'plots/ca_feature_correlation_heatmap.svg').
        significance_threshold (float): The p-value threshold below which a correlation is
                                        considered statistically significant and marked with an asterisk.
                                        Defaults to 0.05.
        method_name (str): The name of the correlation method used (e.g., "Spearman", "Pearson").
                           This is used in the plot title and for logging. Defaults to "Spearman".
        features_to_correlate (Optional[List[str]]): A specific list of feature names (column names)
                                                     from `metrics_df` and `rscu_df` to correlate
                                                     against the CA axes. If None, a sensible default
                                                     set of common metrics and all RSCU codons will be used.
                                                     Defaults to None.
    """
    if ca_dims_df is None or ca_dims_df.empty:
        logger.warning("CA dimensions DataFrame is missing or empty. Cannot plot CA-Feature correlation.")
        return
    if metrics_df is None or metrics_df.empty:
        logger.warning("Metrics DataFrame is missing or empty. Cannot plot CA-Feature correlation.")
        return
    if rscu_df is None or rscu_df.empty:
        logger.warning("RSCU DataFrame is missing or empty. Cannot plot CA-Feature correlation.")
        return

    # --- Validate input DataFrames and their indices ---
    # Ensure indices are unique for reliable merging
    if not ca_dims_df.index.is_unique:
        logger.error("Index of CA dimensions DataFrame is not unique. Aborting correlation plot.")
        return
    if not metrics_df.index.is_unique:
        logger.error("Index of metrics DataFrame is not unique. Aborting correlation plot.")
        return
    if not rscu_df.index.is_unique:
        logger.error("Index of RSCU DataFrame is not unique. Aborting correlation plot.")
        return

    fig: Optional[Figure] = None
    try:
        # --- Merge DataFrames robustly ---
        logger.debug(f"Initial shapes: CA_dims({ca_dims_df.shape}), Metrics({metrics_df.shape}), RSCU({rscu_df.shape})")

        # Find common indices across all three DataFrames to ensure data alignment
        common_index = ca_dims_df.index.intersection(metrics_df.index).intersection(rscu_df.index)

        if common_index.empty:
            logger.error("No common indices found between CA dimensions, metrics, and RSCU DataFrames. Cannot merge for correlation plot.")
            return

        logger.info(f"Found {len(common_index)} common entries for merging CA dimensions, metrics, and RSCU data.")

        # Align all DataFrames to the common index before concatenating
        ca_dims_aligned = ca_dims_df.loc[common_index]
        metrics_aligned = metrics_df.loc[common_index]
        rscu_aligned = rscu_df.loc[common_index]

        # Concatenate metrics and RSCU data horizontally (axis=1) as they now share the same index.
        # This assumes no overlapping column names between metrics_aligned and rscu_aligned,
        # or that any overlaps are handled appropriately (e.g., by pandas' default behavior).
        metric_cols = set(metrics_aligned.columns)
        rscu_cols = set(rscu_aligned.columns)
        overlapping_cols_mr = metric_cols.intersection(rscu_cols)
        if overlapping_cols_mr:
            logger.warning(f"Overlapping columns found between metrics and RSCU data: {overlapping_cols_mr}. These might cause issues or be overwritten during merge.")

        merged_df_features = pd.concat([metrics_aligned, rscu_aligned], axis=1)

        # Now merge the combined features DataFrame with the CA dimensions DataFrame.
        # Critical check for column name conflicts between features and CA dimensions.
        features_cols = set(merged_df_features.columns)
        ca_dim_cols = set(ca_dims_aligned.columns)
        overlapping_cols_fc = features_cols.intersection(ca_dim_cols)
        if overlapping_cols_fc:
             logger.error(f"Critical: Overlapping columns found between features and CA dimensions: {overlapping_cols_fc}. Aborting plot.")
             return

        merged_df = pd.concat([ca_dims_aligned, merged_df_features], axis=1)

        if merged_df.empty:
            logger.error("Merged DataFrame for CA-Feature correlation is empty. This should not happen if common_index was found. Aborting.")
            return

        logger.info(f"Successfully merged data for correlation, final shape: {merged_df.shape}")

        # --- Define features to correlate ---
        if features_to_correlate is None:
            # If no specific features are provided, use a default set of common metrics and all RSCU codons.
            default_metric_features = ['Length', 'TotalCodons', 'GC', 'GC1', 'GC2', 'GC3', 'GC12',
                                       'ENC', 'CAI', 'Fop', 'RCDI', 'ProteinLength', 'GRAVY', 'Aromaticity']
            # Filter default metrics to include only those actually present in the merged DataFrame
            available_metric_features = [f for f in default_metric_features if f in merged_df.columns]
            # Identify all RSCU columns (assumed to be 3-letter uppercase codons) from the aligned RSCU data
            available_rscu_columns = sorted([col for col in rscu_aligned.columns if len(col) == 3 and col.isupper()])
            features_to_correlate = available_metric_features + available_rscu_columns
        else:
            # If a list is provided, filter it to ensure all requested features exist in the merged DataFrame.
            original_feature_count = len(features_to_correlate)
            features_to_correlate = [f for f in features_to_correlate if f in merged_df.columns]
            if len(features_to_correlate) < original_feature_count:
                logger.warning("Some requested features for correlation were not found in the merged data and were skipped.")

        if not features_to_correlate:
            logger.error("No valid features selected or available for CA-Feature correlation. Aborting plot.")
            return

        # Identify CA dimension columns (assuming they are the columns from ca_dims_aligned)
        ca_dim_column_names = list(ca_dims_aligned.columns)
        if not ca_dim_column_names:
            logger.error("No CA dimension columns found in ca_dims_df. Aborting plot.")
            return

        # --- Calculate Correlations (coefficients and p-values) ---
        logger.info(f"Calculating {method_name} correlations for {len(ca_dim_column_names)} CA Axes vs {len(features_to_correlate)} features...")
        all_corr_coeffs: Dict[str, Dict[str, float]] = {}
        all_p_values: Dict[str, Dict[str, float]] = {}

        if not SCIPY_AVAILABLE: # Check if SciPy library is available for p-value calculation
            logger.warning(f"Scipy not installed. Cannot calculate p-values for {method_name} correlations. Heatmap will show coefficients only.")
            # Fallback: calculate correlations using pandas if scipy is not available
            corr_matrix_full = merged_df[ca_dim_column_names + features_to_correlate].corr(method=method_name.lower())
            corr_matrix_subset = corr_matrix_full.loc[ca_dim_column_names, features_to_correlate]
            pval_matrix_subset = pd.DataFrame(np.nan, index=corr_matrix_subset.index, columns=corr_matrix_subset.columns) # P-values will be NaN
        else:
            for ca_dim_col in ca_dim_column_names:
                all_corr_coeffs[ca_dim_col] = {}
                all_p_values[ca_dim_col] = {}
                ca_dim_data = merged_df[ca_dim_col]
                for feature in features_to_correlate:
                    feature_data = merged_df[feature]
                    # Identify common non-NaN data points for correlation calculation
                    common_mask = ca_dim_data.notna() & feature_data.notna()
                    n_common = common_mask.sum()

                    # Skip correlation if insufficient data points or no variation
                    if n_common < 3 or feature_data[common_mask].nunique() <= 1 or ca_dim_data[common_mask].nunique() <= 1 :
                        all_corr_coeffs[ca_dim_col][feature] = np.nan
                        all_p_values[ca_dim_col][feature] = np.nan
                        continue
                    try:
                        # Perform correlation calculation based on the specified method
                        if method_name.lower() == 'spearman':
                            corr, pval = scipy_stats_module.spearmanr(ca_dim_data[common_mask], feature_data[common_mask])
                        elif method_name.lower() == 'pearson':
                            corr, pval = scipy_stats_module.pearsonr(ca_dim_data[common_mask], feature_data[common_mask])
                        else:
                            logger.warning(f"Unsupported correlation method '{method_name}'. Defaulting to Spearman.")
                            corr, pval = scipy_stats_module.spearmanr(ca_dim_data[common_mask], feature_data[common_mask])
                        all_corr_coeffs[ca_dim_col][feature] = corr
                        all_p_values[ca_dim_col][feature] = pval
                    except ValueError as spe_err:
                        logger.warning(f"Could not calculate {method_name} correlation for {ca_dim_col} vs '{feature}': {spe_err}")
                        all_corr_coeffs[ca_dim_col][feature] = np.nan
                        all_p_values[ca_dim_col][feature] = np.nan

            # Convert dictionaries of correlations and p-values to DataFrames
            corr_matrix_subset = pd.DataFrame.from_dict(all_corr_coeffs, orient='index')
            pval_matrix_subset = pd.DataFrame.from_dict(all_p_values, orient='index')
            # Reorder columns to match the desired features_to_correlate order
            if not corr_matrix_subset.empty:
                corr_matrix_subset = corr_matrix_subset.reindex(columns=features_to_correlate)
            if not pval_matrix_subset.empty:
                pval_matrix_subset = pval_matrix_subset.reindex(columns=features_to_correlate)


        if corr_matrix_subset.empty:
            logger.error("Correlation matrix is empty. Cannot generate heatmap.")
            return

        # --- Plotting ---
        # Dynamically adjust figure size based on the number of features to plot
        n_features_plot = len(corr_matrix_subset.columns)
        fig_height = max(4, len(corr_matrix_subset.index) * 0.8)
        fig_width = max(10, n_features_plot * 0.4)
        fig_width = min(fig_width, 45) # Cap max width to prevent excessively large figures

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        # Create annotation data: add '*' for significant correlations
        annot_mask = pval_matrix_subset < significance_threshold
        annot_data = np.where(
            annot_mask,
            corr_matrix_subset.round(2).astype(str) + "*", # Add '*' for significant values
            "" # Show empty string for non-significant values
        )

        # Define a diverging color palette for correlations
        cmap = sns.diverging_palette(240, 10, s=99, l=50, as_cmap=True)

        sns.heatmap(
            corr_matrix_subset, # Use the correctly ordered subset of correlation coefficients
            annot=annot_data, # Use the custom annotation data
            fmt="", # Format as string since annot_data is already formatted
            cmap=cmap,
            linewidths=.5,
            linecolor='lightgray',
            cbar=True,
            center=0, # Center the colormap at 0 for correlations
            vmin=-1, vmax=1, # Ensure full range for correlation coefficients
            annot_kws={"size": 7},
            cbar_kws={'label': f'{method_name} Correlation Coefficient', 'shrink': 0.7},
            ax=ax
        )

        ax.set_title(f'{method_name} Correlation: CA Axes vs Features (p < {significance_threshold} marked with *)', fontsize=14)
        ax.set_xlabel("Features", fontsize=12)
        ax.set_ylabel("CA Axes", fontsize=12)

        # Adjust x-tick label font size based on number of features to prevent overlap
        xtick_fontsize = 8 if n_features_plot < 50 else (6 if n_features_plot < 80 else 5)
        plt.xticks(rotation=90, ha='right', fontsize=xtick_fontsize) # Rotate for readability
        plt.yticks(rotation=0, fontsize=10) # Keep y-ticks horizontal

        # Adjust layout to prevent elements from being cut off, especially with rotated labels
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        output_path_obj = Path(output_filepath)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
        plt.savefig(output_path_obj, dpi=300, bbox_inches='tight')
        logger.info(f"CA Axes vs Features correlation heatmap saved to: {output_path_obj}")

    except Exception as e:
        logger.exception(f"Error generating CA Axes vs Features correlation heatmap: {e}")
    finally:
        if fig is not None:
            plt.close(fig)


# --- [Optional] plot_rscu_distribution_per_gene ---
# This function might be redundant if plot_rscu_boxplot_per_gene is preferred.
# If kept, it needs the same refactoring treatment: logging, try/except, type hints, plt.close().
# def plot_rscu_distribution_per_gene(...) -> None: ...