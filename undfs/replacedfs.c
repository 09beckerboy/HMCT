#include <stdlib.h>
#include <stdio.h>
#include <direct.h>
#include <string.h>

struct DFSHeader
{
    char sign[4];
    int unknown1;
    int unknown2;
    int unknown3;
    int entry_count;
    int unknown4;
    int dict_size;
    int unknown5; // probably offset to blob sizes, but we always have only one blob so threat it all as single header
    int unknown6; // probably offset to file entries
    int dict_offset;
    int blob_size;
};

struct DFSEntry
{
    int filename1;
    int filename2;
    int maindir;
    int extension;
    int offset;
    int size;
};

size_t filelength(FILE *f)
{
    long t;
    long len;

    t = ftell(f);
    fseek(f, 0, SEEK_END);
    len = ftell(f);
    fseek(f, t, SEEK_SET);

    return len;
}

int main(int argc, char *argv[])
{
    char name_dfs[64];
    char name_000[64];
    char *dot;
    
    FILE *f = NULL, *blob = NULL, *new;
    int i;

    struct DFSHeader header;
    struct DFSEntry entry;

    char *dictionary = NULL;

    char path[256];
    void *buffer;

    long new_offset;
    long new_size;
    long blob_size;

    if(argc < 3)
    {
        printf("usage: replacedfs archive.dfs <name> <file>\n");
        printf("where <name> - file name in archive\n");
        printf("where <file> - file name on disk\n");
        goto exit;
    }
    
    strcpy(name_dfs, argv[1]);
    
    strcpy(name_000, name_dfs);
    dot = strchr(name_000, '.');
    if(dot)
        strcpy(dot, ".000"); 

    f = fopen(name_dfs, "r+b");
    if(!f)
        goto exit;
    blob = fopen(name_000, "ab");
    if(!blob)
        goto exit;

    if(fread(&header, 1, sizeof(header), f) != sizeof(header))
        goto exit;

    dictionary = malloc(header.dict_size);
    if(!dictionary)
        goto exit;

    fseek(f, header.dict_offset, SEEK_SET);
    if(fread(dictionary, 1, header.dict_size, f) != header.dict_size)
        goto exit;
    fseek(f, 0x2C, SEEK_SET);

    for(i = 0 ; i < header.entry_count; i++)
    {
        if(fread(&entry, 1, sizeof(entry), f) != sizeof(entry))
            goto exit;

        sprintf(path, "%s%s%s%s", 
            dictionary + entry.maindir,
            dictionary + entry.filename1,
            dictionary + entry.filename2,
            dictionary + entry.extension
        );
        
        if(stricmp(path, argv[2]) == 0)
        {
            new = fopen(argv[3], "rb");
            if(new)
            {
                new_size = filelength(new);
                new_offset = ftell(blob);
                
                buffer = malloc(new_size);
                fread(buffer, new_size, 1, new);
                fwrite(buffer, new_size, 1, blob);
                free(buffer);
                
                fclose(new);

                entry.offset = new_offset;
                entry.size = new_size;

                /* update entry */
                fseek(f, -sizeof(entry), SEEK_CUR);
                fwrite(&entry, 1, sizeof(entry), f);

                /* update blob size */
                blob_size = ftell(blob);
                fseek(f, 0x28, SEEK_SET);
                fwrite(&blob_size, 1, sizeof(blob_size), f);
            }
            else
                printf("Can't open file '%s'\n", argv[3]);

            goto exit;
        }
    }

    printf("File '%s' not found in achive\n", argv[2]);

    exit:
    if(f) fclose(f);
    if(blob) fclose(blob);
    free(dictionary);
    
    return 0;
}

