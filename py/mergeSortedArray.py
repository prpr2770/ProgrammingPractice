
    
def setSwitch( anums1:int, anums2:int) -> bool:
    if(anums1<=anums2):
        return False
    else:
        return True
    
def merge_with_extra_array( nums1, m: int, nums2, n: int):
    """
    Create a temporary results-array. Update that while traversing both input-arrays. 
    later, rename first-input-array to point to temporary result-array. 
    """
    Mhd = 0
    Nhd = 0
    result = []
    switch = setSwitch(nums1[0], nums2[0])
    cursor = 0 
    print("Total Length => nums1: %d, nums2: %d"%(m, n))
    while(Mhd<m or Nhd<n):
        print("Mhd: %d, Nhd: %d" %(Mhd, Nhd))
        if(Mhd < m):
            if(switch): #nums2 has lesser elements
                result.append(nums2[Nhd])
                Nhd = Nhd + 1
            else:
                result.append(nums1[Mhd])
                Mhd = Mhd + 1
            switch = setSwitch(nums1[Mhd], nums2[Nhd])
        else:
            result.append(nums2[Nhd])
            Nhd = Nhd + 1

    print("result", result)
    return result


def merge_with_no_extra_array( nums1, m: int, nums2, n: int):
    """
    Do not return anything, modify nums1 in-place instead.
    """
    
def merge( nums1, m: int, nums2, n: int) -> None:

    # Implementation-1: with extra memory created
    nums1 = merge_with_extra_array( nums1, m, nums2, n)

    # Implementation-2: with NO Extra Memory. 
    merge_with_no_extra_array(nums1, m, nums2, n)


if __name__=="__main__":
    nums1 = [1,2,3,0,0,0]
    m = 3
    nums2 = [2,5,6]
    n = 3

    merge(nums1, m, nums2, n)
    print("nums1", nums1)