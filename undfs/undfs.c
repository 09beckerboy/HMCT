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

void create_path(char *path)
{
    char *s = path;

    while(1)
    {
        s = strchr(s,'\\');
        
        if(s)
            *s = '\0';

        mkdir(path);

        if(s)
        {
            *s = '\\';
            s++;
        }
        else
            break;
    }
}

int main(int argc, char *argv[])
{
    char name_dfs[64];
    char name_000[64];
    char *dot;
    
    FILE *f = NULL, *blob = NULL, *out;
    int i;

    struct DFSHeader header;
    struct DFSEntry entry;

    char *dictionary = NULL;

    char path[256];
    void *buffer;

    if(argc < 1)
    {
        printf("usage: udfs file.dfs\n");
        goto exit;
    }
    
    strcpy(name_dfs, argv[1]);
    
    strcpy(name_000, name_dfs);
    dot = strchr(name_000, '.');
    if(dot)
        strcpy(dot, ".000"); 

    f = fopen(name_dfs, "rb");
    if(!f)
        goto exit;
    blob = fopen(name_000, "rb");
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
        
        printf("%s %d %d\n",
            path,
            entry.size,
            entry.offset
        );

        create_path(dictionary + entry.maindir);
        out = fopen(path, "wb");
        if(out)
        {
            buffer = malloc(entry.size);
            fseek(blob, entry.offset, SEEK_SET);
            fread(buffer, entry.size, 1, blob);
            fwrite(buffer, entry.size, 1, out);
            free(buffer);
            
            fclose(out);
        }
        else
            printf("Can't open file '%s' for writing\n", path);
    }

    exit:
    if(f) fclose(f);
    if(blob) fclose(blob);
    free(dictionary);
    
    return 0;
}
