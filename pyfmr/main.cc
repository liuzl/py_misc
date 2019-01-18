#include "fmr.h"
#include <stdio.h>

int main(int argc, char *argv[])  
{
    if (argc < 4)
    {
        printf("usage: %s <grammar_file> <s> <line>\n", argv[0]);
        return 1;
    }
    init_grammar(argv[1]);
    char *ret = extract(argv[3], argv[2]);
    printf("%s\n",ret);
    return 0;
}
