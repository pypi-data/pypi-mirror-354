from .basic import MinPositions


def PatternCount(Text: str, Pattern: str) -> int:
    """
    Counts the number of exact occurrences of a pattern in a given DNA sequence.

    This function uses a sliding window approach to iterate through the input DNA text 
    and counts how many times the exact pattern appears.

    Args:
        Text (str): DNA sequence in which the pattern is searched.
        Pattern (str): DNA pattern to find within the sequence.

    Returns:
        int: Number of times the pattern occurs exactly in the sequence.

    Example:
        >>> PatternCount("ATATAT", "ATA")
        2
    """
    count = 0
    for i in range(len(Text)-len(Pattern)+1):
        if Text[i:i+len(Pattern)] == Pattern:
            count = count+1
    return count

def Reverse(Pattern: str) -> str:
    """
    Reverses the given DNA pattern.

    This function returns the reverse of the input DNA sequence by reversing the order of its characters.

    Args:
        Pattern (str): DNA sequence to be reversed.

    Returns:
        str: The reversed DNA sequence.

    Example:
        >>> Reverse("ATCG")
        "GCTA"
    """
    rev = ""
    for char in Pattern:
        rev = char + rev
    return rev

def Complement(Pattern: str) -> str:
    """
    Returns the complementary DNA strand of the given pattern.

    This function substitutes each nucleotide in the input DNA sequence with its Watson-Crick complement:
    A ↔ T, C ↔ G.

    Args:
        Pattern (str): DNA sequence consisting of characters 'A', 'T', 'C', and 'G'.

    Returns:
        str: The complementary DNA sequence.

    Example:
        >>> Complement("ATCG")
        "TAGC"
    """
    comp = ""
    for char in Pattern:
        if(char == 'T'):
            comp = comp + 'A'
        if(char == 'A'):
            comp = comp + 'T'
        if(char == 'C'):
            comp = comp + 'G'
        if(char == 'G'):
            comp = comp + 'C'
    return comp

def ReverseComplement(Pattern: str) -> str:
    """
    Computes the reverse complement of a DNA sequence.

    This function first reverses the input DNA sequence, then replaces each nucleotide
    with its Watson-Crick complement: A ↔ T, C ↔ G.

    Args:
        Pattern (str): DNA sequence to be reverse-complemented.

    Returns:
        str: The reverse complement of the input sequence.

    Example:
        >>> ReverseComplement("ATCG")
        "CGAT"
    """
    Pattern = Reverse(Pattern) # reverse all letters in a string
    Pattern = Complement(Pattern) # complement each letter in a string
    return Pattern

def PatternMatching(Pattern: str, Genome: str) -> list[int]:
    """
    Finds all starting positions where a given pattern appears exactly in a genome.

    This function searches the genome string for exact matches of the input pattern 
    and returns a list of all starting indices where the match occurs.

    Args:
        Pattern (str): DNA pattern to search for.
        Genome (str): DNA sequence in which to search for the pattern.

    Returns:
        list[int]: List of starting positions where the pattern occurs.

    Example:
        >>> PatternMatching("ATG", "ATGCATGATG")
        [0, 4, 7]
    """
    positions = []
    for i in range(len(Genome)-len(Pattern)+1):
        if Genome[i:i+len(Pattern)] == Pattern:
            positions.append(i)
    return positions

def FasterSymbolArray(Genome: str, symbol: str) -> dict[int, int]:
    """
    Efficiently computes the symbol frequency array over a sliding window of size n/2.

    This optimized version of SymbolArray avoids redundant computations by using a 
    sliding window approach. Instead of recomputing the number of occurrences of the 
    symbol from scratch for each window, it updates the count by considering only the 
    symbol that exits the window and the one that enters it. This reduces the time 
    complexity from O(n^2) to O(n), making it suitable for long genomes.

    Args:
        Genome (str): The DNA sequence to analyze.
        symbol (str): The nucleotide symbol ('A', 'C', 'G', or 'T') to count.

    Returns:
        dict[int, int]: A dictionary where keys are starting positions and values are 
        the counts of the symbol in the corresponding window.

    Example:
        >>> FasterSymbolArray("AAAAGGGG", "A")
        {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 1, 6: 2, 7: 3}

    Notes:
        - The sliding window is of length n/2.
        - The genome is virtually extended by its first n/2 characters to handle wrapping.
    """
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n//2]

    # look at the first half of Genome to compute first array value
    array[0] = PatternCount(Genome[0:n//2], symbol)

    for i in range(1, n):
        # start by setting the current array value equal to the previous array value
        array[i] = array[i-1]

        # the current array value can differ from the previous array value by at most 1
        if ExtendedGenome[i-1] == symbol:
            array[i] = array[i]-1
        if ExtendedGenome[i+(n//2)-1] == symbol:
            array[i] = array[i]+1
    return array

def SkewArray(Genome: str) -> list[int]:
    """
    Computes the skew array of a DNA genome.

    The skew array records the difference between the cumulative counts of 
    'G' and 'C' nucleotides at each position in the genome. It starts at 0 and 
    increments by +1 for every 'G', -1 for every 'C', and remains unchanged for 
    other nucleotides (e.g., 'A' or 'T').

    This array is particularly useful for identifying the origin of replication, 
    as the minimum point typically corresponds to the location of the ori.

    Args:
        Genome (str): The DNA sequence to analyze.

    Returns:
        list[int]: A list of skew values, one for each position from 0 to len(Genome).

    Example:
        >>> SkewArray("CAGTGC")
        [0, -1, -1, 0, 1, 1, 0]
    """
    skew = [0]
    for i in range(len(Genome)):
        if Genome[i] == "C":
            skew.append(skew[-1] - 1)
        elif Genome[i] == "G":
            skew.append(skew[-1] + 1)
        else:
            skew.append(skew[-1])
    return skew

def MinimumSkew(Genome: str) -> list[int]:
    """
    Identifies all positions in the genome where the skew array reaches its minimum value.

    This function computes the skew array of the genome and returns all indices where 
    the skew is minimal. These positions are biologically significant, as the origin of 
    replication (ori) often occurs near the minimum skew point.

    Args:
        Genome (str): The DNA sequence to analyze.

    Returns:
        list[int]: A list of genome positions where the skew is minimal.

    Example:
        >>> MinimumSkew("TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT")
        [11, 24]
    """
    positions = []
    skew = SkewArray(Genome)
    return MinPositions(skew)

def HammingDistance(p: str, q: str) -> int:
    """
    Computes the Hamming distance between two DNA strings.

    The Hamming distance is defined as the number of positions at which the 
    corresponding symbols are different. It is commonly used to measure the 
    similarity between two sequences of equal length.

    Args:
        p (str): First DNA string.
        q (str): Second DNA string, must be the same length as `p`.

    Returns:
        int: The number of differing positions between the two strings.

    Raises:
        ValueError: If the input strings are not of equal length.

    Example:
        >>> HammingDistance("GGGCCGTTGGT", "GGACCGTTGAC")
        3
    """
    if len(p) != len(q):
        raise ValueError("Strings must be of equal length to compute Hamming distance.")
    count = 0
    for i in range(len(p)):
        if(p[i] != q[i]):
            count+=1
    return count

def ApproximatePatternMatching(Text: str, Pattern: str, d: int) -> list[int]:
    """
    Finds all starting positions where a pattern appears in a text with at most d mismatches.

    This function performs approximate pattern matching by sliding the pattern over the text 
    and computing the Hamming distance at each position. All positions where the distance 
    is less than or equal to `d` are returned.

    Args:
        Text (str): The DNA sequence in which to search for the pattern.
        Pattern (str): The DNA pattern to search for.
        d (int): Maximum number of allowed mismatches (Hamming distance threshold).

    Returns:
        list[int]: A list of starting positions where the pattern appears with ≤ d mismatches.

    Example:
        >>> ApproximatePatternMatching("CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT", "ATTCTGGA", 3)
        [6, 7, 26 27]
    """
    positions = []
    for i in range(len(Text)-len(Pattern)+1):
        distance = HammingDistance(Text[i:i+len(Pattern)], Pattern)
        if distance <= d:
            positions.append(i)
    return positions

def ApproximatePatternCount(Pattern: str, Text: str, d: int) -> int:
    """
    Counts the number of times a pattern appears in a text with at most d mismatches.

    This function scans the text for substrings that approximately match the pattern,
    allowing for up to `d` mismatches based on Hamming distance, and returns how many such matches exist.

    Args:
        Pattern (str): The DNA pattern to search for.
        Text (str): The DNA sequence in which to search.
        d (int): Maximum number of allowed mismatches.

    Returns:
        int: The total number of approximate occurrences of the pattern.

    Example:
        >>> ApproximatePatternCount("GAGG", "TTTAGAGCCTTCAGAGG", 2)
        4
    """
    count = 0
    for i in range(len(Text)-len(Pattern)+1):
        distance = HammingDistance(Text[i:i+len(Pattern)], Pattern)
        if distance <= d:
            count = count+1
    return count
