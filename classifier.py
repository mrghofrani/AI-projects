
UNIGRAM = 0
BIGRAM = 1
TRIGRAM = 2

def main():
    model = dict()
    line = "initial value"
    topic_num = dict()
    number_of_start_sign = 0 # number of start sign
    # +-------------------------+
    # |      Training part      |
    # +-------------------------+
    with open("HAM-Train-Test/HAM-Test.txt", "r") as ftrain:
        while True:
            line = ftrain.readline()
            if not line:
                break
            # If the line contains a topic 
            if "@@@@@@@@@@" in line:
                number_of_start_sign += 1
                topic = line.split("@@@@@@@@@@")[0]
                line = line.split("@@@@@@@@@@")[1]
                if topic not in model:
                    model[topic] = []
                    model[topic].append(dict()) # A dictionary for holding data related to unigram
                    model[topic].append(dict()) # A dictionary for holding data related to bigram
                    model[topic].append(dict()) # A dictionary for holding data related to trigram
                    topic_num[topic] = 0
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
                topic_num[topic] += 1 # for storing number of words in each topic
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

        # Going to calculate probability
        # Trigram
        for topic in model:
            for tpl in model[topic][TRIGRAM]:
                nominator = model[topic][TRIGRAM][tpl]
                antecedent = tpl[:TRIGRAM]
                antecedent = list(filter(lambda a: a != '*', antecedent))
                if len(antecedent) == 0:
                    denominator = number_of_start_sign
                elif len(antecedent) == 1:
                    antecedent = antecedent[0]
                    denominator = model[topic][UNIGRAM][antecedent]
                elif len(antecedent) == 2:
                    antecedent = tuple(antecedent)
                    denominator = model[topic][BIGRAM][antecedent]
                model[topic][TRIGRAM][tpl] = nominator / denominator
        # Bigram
        for topic in model:
            for tpl in model[topic][BIGRAM]:
                nominator = model[topic][BIGRAM][tpl]
                antecedent = tpl[:BIGRAM]
                antecedent = list(filter(lambda a: a != '*', antecedent))
                denominator = number_of_start_sign if len(antecedent) == 0 else model[topic][UNIGRAM][antecedent[0]]
                model[topic][BIGRAM][tpl] = nominator / denominator
        # Unigram
        for topic in model:
            for tpl in model[topic][UNIGRAM]:
                nominator = model[topic][UNIGRAM][tpl]
                # Here is no start sign so that there is no need to cope with it
                denominator = topic_num[topic]
                model[topic][UNIGRAM][tpl] = nominator / denominator

        # +-------------------------+
        # |      Testing part       |
        # +-------------------------+


if __name__ == "__main__":
    main()