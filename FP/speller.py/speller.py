# f = open("dictionary","r")

# # dict = ["apple","grape","crazy"]
# list = []
# # badletters = "ry"

# for word in f.readlines():
#     list.append(word[0:5])
# # for word in dict:
#     # for bl in badletters:
#     #     print(bl)
#     #     print(word)
#     #     if bl not in word:

#     #         print("!")
#     #         continue

#     #     list.append(word)



# print(list)
# print(len(list))
# f.close()

def GetAnswers(letter1, letter2, letter3, letter4, letter5, oletters, xletters):

    #Get all 5 letters words
    f = open("dictionary","r")

    dictionary = []

    for word in f.readlines():
        dictionary.append(word[0:5])

    f.close()



    # if oletters is null, use all letters
    allletters = "qazwsxedcrfvtgbyhnujmikolp"
    if xletters:
        temp = ""
        for o in allletters:
            if o not in xletters:
                temp += o
        allletters = temp

    print("allletters: " + allletters)
    #Get all possiblities
    answers = []

    for i in allletters:
        for j in allletters:
            for k in allletters:
                for m in allletters:
                    for n in allletters:

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

                        answers.append(word)
        # Remove the dupicates
        answers = list(dict.fromkeys(answers))

    # Remove the dupicates
    answers = list(dict.fromkeys(answers))

    # print("=======================answers============================")
    # print(answers)


    excluded = []

    if xletters:

        for x in xletters:
            # first time when excluded is empty. Check the ones that do not contain the x letter
            if not excluded:
                for ans in answers:
                    # print(ans)
                    # print(x)

                    if x not in ans:
                        # print("o")
                        excluded.append(ans)

            # remove the ones that has the other x letters
            else:
                tempList = []
                for ex in excluded:
                    # print(ex)

                    if x in ex:
                        # print("x")
                        tempList.append(ex)

                for i in tempList:
                    excluded.remove(i)

    else:
        excluded = answers

    # print("===================removed x answers============================")
    # print(excluded)


    # Get the ones that exist
    result = []

    for ans in excluded:
        if ans in dictionary:
            result.append(ans)


    goodResult = []
    if oletters:
        for o in oletters:
            for r in result:
                if o in r:
                    goodResult.append(r)
    goodResult = list(dict.fromkeys(goodResult))

    if goodResult:
        result = goodResult

    return result




res = GetAnswers("t", "", "", "", "", "un", "qazwsxedcrfv")

print(res)
