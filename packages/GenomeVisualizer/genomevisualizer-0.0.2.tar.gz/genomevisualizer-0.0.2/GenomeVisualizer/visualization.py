import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logomaker
from GenomeVisualizer.motifs import Profile

def plot_symbol_array_impl(symbol_array: dict[int, int], symbol: str, genome_label: str = "genome") -> plt.Figure:
    """See plot_symbol_array"""
    positions = list(symbol_array.keys())
    counts = list(symbol_array.values())

    fig = plt.figure(figsize=(10, 5))
    plt.plot(positions, counts, color="blue")
    plt.xlabel("genome position")
    plt.ylabel(f"count of {symbol} in half-genome starting at given position")
    plt.title(f"Symbol array for {genome_label} (symbol = '{symbol}')")
    plt.grid(True)
    plt.tight_layout()
    return fig

def plot_symbol_array(symbol_array: dict[int, int], symbol: str, genome_label: str = "genome") -> None:
    """
    Plots the symbol frequency array across the genome.

    This function visualizes the number of occurrences of a specified nucleotide 
    in a sliding window (typically of size genome_length/2), showing variation 
    in composition across the genome.

    Args:
        symbol_array (dict[int, int]): Dictionary mapping genome positions to the count of a symbol in the sliding window.
        symbol (str): The nucleotide symbol ('A', 'C', 'G', or 'T') used for counting.
        genome_label (str, optional): Label for the genome, used in the figure title. Default is "genome".

    Returns:
        None: The function displays the plot using matplotlib.

    Example:
        >>> arr = FasterSymbolArray(genome, 'C')
        >>> plot_symbol_array(arr, 'C', genome_label="E. coli")
    """
    plot_symbol_array_impl(symbol_array, symbol, genome_label)
    plt.show()

def plot_skew_array_with_ori_impl(skew: list[int], ori_positions: list[int], genome_label: str = "genome") -> plt.Figure:
    """
    Plots the skew array and highlights the estimated origin(s) of replication.

    Args:
        skew (list[int]): Skew values computed across the genome.
        ori_positions (list[int]): Positions where the skew reaches its minimum (possible ori sites).
        genome_label (str, optional): Name of the genome to show in the title. Default is "genome".

    Returns:
        None: The function displays the plot using matplotlib.

    Example:
        >>> skew = SkewArray(genome)
        >>> ori_pos = MinimumSkew(genome)
        >>> plot_skew_array_with_ori(skew, ori_pos, genome_label="E. coli")
    """
    fig = plt.figure(figsize=(10, 5))
    plt.plot(range(len(skew)), skew, label="Skew", color="darkgreen")
    plt.scatter(ori_positions, [skew[pos] for pos in ori_positions], color="red", label="Minimum skew (ori?)")
    plt.xlabel("Genome position")
    plt.ylabel("Skew (G - C)")
    plt.title(f"Skew array for {genome_label}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return fig

def plot_skew_array_with_ori(skew: list[int], ori_positions: list[int], genome_label: str = "genome") -> None:
    """
    Plots the skew array and highlights the estimated origin(s) of replication.

    Args:
        skew (list[int]): Skew values computed across the genome.
        ori_positions (list[int]): Positions where the skew reaches its minimum (possible ori sites).
        genome_label (str, optional): Name of the genome to show in the title. Default is "genome".

    Returns:
        None: The function displays the plot using matplotlib.

    Example:
        >>> skew = SkewArray(genome)
        >>> ori_pos = MinimumSkew(genome)
        >>> plot_skew_array_with_ori(skew, ori_pos, genome_label="E. coli")
    """
    fig=plot_skew_array_with_ori_impl(skew, ori_positions,  "genome")
    fig.show()

def plot_motiflogo_impl(motifs: list[str], font_name='Arial Rounded MT Bold'):
    """see plot_motiflogo"""
    profile = Profile(motifs)
    k = len(motifs[0])

    # Compute entropy and information content
    entropy = []
    for i in range(k):
        H = 0
        for nt in "ACGT":
            p = profile[nt][i]
            if p > 0:
                H -= p * np.log2(p)
        entropy.append(H)

    info_content = [2 - h for h in entropy]

    # Construct bit matrix
    bit_matrix = {nt: [] for nt in "ACGT"}
    for nt in "ACGT":
        for i in range(k):
            bit_matrix[nt].append(profile[nt][i] * info_content[i])

    df = pd.DataFrame(bit_matrix)

    # Plot motif logo
    logo = logomaker.Logo(df, color_scheme='classic', font_name=font_name)
    logo.style_spines(visible=False)
    logo.style_spines(spines=['left', 'bottom'], visible=True)
    logo.ax.set_xlabel('Position', fontsize=14)
    logo.ax.set_ylabel('Bits', fontsize=14)
    logo.ax.set_title("Motif Logo", fontsize=16)
    logo.ax.set_xticks(list(range(k)))
    plt.tight_layout()
    return logo.fig

def plot_motiflogo(motifs: list[str]) -> None:
    """
    Plots a motif logo based on information content using Shannon entropy.

    This function generates a sequence logo from a list of motifs, where each letter's 
    height is proportional to its information content in bits. Highly conserved positions 
    produce taller symbols.

    Args:
        motifs (list[str]): A list of DNA strings (motifs) of equal length.

    Returns:
        None: Displays a motif logo plot using matplotlib.

    Example:
        >>> plot_motiflogo(["ATG", "ACG", "AAG", "AGG", "ATG"])
    """
    plot_motiflogo_impl(motifs)
    plt.show()
