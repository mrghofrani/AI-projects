
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
            for word in line: # Calculating unigram
                if word not in model[topic][UNIGRAM]:
                    model[topic][UNIGRAM][word] = 0
                model[topic][UNIGRAM][word] += 1

            # for word in line:
            #     pass

            # for trigram:
            #     pass

if __name__ == "__main__":
    main()