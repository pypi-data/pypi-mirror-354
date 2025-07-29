import random

def Count(Motifs):
    count = {}
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(0)
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def Profile(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = {}
    profile = Count(Motifs)
    for i in profile:
        for j in range(k):
            profile[i][j]/=t
    return profile

def Consensus(Motifs):
    k = len(Motifs[0])
    count = Count(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

def Score(Motifs):
    consensus=Consensus(Motifs)
    score = 0
    k = len(Motifs[0])
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            if Motifs[i][j] != consensus[j]:
                score += 1
    return score

def Pr(Text, Profile):
    p = 1
    for i in range(len(Text)):
        p=p*Profile[Text[i]][i]
    return p

def ProfileMostProbableKmer(text, k, profile):
    most_probable=""
    most_probable_value=-1
    for i in range(len(text)-k+1):
        k_mer=text[i:(i+k)]
        k_mer_probability=Pr(k_mer, profile)
        if(k_mer_probability > most_probable_value):
            most_probable_value = k_mer_probability
            most_probable = k_mer
    return most_probable

def GreedyMotifSearch(Dna, k, t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
        
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = Profile(Motifs[0:j])
            Motifs.append(ProfileMostProbableKmer(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
                BestMotifs = Motifs
            
    return BestMotifs

def CountWithPseudocounts(Motifs):
    count = {}
    t = len(Motifs)
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(1)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = {}
    profile = CountWithPseudocounts(Motifs)
    for i in profile:
        for j in range(k):
            profile[i][j]/=(t+4)
    return profile

def GreedyMotifSearchWithPseudocounts(Dna, k, t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
        
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = ProfileWithPseudocounts(Motifs[0:j])
            Motifs.append(ProfileMostProbableKmer(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
                BestMotifs = Motifs
            
    return BestMotifs

def Motifs(Profile, Dna):
    n = len(Dna[0])
    k= len(Profile["A"])
    P = Profile
    Motifs = []
    for j in range(0, len(Dna)):
        Motifs.append(ProfileMostProbableKmer(Dna[j], k, P))
    return Motifs

def RandomMotifs(Dna, k, t):
    Motifs = []
    for j in range(0, t):
        r=random.randint(0, len(Dna[j])-k)
        Motifs.append(Dna[j][r:r+k])
    
    return Motifs

def RandomizedMotifSearch(Dna, k, t):
    M = RandomMotifs(Dna, k, t)
    BestMotifs = M
    
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs
        
def Normalize(Probabilities):
    sum_of_values = sum(Probabilities.values())
    for symbol in Probabilities:
        Probabilities[symbol]=Probabilities[symbol]/sum_of_values
    return Probabilities

def WeightedDie(Probabilities):
    kmer = ''
    p = random.uniform(0,1)
    sum=0
    for kmer in Probabilities:
        sum=sum+Probabilities[kmer]
        if p < sum:
            return kmer
        
def ProfileGeneratedString(Text, profile, k):
    n = len(Text)
    probabilities = {}
    
    for i in range(0,n-k+1):
        probabilities[Text[i:i+k]] = Pr(Text[i:i+k], profile)
        
    probabilities = Normalize(probabilities)
    return WeightedDie(probabilities)

def GibbsSampler(Dna, k, t, N):
    BestMotifs = []
    Motifs = RandomMotifs(Dna, k, t)
    BestMotifs = Motifs
    for j in range(N):
        i = random.randint(1,t)
        text=Motifs.pop(i-1)
        profile=ProfileWithPseudocounts(Motifs)
        kmer=ProfileMostProbableKmer(text, k, profile)
        Motifs.insert(i-1, kmer)
        if(Score(Motifs) < Score(BestMotifs)):
            BestMotifs = Motifs
    return BestMotifs