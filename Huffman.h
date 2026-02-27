#ifndef HUFFMAN
#define HUFFMAN
#include <string>
#include<iostream>
#include<unordered_map>
#include<vector>
#include<algorithm>
#include<queue>
#include<bitset>
using std::pair;
using std::string;
using std::unordered_map;
using std::vector;
using std::sort;
using std::priority_queue;

struct Node
    {
        /* data */
        char c;
        int frqcy;
        Node *left;
        Node *right;
        Node(char ch, int f) : c(ch), frqcy(f), left(nullptr), right(nullptr) {}
    };

class Huffman{
    private:
        Node* huffmanNode;
        void generateHufTree(string s);
    public:
        Huffman(string s);
        string decodeHuff();
        unordered_map<char,string> getHuffmanCode();
        ~Huffman();
};
#endif