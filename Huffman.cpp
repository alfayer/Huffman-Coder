#include "Huffman.h"

// 定义比较函数，用于priority_queue
struct Compare
{
    bool operator()(const pair<char, int> &a, const pair<char, int> &b)
    {
        return a.second > b.second; // 小顶堆
    }
};

Huffman::Huffman(string s)
{
    generateHufTree(s);
}

Huffman::~Huffman()
{
}

void Huffman::generateHufTree(string s)
{
    unordered_map<char, int> map;
    for (int i = 0, totalLen = s.size(); i < totalLen; i++)
    {
        map[s[i]] += 1;
    }

    // 直接使用priority_queue，避免vector和sort
    priority_queue<pair<char, int>, vector<pair<char, int>>, Compare> q;

    // 将unordered_map中的元素直接插入priority_queue
    for (const auto &entry : map)
    {
        q.push(entry);
    }

    Node *left, *right, *root;
    while (q.size() > 1)
    {
        left = new Node(q.top().first, q.top().second);
        q.pop();
        right = new Node(q.top().first, q.top().second);
        q.pop();
        root = new Node(0, 0);
        root->frqcy = left->frqcy + right->frqcy;
        root->left = left;
        root->right = right;
        q.push(pair<char, int>(root->c, root->frqcy));
    }
    huffmanNode = new Node(q.top().first, q.top().second);
}
string Huffman::decodeHuff()
{

}
unordered_map<char, string> Huffman::getHuffmanCode()
{

}