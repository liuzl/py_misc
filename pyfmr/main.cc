#include "fmr.h"
#include <stdio.h>

int main(int argc, char *argv[])  
{
    if (argc < 4)
    {
        printf("usage: %s <grammar_file> <s> <line>\n", argv[0]);
        return 1;
    }
    int i = init_grammar(argv[1]);
    char *ret = extractx(i, argv[3], argv[2]);
    printf("%s\n",ret);
    gofree(ret);
    return 0;
}
