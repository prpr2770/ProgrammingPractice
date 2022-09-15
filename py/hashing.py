"""
Implementation of Recursive Hashing by Cyclic Polynomials
"""
import random
import sys
import numpy as npy
import itertools
random.seed(0)

## 4-byte representation of each symbol
# random.randbytes(4)

class DefaultHash(object):
    id_iter = itertools.count()
    def __init__(self, s: str):
        self.word = s
        self.k_mer = len(self.word)
        self.id = next(DefaultHash.id_iter)
        # compute this
        self.hash_value = self.__hash__()

    def __hash__(self):
        return hash(self.word)
     
    def __eq__(self, other):
        """
        check_hash_value = ((self.hash_value == other.hash_value))
        check_word = ((self.word == other.word))
        check_id = ((self.id == other.id))
        """
        check_word = ((self.word == other.word))
        return check_word


class SelfAnnihilatingHash(object):
    id_iter = itertools.count()
    def __init__(self, s: str, T_encoder=None, Tprime_encoder=None, prev_key=None, removed_symbol=None, introduced_symbol=None ):
        self.word = s
        self.T_enc = T_encoder
        self.Tprime_enc = Tprime_encoder
        self.k_mer = len(self.word)
        self.delta = 1
        self.introduced_symbol = introduced_symbol
        self.removed_symbol = removed_symbol
        self.prev_key = prev_key
        self.id = next(SelfAnnihilatingHash.id_iter)

        # compute this
        self.hash_value = self.__hash__()


    def __hash__(self):
        if self.prev_key == None:
            hashWord = 0 
            for i in range(self.k_mer):
                hashWord = hashWord << self.delta
                hashWord = hashWord ^ self.T_enc[self.word[i]]
        else:
            hashWord = self.prev_key << self.delta
            hashWord = hashWord ^  self.T_enc[self.introduced_symbol]
            hashWord = hashWord ^ self.Tprime_enc[self.removed_symbol]

        return hashWord

     
    def __eq__(self, other):
        """
        check_hash_value = ((self.hash_value == other.hash_value))
        check_word = ((self.word == other.word))
        check_id = ((self.id == other.id))
        """
        check_word = ((self.word == other.word))
        return check_word
 

def read_from_strings(string1, string2, k):

    total_symbols = 0
    symbols = {}
    string3 = string1 + string2
    for achar in string3:
        if achar not in symbols.keys():
            symbols[achar] = 1
            total_symbols = total_symbols + 1

    

    T_encoder = {}
    Tprime_encoder = {}

    for achar in symbols.keys():
        anum = random.randint(0,2**32) #random.randint(4)
        T_encoder[achar] = anum
        Tprime_encoder[achar] = anum << k


    # ======================
    # CONSTURCTING DICTIONARY - FROM STRING-1

    # finding sub-strings 
    seg0 = string1[:k]
    segment0 = SelfAnnihilatingHash(s=seg0, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder)
    old_hashkey = segment0.hash_value

    segment_dict = {}
    segment_dict[segment0] = 0

    for start_indx in range(1,len(string1)-k+1):
        end_indx = start_indx + k - 1
        print("len:%d, start:%d, end:%d" %(len(string1), start_indx, end_indx))
        old_symbol = string1[start_indx - 1 ]
        new_symbol = string1[end_indx]
        seg = string1[start_indx:end_indx]
        segment = SelfAnnihilatingHash(s=seg, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder, prev_key=old_hashkey, removed_symbol=old_symbol, introduced_symbol=new_symbol ) 
        old_hashkey = segment.hash_value
        if segment not in segment_dict.keys(): 
            segment_dict[segment] = start_indx

    # ======================
    # DETECTING - COMMON SUBSTRINGS

    commons = []

    # finding sub-strings 
    seg0 = string2[:k]
    segment0 = SelfAnnihilatingHash(s=seg0, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder)
    old_hashkey = segment0.hash_value

    try: 
        src_indx = segment_dict[segment0]
        commons.append( (src_indx, 0) )
    except:
        pass

    for start_indx in range(1, len(string2)-k +1):
        end_indx = start_indx + k -1
        old_symbol = string2[start_indx -1]
        new_symbol = string2[end_indx]
        seg = string2[start_indx:end_indx]
        segment = SelfAnnihilatingHash(s=seg, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder, prev_key=old_hashkey, removed_symbol=old_symbol, introduced_symbol=new_symbol ) 
        old_hashkey = segment.hash_value
        try: 
            src_indx = segment_dict[segment]
            commons.append( (src_indx, start_indx) )
        except:
            pass
    return (commons, segment_dict)

def compute_symbol_alphabet(file1):
    total_symbols = 0
    alphabet = {}
    with open(file1, "r") as f:
        while True:
            achar = f.read(1)
            if not achar: 
                break
            if achar not in alphabet.keys():
                alphabet[achar] = 1
                total_symbols = total_symbols + 1

    return (total_symbols, alphabet)

def update_alphabet(sym, k, alphabet, total_symbols, T_encoder, Tprime_encoder):
    alphabet[sym] = 1
    total_symbols = total_symbols + 1
    anum = random.randint(0,2**32) #random.randint(4)
    # Ensure that the random-int doesn't exist in Table. 
    while( anum in T_encoder.values() ):
        anum = random.randint(0,2**32) #random.randint(4)
    T_encoder[sym] = anum
    Tprime_encoder[sym] = anum << k

def read_from_files_rolling(file1, file2, k):

    (total_symbols, alphabet) = compute_symbol_alphabet(file1)


    # ======================
    # CONSTURCTING SYMBOL-ENCODER TABLES - from Alphabet

    T_encoder = {}
    Tprime_encoder = {}

    for achar in alphabet.keys():
        anum = random.randint(0,2**32) #random.randint(4)
        T_encoder[achar] = anum
        Tprime_encoder[achar] = anum << k

    # ======================
    # CONSTURCTING DICTIONARY - FROM STRING-1

    with open(file1, "r") as f:

        # finding sub-strings 
        try:
            start_indx = 0 
            seg0 = f.read(k)
            if not seg0:
                print("ERROR: Cannot read first segment!")
                raise Exception
            segment0 = SelfAnnihilatingHash(s=seg0, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder)
            old_hashkey = segment0.hash_value

            segment_dict = {}
            segment_dict[segment0] = 0

            old_symbol = seg0[0]
            while True:
                start_indx = start_indx + 1
                f.seek(start_indx)
                seg = f.read(k)
                if not seg:
                    break
                new_symbol = seg[-1]
                segment = SelfAnnihilatingHash(s=seg, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder, prev_key=old_hashkey, removed_symbol=old_symbol, introduced_symbol=new_symbol ) 

                if segment not in segment_dict.keys(): 
                    segment_dict[segment] = start_indx

                old_hashkey = segment.hash_value
                old_symbol = seg[0]
        except:
            print("ERROR! Reading file1!")
            exit(-1)

    # ======================
    # DETECTING - COMMON SUBSTRINGS

    commons = []

    with open(file2, "r") as f2:
        # finding sub-strings 

        start_indx = 0 
        try:
            seg0 = f2.read(k)
            if not seg0:
                print("ERROR: Cannot read first segment!")
        except:
            print("ERROR: Reading first segement in file2!")
            exit(-1)

        # ------ 
        # Ensure all symbols exist in Alphabet. 
        for achar in seg0:
            if achar not in T_encoder.keys():
                update_alphabet(achar, k, alphabet, total_symbols, T_encoder, Tprime_encoder)


        segment0 = SelfAnnihilatingHash(s=seg0, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder)
        old_hashkey = segment0.hash_value
        old_symbol = seg0[0]

        # detect the segment in dictionary
        try: 
            src_indx = segment_dict[segment0]
            commons.append( (src_indx, start_indx) )
        except:
            pass

        while True:
            start_indx = start_indx + 1
            f2.seek(start_indx)
            seg = f2.read(k)
            if not seg:
                break
            new_symbol = seg[-1]
            # --------------------------
            # Ensure that the new-symbol being added exists in Vocabulary. If not, account for it. 
            if new_symbol not in T_encoder.keys():
                alphabet[new_symbol] = 1
                total_symbols = total_symbols + 1
                anum = random.randint(0,2**32) #random.randint(4)
                # Ensure that the random-int doesn't exist in Table. 
                while( anum in T_encoder.values() ):
                    anum = random.randint(0,2**32) #random.randint(4)
                T_encoder[new_symbol] = anum
                Tprime_encoder[new_symbol] = anum << k

            # --------------------------
            segment = SelfAnnihilatingHash(s=seg, T_encoder=T_encoder, Tprime_encoder=Tprime_encoder, prev_key=old_hashkey, removed_symbol=old_symbol, introduced_symbol=new_symbol ) 
            try: 
                src_indx = segment_dict[segment]
                commons.append( (src_indx, start_indx) )
            except:
                pass

            old_hashkey = segment.hash_value
            old_symbol = seg[0]

    
    return (commons, segment_dict)


def experiment_with_strings():
    string1 = "Searching for common substrings is a very important problem in computer science."
    string2 = "Solve this problem using a hash table. Your code should input two files that contain the strings s1 and s2 along with the number k.It then outputs all possible postions i, j in the strings where the matches occur. "
    k = 5 # size of k-mer


    (result1 , segment_dict_1) = read_from_strings(string1, string2, k)
    print(result1)


def experiment_with_files_rolling():
    dir = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/"
    dfiles = [ 'war_and_peace_tolstoy.txt', 'hemingway-sun-also-rises.txt', 'anna_karenina_tolstoy.txt', 'bacterial_genome_2.txt', 'hemingway-stories-poems.txt', 'bacterial_genome_1.txt', 'monkeypox-genome.txt', 'hemingway-in-our-time.txt']

    file1 = dir + 'bacterial_genome_2.txt'
    file2 = dir + 'bacterial_genome_1.txt'
    k = 20
    (result2, segment_dict_2) = read_from_files_rolling(file1, file2, k)
    print("total-common-patterns: %d" % len(result2))
    print("total-unique-keys: %d" % len(segment_dict_2.keys()))

    check_diags(result2)

def check_diags(result2):
    isEqual = True
    diags = []
    for (x,y) in result2:
        if (x !=  y):
            #print((x,y))
            isEqual = False
        else:
            diags.append(x)
    
    print("length-diags: %d" % len(diags))
    #print(diags)
    if isEqual:
        print("Exactly equal indices for both files!")


# -------------------
# DEFAULT HASH FUNCTION:
def read_from_files(file1, file2, k):

    # ======================
    # CONSTURCTING DICTIONARY - FROM FILE-1
    segment_dict = {}

    with open(file1, "r") as f:

        # finding sub-strings 
        try:
            start_indx = 0 
            seg0 = f.read(k)
            if not seg0:
                print("ERROR: Cannot read first segment!")
                raise Exception

            segment_dict[seg0] = 0
            old_symbol = seg0[0]
            while True:
                start_indx = start_indx + 1
                f.seek(start_indx)
                seg = f.read(k)
                if not seg:
                    break
                new_symbol = seg[-1]

                if seg not in segment_dict.keys(): 
                    segment_dict[seg] = start_indx

                old_symbol = seg[0]
        except:
            print("ERROR! Reading file1!")
            exit(-1)

    # ======================
    # DETECTING - COMMON SUBSTRINGS

    commons = []

    with open(file2, "r") as f2:
        # finding sub-strings 

        start_indx = 0 
        try:
            seg0 = f2.read(k)
            if not seg0:
                print("ERROR: Cannot read first segment!")
        except:
            print("ERROR: Reading first segement in file2!")
            exit(-1)


        # detect the segment in dictionary
        try: 
            src_indx = segment_dict[seg0]
            commons.append( (src_indx, start_indx) )
        except:
            pass

        while True:
            start_indx = start_indx + 1
            f2.seek(start_indx)
            seg = f2.read(k)
            if not seg:
                break

            try: 
                src_indx = segment_dict[seg]
                commons.append( (src_indx, start_indx) )
            except:
                pass

    return (commons, segment_dict)


def experiment_with_files():
    dir = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/"
    dfiles = [ 'war_and_peace_tolstoy.txt', 'hemingway-sun-also-rises.txt', 'anna_karenina_tolstoy.txt', 'bacterial_genome_2.txt', 'hemingway-stories-poems.txt', 'bacterial_genome_1.txt', 'monkeypox-genome.txt', 'hemingway-in-our-time.txt']

    file1 = dir + 'bacterial_genome_2.txt'
    file2 = dir + 'bacterial_genome_1.txt'
    k = 20
    (result2, segment_dict_2) = read_from_files(file1, file2, k)
    print("total-common-patterns: %d" % len(result2))
    print("total-unique-keys: %d" % len(segment_dict_2.keys()))

    check_diags(result2)

if __name__=="__main__":

    #experiment_with_strings():
    print("---- rollingHash exp: ")
    experiment_with_files_rolling()
    print("---- default exp: ")
    experiment_with_files()






    


