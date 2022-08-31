/*

https://leetcode.com/problems/occurrences-after-bigram/
Given two strings first and second, consider occurrences in some text of the form "first second third", where second comes immediately after first, and third comes immediately after second.
Return an array of all the words third for each occurrence of "first second third".

Input: text = "alice is a good girl she is a good student", first = "a", second = "good"
Output: ["girl","student"]
*/

#include <iostream>
#include <vector>
#include <string>

        std::vector<std::string> findOcurrences(std::string text, std::string first, std::string second) {

            std::string query = first + " " + second;
            std::size_t query_length = query.size();
            std::vector<std::string> result = {};
            
            std::size_t start_index, end_index, length_word;
            std::string new_word;

            std::size_t found = text.find(query);
            
            while (found!=std::string::npos){
                //std::cout << " 'query' found at: " << found << '\n';
                
                // find the space-char after this. 
                //std::cout<<"found-index: "<< found <<std::endl;
                //if(found!=0) std::cout<<"prev-char: "<< text.at(found-1) << std::endl;
                
                if( found == 0 || ( found != 0 && text.at(found-1)==' ') ){                 
                    start_index = found + query_length +1; 
                    if (start_index < text.size()){
                        //std::cout << "start_index: " << start_index << '\n';
                        end_index = text.find(" ", start_index);
                        //std::cout << "end_index: " << end_index << '\n';
                        if(end_index!= std::string::npos){
                            //std::cout<<"inside if.if"<<std::endl;
                            length_word = end_index - start_index; 
                        }else{
                            // if no space exists - 
                            //std::cout<<"inside if.else"<<std::endl;
                            length_word = text.size() - start_index;
                            //std::cout<<"length-word; "<< length_word << " text.size"<< text.size() << std::endl;
                        }
                        std::string new_word = text.substr(start_index, length_word);
                        result.push_back(new_word);   
                    }
                }
                found = text.find(query, found + 1);   
            }

            return result;
        }

int main(){

    std::string text = "we will we will rock you";
    std::string first = "we";
    std::string second = "will";

    std::vector<std::string> result; 
    result = findOcurrences(text, first, second);

    for (int i=0; i<result.size(); i++){
        std::cout<< result[i] <<"\t";
    }
    std::cout<< std::endl;
}
