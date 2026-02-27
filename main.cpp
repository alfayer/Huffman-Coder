
#include<iostream>
#include<vector>
#include"Huffman.h"
using namespace std;
//constexpr int test(int t);

int main(){
    std::cout<<"Hello World!"<<std::endl;
    string s="aabbbccddd";
    std::cout<<s<<std::endl;

    Huffman hfm(s);
    hfm.printTree();
    hfm.printCodes();
    hfm.compress(s);
    return 0;
}