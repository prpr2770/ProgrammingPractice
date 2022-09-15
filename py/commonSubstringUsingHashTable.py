"""
Searching for common substrings is a very important problem in computer
science. We are given two strings: s1, s2 of possibly different lengths and a number k. We would
like to know if there is a substring s1[i] . . . s1[i + k − 1] that matches s2[j] . . . s2[j + k − 1]. 
Solve this problem using a hash table.
Your code should input two files that contain the strings s1 and s2 along with the number k.
It then outputs all possible postions i, j in the strings where the matches occur.


Notes:
0. Two methods to solve the problem: 
    a) Assume that the data1 and data2 can fit into memory. 
    b) Assume that the data1 and data2 can only be read as input-data-stream. 

1. Try to read from the data as a stream. Don't treat it as if it's available in memory. 
2. Define a rolling-hash-function, so that you can easily compute the hashFunctions, from the previously available hashKeys. 
    + Note that: 
        - the input data follows a pattern. Each successive word, differs from the previous by one character. 
        And that too only at the terminal positions. 
        - performance analysis of your whole program/code :: 
            a) to get the result in least time. 
3. Observe that we are using the HashTable only for the lookup!! We only wish to know whether there 


Concerns to ponder: 
1. In what other ways can you think of optmizing this program? 
    - why was it the case that designing a rolling-hash-function was an optimization? 

2. Define Classes - to handle in-memory and streamingCompute? 
Maybe compare how they perform?? 
class inMemoryCompute:
class streamingCompute: 

"""

import copy
import timeit
import itertools

class SegmentKey(object):
    id_iter = itertools.count()
    def __init__(self, word, hashType=None, encoding_table=None, prev_key=None, old_char=None, new_char=None):
        """
        input: 
            - word : 
            - hashType = []
            - prev_key : hashKey generate for previous k-mer with only one-char different from word
            - encoding_table : the dictionary that encodes each character to an integer value. 
            - old_char : symbol that exists in previous-word with hashKey = prev_key
            - new_char : symbol introduced in word, that's absent in previous-word with hashKey  = prev_key
        """
        self.segment = word
        self.prev_key = prev_key
        self.id = next(SegmentKey.id_iter)
        self.hash_key = None
        self.segment_encoding = encoding_table

        if self.segment_encoding == None: 
            self.__update_segment_encoding()

        if hashType in ["hash1", "rolling1", "rolling2" None]:
            self.hash_type = hashType

            self.__update_hashkey()   # compute self-hash key and store it. 
        else:
            raise Exception
        
    def __char_encoder(self, achar):
        """
        Character Encoding Function based on ASCII character codes.

        Note: 
        There can be different types of encodings being used. 
        """
        result = (1 + ord(achar) - ord('a'))
        return result


    def __update_segment_encoding(self):
        """
        Define the Transformation function T(s_i) for each symbol in segment. 
        """
        word = self.segment
        length = len(word)
        word_encoding = {} # dictionary look-up table to encode symbols in segment.
        for i in range(length):
            achar = word[i]
            if achar not in word_encoding.keys():
                char_encoding = self.__char_encoder(achar)
                word_encoding[achar]=char_encoding
        
        self.segment_encoding = word_encoding
        

    def __hashFun1_rec(self, word):

        if len(word) == 1:
            result = self.segment_encoding[word]
        else:
            result = (self.radix_r * self.__hashFun1_rec(word[:-1]) + self.segment_encoding[ word[-1]] ) 
            result = result % self.max_ring  #Always constrain the value to lie within the RING
        return result

    def __hashFun1_init(self):
        self.radix_r = 37
        self.max_ring = 10**9 + 7

    def __hashFun1(self, word):
        """ custom hashfun-1:   
        polynomial-rolling-hash-function computation independent of previous keys.

        Question: How to optimize the computation by using numpy? 
        """
        self.__hashFun1_init()      # initialize parameters of hashing function
        return self.__hashFun1_rec(word)

    def __hashFun1_rolling1(self, word, prev_key=None, old_char, new_char):
        """ custom rolling-hashfun-1:   """
        if prev_key == None: 
            result = self.__hashFun1(word)
        else:
            self.__hashFun1_init()      # initialize parameters of hashing function
            length = len(word)
            result = self.radix_r * prev_key + self.segment_encoding[new_char] - (self.radix_r**length)*old_char
            result = result % self.max_ring
        
        return result

    def __hashFun_rolling2(self, word, prev_key, old_char, new_char):
        """ custom rolling-hashfun-2:   
        Hashing by Cyclic Polynomials - 
        w-bit word used in architecture-representation. 

        The symbol transformation is a lookup table containing “random” elements of GF(2)[ x]/( xw 1 1), indexed by the ordinal value of its argument. In the author’s practice, the table consists of words whose contents are filled from a computer’s random-number generator.
        """
        pass        

    def __hashFun_rolling3(self, word, prev_key, old_char, new_char):
        """ 
        Hashing by General Polynomial Division
        d-bit word representation. 
        w-bit word with w>d and (w-d) leading bits set to zero. 

            symbol transformation is
            performed by consulting a lookup table containing “random” elements of
            GF(2)[ x]/p( x), indexed by the ordinal value of its argument. To remove the
            contribution of the old symbol, the transformation T may be combined with
            multiplication by xn to form a new transformation
            T'(s) = x^n * T(s)
            T' may also be precomputed and be implemented by a lookup table.

            T may be produced by repeated calls to a random-word generator.
        """
        pass     



    def __custom_compute_hash(self):
        """
        input: 
            - segment-key that needs to be hashed. 
            - hashType : string representing the hashingFunctionName

        output: 
            - HashFun(segment)
        """

        if self.hash_type == "hash1":
            key = self.__hashFun1(self.segment)
        elif self.hash_type == "rolling1":
            key = self.__hashFun1_rolling1(self.segment, self.prev_key)
        elif self.hash_type == "rolling2":
            key = self.__hashFun_rolling2(self.segment, self.prev_key)
        else: # default hash-function
            key =  None
        return key

    def __update_hashkey(self):
        """
        function to compute the hash-key for the element. And store it within it. 
        """
        self.hash_key = self.__hash__()

    def __eq__(self, other):
        return (self.segment == other.segment and self.id == other.id)

    def __hash__(self):
        if self.hash_type != None: 
            key = self.__custom_compute_hash()
        else:
            key = hash(self.segment)
        return key

    


def rollingHashFun_algo3(word0, hash0, word1):
    """
    Use this hashFunction to extract the keys to be inserted into the hashTable. 
    inputs: 
        - word0 : previous_key
        - hash0 : RollingHashFun(previous_key)
        - word1 : current_key

    output: 
        - hash1 : RollingHashFun(current_key)

    constraints: 
        - verify that word0 and word1, differ only by one-character!! ( at either terminal position )

    Note: Compute hash1 from hash0 using finite number of arithmetic operations. 
    """
    substring_dict = {}
    result = []
    # 1. Extract keys from data1
    len_data1 = len(data1)
    prevKey = None
    for i in range(len_data1):
        segment = SegmentKey(word=data1[i:i+k], hashType="rolling", prev_key=prevKey)
        substring_dict[segment] = i
        prevKey = copy.copy(segment.hash_key)
    
    len_data2 = len(data2)
    for j in range(len_data2):
        segment = SegmentKey(word=data2[j:j+k], hashType="rolling", prev_key=prevKey)
        try:
            i_indx = substring_dict[key]
            result.append( (i_indx, j) )
        except:
            # index doesn't exist.
            pass
        prevKey = copy.copy(segment.hash_key)
    return result




def algo2_simple_hashing(data1, data2, k):
    """

    1. Extract all k-length substrings in data1 :: as keys1
    2. Compute a = HashFun(key1) for each key in keys1. 
    3. Insert into Dict. Let the value be i : index of key1 in data1. 
    3. Extract all k-length substrings in data2 :: as keys2 
    4. Compute b = HashFun(key2) for each key in keys1. 
    5. Check if b EXISTS within Dict. If yes, return (i,j) where
        - i: value in Dict.
        - j: index of key2 in data2. 
    """
    substring_dict = {}
    result = []
    # 1. Extract keys from data1
    len_data1 = len(data1)
    prevKey = None
    for i in range(len_data1):
        segment = SegmentKey(word=data1[i:i+k], hashType="hash1", prev_key=prevKey)
        substring_dict[segment] = i
        
    
    len_data2 = len(data2)
    prevKey = None
    for j in range(len_data2):
        segment = SegmentKey(word=data2[j:j+k], hashType="hash1", prev_key=prevKey)
        try:
            i_indx = substring_dict[key]
            result.append( (i_indx, j) )
        except:
            # index doesn't exist.
            pass
    return result


def algo1_naive(data1, data2, k):
    """

    1. Extract all k-length substrings in data1. 
    2. Insert keys into hashTable. Let the value be i-index of key1 in data1. 
    3. Extract all k-length substrings in data2. 
    4. Check if the keys exist in hashTable. 
    5. If yes, 
        return (i,j) : where (i = value in Dict, j = index of key2 in data2. )
    """

    substring_dict = {}
    result = []
    # 1. Extract keys from data1
    len_data1 = len(data1)
    for i in range(len_data1):
        segment = SegmentKey(word=data1[i:i+k])
        substring_dict[segment] = i

    len_data2 = len(data2)
    for j in range(len_data2):
        segment = SegmentKey(word=data2[j:j+k])
        try:
            i_indx = substring_dict[segment]
            result.append( (i_indx, j) )
        except:
            # index doesn't exist.
            pass
    return result


    

def computeCommonSubstring(data1, data2, k):
    """
    Find the common substrings. Return the list of tuples (i,j) indicating location of common substrings. 
    """
    
    # default-hashing
    result = algo1_naive(data1, data2, k)

    ## simple-hash-function
    #result = algo2_simple_hashing(data1, data2, k)

    ## rolling-hash-function
    #result = rollingHashFun_algo3(data1, data2, k)

    return result



def testing():
    string1 = "Searching for common substrings is a very important problem in computer science."
    string2 = "Solve this problem using a hash table. Your code should input two files that contain the strings s1 and s2 along with the number k.It then outputs all possible postions i, j in the strings where the matches occur. "

    data1 = ''.join(string1.split(' '))
    data2 = ''.join(string2.split(' '))
    k = 5

    result_computeInMemory = computeCommonSubstring(data1, data2, k)

    print("result: ", result_computeInMemory)
    #result_computeStream = 

def common_substring_search_in_files(file1, file2, seg_size=10):
    """
    Input: 
        file1, file2 : names of files to read
        seg_size : k-mer size to be examined. 

    Output: 
        result = [(i,j) ] : where i,j represent indices of substring that's common to both files. 
                                - i : index of substring in file1
                                - j : index of substring in file2
    """
    substring_dict = {} # Accurate Counting via Dict
    result = [] # Final result is stored here as tuples of indices
    with open(file1) as f1:
        f1_count = 0 
        while True:
            # 1. compute the fseek-pointer-position
            # 2. read M=10*k
            # 3. iterate and extract seg_size segments, until it (M-k)
            dataseg1 = f1.read(seg_size)
            if not dataseg1:
                break
            segment = SegmentKey(word=dataseg1)
            substring_dict[segment] = f1_count
            f1_count = f1_count + 1
            if f1_count % 100 == 0:
                print("%d :  %s \n" % (f1_count, dataseg1) )
    print("completed file1!\n")

    catchinput = input("Enter any key")

    with open(file2) as f2:
        f2_count = 0 
        while True:
            dataseg2 = f2.read(seg_size)
            segment = SegmentKey(word=dataseg2)
            try:
                f1_count = substring_dict[segment]
                result.append( (f1_count, f2_count) )
            except:
                # index doesn't exist.
                pass
            f2_count = f2_count + 1
            if (f2_count % 200 == 0):
                print("segment-id: %d, " % f2_count)

    print("completed file2!\n")

    return result


# compute binary search time
def naive_hashing():
    SETUP_CODE = '''
from __main__ import common_substring_search_in_files
'''
 
    TEST_CODE = '''
f1 = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/bacterial_genome_1.txt"
f2 = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/bacterial_genome_2.txt"
k = 20
result = process_input_files(file1=f1, file2=f2, seg_size=k)
'''
     
    # timeit.repeat statement
    times = timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE,
                          repeat = 3,
                          number = 10000)
 
    # printing minimum exec. time
    print('Default Hashing based substring-search: {}'.format(min(times)))       
 
 


if __name__=="__main__":

    #/'''
    f1 = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/bacterial_genome_1.txt"
    f2 = "/Users/uchiha/Downloads/Fall2022Courses/Sriram_AdvDataStructures/hw1/bacterial_genome_2.txt"
    k = 2000
    result = common_substring_search_in_files(file1=f1, file2=f2, seg_size=k)
    print("Computing length of result: ")
    print( len(result) )
    #'''

    # timing it
    #naive_hashing()



