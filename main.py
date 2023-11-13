def generate_number_tier(original_file):
    new_file = [] # The original file, copied
    number_tier_boilerplate = ["item [3]:",
        'class = "IntervalTier"',
        'name = "Number"',
        "xmin = 0",
        "xmax = 789.48781",
        "intervals: size = 321"]
    number_tier = [] # The new tier to be added, represented as a list of boundaries
    with open(original_file,'r') as file:
        token_count = {} # A dictionary of all the words and how many times each has occurred
        word_tier = False # A boolean to track whether or not the program has read up to the word tier
        for line in file.readlines():
            line = line.strip()
            if len(new_file) == 6:
                new_file.append("size = 3")
            else:
               new_file.append(line)
            if line == "name = \"sentence - words\"":
                word_tier = True
            if word_tier:
                boundary = []

                if "text" in line:
                    token = line[8:-2]
                    if token != "":
                        if token not in token_count:
                            token_count[token] = 1
                        else:
                            token_count[token] += 1
                        line = "text = \"" + str(token_count[token]) + "\""

                boundary.append(line)
                if len(boundary) == 4:
                    boundary = []
                number_tier.append(boundary)
    with open("newfile.txt", "w") as file_2:
        for line in new_file:
            file_2.write(line + "\n")
        for line in number_tier_boilerplate:
            file_2.write(line + "\n")
        number_tier.pop(0)
        number_tier.pop(0)
        number_tier.pop(0)
        number_tier.pop(0)
        for boundary in number_tier:
            for line in boundary:
                file_2.write(line + "\n")
generate_number_tier("Input_test.TextGrid")
