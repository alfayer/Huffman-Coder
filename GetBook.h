#ifndef GETBOOK
#define GETBOOK
#define WebUrl "https://dev.gutenberg.org/cache/epub/7193/pg7193.txt"
#define OutputFile "books/"
#include <iostream>
#include<string>
#include<curl/curl.h>
class GetBook{
    private:
        std::string url=WebUrl;
        static int bookCount;
        CURL *curl;
        CURLcode res;
        FILE* f;
        size_t writeFunction(void*,size_t,size_t,void*);
    public:
        GetBook();
        void downloadBook();
};
#endif