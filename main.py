import streamlit as st
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
    xmin = new_file[3][7:] # The xmin and xmax variables represent the length in seconds of the file. These are
    xmax = new_file[4][7:] # always on the 4th and 5th lines of the TextGrid, hence the use of indices 3 and 4.
    size = int(new_file[6][7:]) # Similarly, the size of the TextGrid represents the amount of tiers.
    new_file[6] = "size = " + str(size + 1) # We need to change the size of our new file to be 1 + the size
                                            # of the original, as we are adding a tier.
    number_tier_metadata = ["item ["+str(size+1)+"]:",   # Necessary tier metadata. The name is currently fixed to
                               'class = "IntervalTier"', # "Number" to avoid user input. This can be changed in
                               'name = "Number"',        # Praat anyways.
                               "xmin = " + xmin,
                               "xmax = " + xmax,
                               "intervals: size = " + interval_size]
    with open("number_tier_output.txt", "w") as file_2: # Write the new file.
        for line in new_file:
            file_2.write(line + "\n")
        for line in number_tier_metadata:
            file_2.write(line + "\n")
        for line in number_tier:
            file_2.write(line + "\n")
    return file_2
print(generate_number_tier("Input_test.TextGrid"))
header = st.container()
body = st.container()
file_upload = st.container()
with header:
    st.title("Welcome to the Praat Number Tier generator")
    st.text("This program automatically count words in Praat.")
with body:
    st.header("How it works")
    st.text("The input must be a .TextGrid or .txt, with a tier titled \"sentence - words\" \n"
            "being the last most tier. There can be any number of tiers above. The sentence - words\n"
            " tier must contain various words, each delimited by a pair of boundaries. The program \n"
            "will ignore empty intervals and create a new file, identical to the input file, but with\n"
            " an added Number tier. The Number tier will have the same boundaries as the sentence - \n"
            "words tier. For each interval with a word in it, the Number tier will contain a number \n"
            "corresponding to the amount of times that word has occured, starting from 1.")
with file_upload:
    st.header("File input/output")
    input_file = st.file_uploader("Upload file:")
    if input_file is not None:
        output_file = generate_number_tier(input_file)
        st.download_button(output_file.getValue())
    try:
        output_file = generate_number_tier(input_file)
    except:
        print("No file found")