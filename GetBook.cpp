#include"GetBook.h"

GetBook::GetBook(){
    bookCount=0;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    f=fopen("./books/book1.txt");
    curl=curl_easy_init();
}

size_t GetBook::writeFunction(void* ptr,size_t size,size_t nmemb,void* userdata){
    fwrite(ptr,size,nmemb,(FILE*)userdata);
    return size*nmemb;
}
void GetBook::downloadBook(){

    if(curl){
        curl_easy_setopt(curl,CURLOPT_URL,url);
        curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,writeFunction);
        curl_easy_setopt(curl,CURLOPT_WRITEDATA,f);
        res=curl_easy_perform(curl);
        if(res!=CURLE_OK){
            std::cout<<"传输失败";
        }
        fclose(f);

        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
}