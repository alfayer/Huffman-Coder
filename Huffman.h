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
        void printHuffmanTree(Node* node, int depth = 0);
        void generateCodes(Node* node, string code);
        void destroyTree(Node* node);
    public:
        unordered_map<char, string> codeMap;
        Huffman(string s);
        string decodeHuff();
        void getHuffmanCode();
        void printTree();
        void printCodes();
        unordered_map<char, string> getMap(){return codeMap;}
        ~Huffman();
};
#endif