/*
Given an aray of integers `nums` and an integer `target`, return indices of two numbers such that they add up to `target`.
You can assume that each input array will have exactly one solution. And you may not use the same element twice. 
You can return the answer in any order. 
*/

#include <iostream>
#include <vector>

//using namespace std; 

std::vector<int> twoSum( std::vector<int>& nums, int target){
    
    std::vector<int> result;
    
    int temp = 0; 

    for (int i=0; i< nums.size(); i++){
        for (int j=i+1; j<nums.size(); j++){

            temp = nums[i] + nums[j];
            if (temp == target){
                result.push_back(i);
                result.push_back(j);
                break;
            }else{
                temp = 0;
            }
         }
    }

    return result;

}


int main(){

    std::vector<int> nums = {2,3,4,5,6,8,10};
    int target = 11;

    std::vector<int> result = twoSum(nums, target);

    std::cout<<result[0] <<","<< result[1] <<std::endl;

    return 0;
}