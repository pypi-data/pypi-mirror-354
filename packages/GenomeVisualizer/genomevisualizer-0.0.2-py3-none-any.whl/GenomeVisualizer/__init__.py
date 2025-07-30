from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("GenomeVisualizer")
except PackageNotFoundError:
    __version__ = "0.0.2"

from .basic import load_genome_from_txt, FrequencyMap, FrequentWords
from .motifs import Count, Profile, Consensus, Score, Pr, ProfileMostProbableKmer, GreedyMotifSearch, CountWithPseudocounts, ProfileWithPseudocounts, GreedyMotifSearchWithPseudocounts, Motifs, RandomMotifs, RandomizedMotifSearch, Normalize, WeightedDie, ProfileGeneratedString, GibbsSampler
from .replication import PatternCount, Reverse, Complement, ReverseComplement, PatternMatching, FasterSymbolArray, SkewArray, MinimumSkew, HammingDistance, ApproximatePatternMatching, ApproximatePatternCount
from .visualization import plot_symbol_array, plot_skew_array_with_ori, plot_motiflogo

__all__ = [
    # Basic
    "FrequencyMap", "FrequentWords","load_genome_from_txt",
    # Motifs
    "Count", "Profile", "Consensus", "Score", "Pr", "ProfileMostProbableKmer",
    "GreedyMotifSearch", "CountWithPseudocounts", "ProfileWithPseudocounts",
    "GreedyMotifSearchWithPseudocounts", "Motifs", "RandomMotifs",
    "RandomizedMotifSearch", "Normalize", "WeightedDie",
    "ProfileGeneratedString", "GibbsSampler",
    # Replication
    "PatternCount", "Reverse", "Complement", "ReverseComplement",
    "PatternMatching", "FasterSymbolArray", "SkewArray", "MinimumSkew",
    "HammingDistance", "ApproximatePatternMatching", "ApproximatePatternCount",
    # Visualization
    "plot_symbol_array", "plot_skew_array_with_ori","plot_motiflogo",
    # Meta
    "__version__",
]