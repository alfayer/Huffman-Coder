#include "Huffman.h"
#include <memory>

// 比较器：比较 Node 指针
struct CompareNodePtr {
    bool operator()(const Node* a, const Node* b) const {
        return a->frqcy > b->frqcy;  // 小顶堆
    }
};

Huffman::Huffman(string s) {
    generateHufTree(s);
    getHuffmanCode();
}

Huffman::~Huffman() {
    // 需要递归删除所有节点
    destroyTree(huffmanNode);
}

void Huffman::destroyTree(Node* node) {
    if (!node) return;
    destroyTree(node->left);
    destroyTree(node->right);
    delete node;
}

void Huffman::generateHufTree(string s) {
    // 统计频率
    unordered_map<char, int> freqMap;
    for (char c : s) {
        freqMap[c]++;
    }
    
    // 优先队列存储 Node*
    priority_queue<Node*, vector<Node*>, CompareNodePtr> pq;
    
    // 创建叶子节点
    for (const auto& entry : freqMap) {
        pq.push(new Node(entry.first, entry.second));
    }
    
    // 特殊情况：只有一个字符
    if (pq.size() == 1) {
        Node* single = pq.top();
        huffmanNode = new Node('\0', single->frqcy);
        huffmanNode->left = single;
        huffmanNode->right = nullptr;
        return;
    }
    
    // 构建哈夫曼树
    while (pq.size() > 1) {
        Node* left = pq.top(); pq.pop();
        Node* right = pq.top(); pq.pop();
        
        Node* parent = new Node('\0', left->frqcy + right->frqcy);
        parent->left = left;
        parent->right = right;
        
        pq.push(parent);
    }
    
    // 根节点
    huffmanNode = pq.top();
}

void Huffman::getHuffmanCode() {
    codeMap.clear();
    generateCodes(huffmanNode, "");
}

void Huffman::generateCodes(Node* node, string code) {
    if (!node) return;
    
    // 叶子节点
    if (!node->left && !node->right) {
        codeMap[node->c] = code;
        return;
    }
    
    // 递归
    generateCodes(node->left, code + '0');
    generateCodes(node->right, code + '1');
}


void Huffman::printHuffmanTree(Node* node, int depth) {
    if (!node) return;
    
    // 先打印右子树
    printHuffmanTree(node->right, depth + 1);
    
    // 打印当前节点
    std::cout << std::string(depth * 4, ' ');
    if (!node->left && !node->right) {
        // 叶子节点
        if (node->c == ' ') {
            std::cout << "' ':" << node->frqcy;
        } else if (node->c == '\0') {
            std::cout << "*:" << node->frqcy;
        } else {
            std::cout << "'" << node->c << "':" << node->frqcy;
        }
    } else {
        // 内部节点
        std::cout << "*:" << node->frqcy;
    }
    std::cout << std::endl;
    
    // 打印左子树
    printHuffmanTree(node->left, depth + 1);
}

void Huffman::printTree() {
    std::cout << "\nHuffman Tree Structure:\n";
    std::cout << "=======================\n";
    printHuffmanTree(huffmanNode, 0);
}

void Huffman::printCodes() {
    std::cout << "\nHuffman Codes:\n";
    std::cout << "==============\n";
    for (const auto& pair : codeMap) {
        if (pair.first == '\0') {
            std::cout << "space: " << pair.second << "\n";
        } else if (pair.first == '\0') {
            std::cout << "NULL: " << pair.second << "\n";
        } else {
            std::cout << "'" << pair.first << "': " << pair.second << "\n";
        }
    }
}

string Huffman::decodeHuff() {
    // 需要实现解码逻辑
    return "";
}