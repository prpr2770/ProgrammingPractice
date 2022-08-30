/*
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, 
and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, 
but instead be stored inside the array nums1. 
To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that 
should be merged, and the last n elements are set to 0 and should be ignored. 
nums2 has a length of n.

*/

#include <iostream>
#include <vector>

using namespace std;

void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {

    std::vector<int> result;

    int i =0;
    int j =0;

    while(i<m || j<n){

            if (nums1[i] < nums2[j] && i<m){
                result.push_back(nums1[i]);
                i = i+1;
            }else if (nums1[i] > nums2[j] && i<m){
                result.push_back(nums2[j]);
                j = j+1;
            }else{
                result.push_back(nums2[j]);
                j = j+1;
            }
    }

    nums1.swap(result);

}


int main(){

    int m = 3;
    int n = 5;
    std::vector<int> nums1;
    std::vector<int> nums2;

    for(int i=0; i<m+n; i++){
        if(i<m){
            nums1.push_back(3);
        }else{
            nums1.push_back(0);
        }
        
    }

    for(int j=0; j<n; j++){
        nums2.push_back(5);
    }

    merge(nums1, m, nums2, n);

    for(int k=0; k<m+n; k++){
        std::cout<<nums1[k]<<",";
    }
    std::cout<<std::endl;

    return 0;
}