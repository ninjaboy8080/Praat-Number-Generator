def generate_number_tier(original_file):

    line_buffer = 0 # Prevents us from copying the tier metadata. The program wants to add lines
                    # after reading the target tier name. However, there are lines underneath that we
                    # don't want to copy. Namely, xmin, xmax, etc. There are 4 of these lines.
    new_file = [] # The original file, copied
    number_tier = [] # The new tier to be added, represented as a list of boundaries
    with open(original_file,'r') as file:
        token_count = {} # A dictionary of all the words and how many times each has occurred
        word_tier = False # A boolean to track whether or not the program has read up to the word tier
        for line_number, line in enumerate(file.readlines()):
            line = line.strip()
            new_file.append(line)


            if line == "name = \"sentence - words\"":
                word_tier = True
            if word_tier:
                line_buffer += 1

                if line_buffer == 4:
                    interval_size = line[18:] # The number of boundaries in the sentence tier, and by extension,
                                              # the number tier too.

                if line_buffer > 4: # As mentioned above, there are 4 lines of metadata we want to skip.
                    if "text" in line:
                        token = line[8:-2]
                        if token != "":
                            if token not in token_count:
                                token_count[token] = 1
                            else:
                                token_count[token] += 1
                            line = "text = \"" + str(token_count[token]) + "\""
                    number_tier.append(line)
    xmin = new_file[3][7:]
    xmax = new_file[4][7:]
    size = int(new_file[6][7:])
    new_file[6] = "size = " + str(size + 1)
    number_tier_boilerplate = ["item ["+str(size+1)+"]:",
                               'class = "IntervalTier"',
                               'name = "Number"',
                               "xmin = " + xmin,
                               "xmax = " + xmax,
                               "intervals: size = " + interval_size]
    with open("newfile.txt", "w") as file_2:
        for line in new_file:
            file_2.write(line + "\n")
        for line in number_tier_boilerplate:
            file_2.write(line + "\n")
        for line in number_tier:
            file_2.write(line + "\n")
generate_number_tier("Input_test.TextGrid")
