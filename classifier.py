
UNIGRAM = 0
BIGRAM = 1
TRIGRAM = 2

def main():
    model = dict()
    line = "initial value"
    with open("HAM-Train-Test/HAM-Test.txt", "r") as ftrain:
        while True:
            line = ftrain.readline()
            if not line:
                break
            # If the line contains a topic 
            if "@@@@@@@@@@" in line:
                topic = line.split("@@@@@@@@@@")[0]
                line = line.split("@@@@@@@@@@")[1]
                if topic not in model:
                    model[topic] = []
                    model[topic].append(dict()) # A dictionary for holding data related to unigram
                    model[topic].append(dict()) # A dictionary for holding data related to bigram
                    model[topic].append(dict()) # A dictionary for holding data related to trigram
            line = line.split(' ')
            
            # for other words
            # At first, we remove unwanter characters from our data line
            if '\n' in line:
                line.remove('\n')
            if '' in line:
                line.remove('')
            for word in line: # Calculating unigram
                if word not in model[topic][UNIGRAM]:
                    model[topic][UNIGRAM][word] = 0
                model[topic][UNIGRAM][word] += 1

            rsline = ['*'] + line # right shifted line
            for word1, word2 in zip(rsline, line):
                if (word1,word2) not in model[topic][BIGRAM]:
                    model[topic][BIGRAM][(word1,word2)] = 0
                model[topic][BIGRAM][(word1,word2)] += 1

            rs2line = ['*'] + rsline # double right shifted line
            for word1, word2, word3 in zip(rs2line, rsline, line):
                if (word1,word2,word3) not in model[topic][TRIGRAM]:
                    model[topic][TRIGRAM][(word1,word2,word3)] = 0
                model[topic][TRIGRAM][(word1,word2,word3)] += 1

if __name__ == "__main__":
    main()