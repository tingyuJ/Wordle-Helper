# letters = ["Q", "W", "R", "O", "Y", "J", "A", "B", "X", "Z"]
# letters = 'QWROYJABXZ'

# for i in letters:
#     word = ""
#     count = 0
#     for j in letters:
#         word = "A" + i + j + "OR"
#         count += 1
#         print(word)
        
        
# ./speller texts/wordle.txt
    
    
    
    
    

# letter1 = "a"
# letter2 = "b"
# letter3 = ""
# letter4 = ""
# letter5 = "c"
# xletters = "abc"
# count = 0
# ans = []

# for i in xletters:
#     for j in xletters:
#         for k in xletters:
#             for m in xletters:
#                 for n in xletters:
                        
#                     word = i + j + k + m + n
                    
#                     if word[0:1] is letter1:
#                         continue
#                     if word[1:2] is letter2:
#                         continue
#                     if word[2:3] is letter3:
#                         continue
#                     if word[3:4] is letter4:
#                         continue
#                     if word[4:5] is letter5:
#                         continue
#                     count += 1
#                     print(word)
# print(count)              
    
    
    
    
    
              
# letters = "abcdef"
# length = len(letters)
# psblts = []


# for i in letters:
#     if length is not 1:
        
#         for j in letters:
#             if length is not 2:
                
#                 for k in letters:
#                     if length is not 3:
                        
#                         for m in letters:
#                             if length is not 4:
                                
#                                 for n in letters:
#                                     # print(i+j+k+m+n)
#                                     psblts.append(i+j+k+m+n)
                
#                             else:
#                                 # print(i+j+k+m)
#                                 psblts.append(i+j+k+m)
                
#                     else:
#                         # print(i+j+k)
#                         psblts.append(i+j+k)
                
#             else:
#                 # print(i+j)
#                 psblts.append(i+j)
                
#     else:
#         # print(i)
#         psblts.append(i)
        

# print(psblts)
# print("end")





# from itertools import combinations_with_replacement
# sample_list = ['a', 'b']
# list_combinations = list()
# list_combinations += list(combinations_with_replacement(sample_list, 2))
# print(list_combinations)






# list = []

# for s in range(3):
#     s = ""
#     list.append(s)
    
# print(list)

# for s in list:
#     index = list.index(s)
#     s += "2"
#     list[index] = s
    
# print(list)

# letters = "abc"
# for s in list:
#     index = list.index(s)
#     for i in letters:
#         s += i
#         list[index] = s
#         letters = letters[1:len(letters)]
#         print(letters)
#         break
    
# print(list)





letter1 = "a"
letter2 = "b"
letter3 = ""
letter4 = ""
letter5 = "c"
xletters = "1234"
count = 0
ans = []

for i in xletters:
    for j in xletters:
        for k in xletters:
            for m in xletters:
                for n in xletters:
                      
                    if letter1:
                        i = letter1
                    if letter2:
                        j = letter2
                    if letter3:
                        k = letter3
                    if letter4:
                        m = letter4
                    if letter5:
                        n = letter5
                        
                    word = i + j + k + m + n
                    ans.append(word)
                    
                    count += 1
                    # print(word)
                    
ans = list(dict.fromkeys(ans))
print(count) 
print(ans)
 
dic = ["ab11c"]

for a in ans:
    if a in dic:
        print(a)