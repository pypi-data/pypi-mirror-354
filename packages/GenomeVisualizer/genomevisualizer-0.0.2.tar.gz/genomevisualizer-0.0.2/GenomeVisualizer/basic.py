def load_genome_from_txt(filepath: str) -> str:
    """
    Loads a genome sequence from a plain text (.txt) file.

    This function reads the entire content of a text file and removes any 
    whitespace or newline characters, returning a continuous DNA string.

    Args:
        filepath (str): Path to the genome file (must be a .txt file containing ACGT characters).

    Returns:
        str: A cleaned DNA sequence as a single string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is empty or contains invalid characters.

    Example:
        >>> genome = load_genome_from_txt("data/ecoli.txt")
        >>> genome[:10]
        'AGCTTTTCAT'
    """
    with open(filepath, "r") as file:
        content = file.read().replace("\n", "").replace(" ", "").upper()

    if not content:
        raise ValueError("The file is empty.")
    if not set(content).issubset({"A", "C", "G", "T"}):
        raise ValueError("The file contains invalid DNA characters.")

    return content

def FrequencyMap(Text: str, k: int) -> dict[str, int]:
    """
    Computes the frequency of all k-length substrings (k-mers) in a DNA sequence.

    This function counts how many times each k-mer appears in the input DNA sequence 
    using a sliding window. The output is a dictionary where each key is a unique 
    k-mer, and the value is the number of occurrences.

    Args:
        Text (str): The DNA sequence to scan.
        k (int): Length of the k-mers to count.

    Returns:
        dict[str, int]: A dictionary mapping each k-mer to its count in the sequence.

    Example:
        >>> FrequencyMap("ATATA", 3)
        {'ATA': 2, 'TAT': 1}
    """
    freq = {}
    n = len(Text)
    for i in range(n-k+1):
        Pattern = Text[i:i+k]
        freq[Pattern] = 0
    for i in range(n-k+1):
        Pattern = Text[i:i+k]
        freq[Pattern] += 1
    return freq

def FrequentWords(Text: str, k: int) -> list[str]:
    """
    Identifies the most frequent k-length substrings (k-mers) in a DNA sequence.

    This function uses FrequencyMap to find all k-mers in the sequence and then 
    returns those that occur with the highest frequency.

    Args:
        Text (str): The DNA sequence to search.
        k (int): Length of the k-mers.

    Returns:
        list[str]: A list of k-mers with the highest frequency in the sequence.

    Example:
        >>> FrequentWords("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4)
        ['CATG', 'GCAT']
    """
    words = []
    freq = FrequencyMap(Text, k)
    m = max(freq.values())
    for key in freq:
        # add each key to words whose corresponding frequency value is equal to m
        if(freq.get(key) == m):
            words.append(key)
    return words


def MinPositions(values: list[int]) -> list[int]:
    """
    Given a list of numbers, return all indices in the list that contain the minimum value.
    """
    positions = []
    mn = min(values)
    for i in range(len(values)):
        if values[i] == mn:
            positions.append(i)
    return positions
