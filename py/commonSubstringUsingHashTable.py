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



class SegmentKey(object):
    def __init__(self, word, hashType=None, prev_key=None):
        self.segment = word
        self.prev_key = prev_key

        if hashType in ["hash1", "rolling", None]:
            self.hash_type = hashType
            self.update_hashkey()
        else:
            raise Exception
        
    
    def update_hashkey(self):
        self.hash_key = self.__hash__()
    
    def __eq__(self, p):
        return (self.segment == p.segment)

    def hashFun1(self, word):
        pass

    def hashFun_rolling(self, word, prev_key):
        pass

    def compute_hash(self, segment, hashType):
        """
        input: 
            - segment-key that needs to be hashed. 
            - hashType : string representing the hashingFunctionName

        output: 
            - HashFun(segment)
        """

        if hashType == "hash1":
            key = self.hashFun1(self.segment)
        elif hashType == "rolling":
            key = self.hashFun_rolling(self.segment, self.prev_key)
        else:
            key =  None
        return key
    
    def __hash__(self):
        if self.hash_type != None: 
            key = self.compute_hash(self.segment, self.hashType)
        else:
            key = hash(self.segment)
            
        return hash(self.segment)

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




if __name__=="__main__":

    string1 = "Searching for common substrings is a very important problem in computer science."
    string2 = "Solve this problem using a hash table. Your code should input two files that contain the strings s1 and s2 along with the number k.It then outputs all possible postions i, j in the strings where the matches occur. "

    data1 = ''.join(string1.split(' '))
    data2 = ''.join(string2.split(' '))
    k = 5

    result_computeInMemory = computeCommonSubstring(data1, data2, k)

    print("result: ", result_computeInMemory)
    #result_computeStream = 