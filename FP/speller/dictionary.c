// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = (LENGTH + 1) * 'z';

// Hash table
node *table[N];

int total_words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashed_value = hash(word);
    node *cursor = table[hashed_value];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return (sum % N);
    
    //credit: https://www.youtube.com/watch?v=HsnjdbHMZO8
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    
    char word[LENGTH + 1];
    total_words = 0;
    
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, word);
        n->next = NULL;
        
        int hashed_value = hash(word);
        
        if (table[hashed_value] == NULL)
        {
            table[hashed_value] = n;
        }
        else
        {
            n->next = table[hashed_value];
            table[hashed_value] = n;
        }
        
        total_words++;
    }
    
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return total_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
