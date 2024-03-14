import streamlit as st
import pandas
def get_word_category(word: str):
    '''
    This function returns an integer based on the "category" of the word. There are 4 categories that we
    are concerned with. Affricate first, affricate second, fricative first, fricative second. "First" refers
    to the phoneme being present in the first syllable. We need to treat these categories differently. For example,
    take "hongcha", which is a affricate second word. We need to replace "C2c" with "Tc" and "C2r" with "T".
    '''
    # Here, we exploit the fact that all syllables in pinyin are at least two letters (for the words present
    # in the word-list).
    first_half = word[0:2]
    second_half = word[2:]
    if first_half == "ch":
        return 1
    if "ch" in second_half:
        return 2
    if first_half == "sh":
        return 3
    if "sh" in second_half:
        return 4
    return 0
def generate_number_tier(original_file, mode='d'):
    '''

    :param original_file:
    :param mode: Sets mode to [d]efault or [alt]ernate
    :return:
    '''
    line_buffer = 0 # Prevents us from copying the tier metadata. The program wants to add lines
                    # after reading the target tier name. However, there are lines underneath that we
                    # don't want to copy. Namely, xmin, xmax, etc. There are 4 of these lines.
    new_file = [] # The original file, copied
    number_tier = [] # The new tier to be added, represented as a list of boundaries
    token_count = {} # A dictionary of all the words and how many times each has occurred
    if mode == "alt":
        token_count = {"non-target": 0, "fricatives": 0, "affricates": 0}
    word_tier = False # A boolean to track whether or not the program has read up to the word tier
    for _, line in original_file.iterrows():
        line = line['data']
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
                    token = line[8:-1]
                    if token != "":
                        if mode == "d":
                            if token not in token_count:
                                token_count[token] = 1
                            else:
                                token_count[token] += 1
                            line = "text = \"" + str(token_count[token]) + "\""
                        if mode == "alt":
                            word_category = get_word_category(token)
                            if word_category == 0:
                                word_category = "non-target"
                            elif word_category in range(1,3):
                                word_category = "affricates"
                            else:
                                word_category = "fricatives"
                            token_count[word_category] += 1
                            line = "text = \"" + str(token_count[word_category]) + "\""
                number_tier.append(line)
    new_file.insert(2, "") # read_csv() seems to skip newlines. TextGrid files always have a newline for their
                           # third line.
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
    string_output = ""
    for line in new_file:
        string_output += line + "\n"
    for line in number_tier_metadata:
        string_output += line + "\n"
    for line in number_tier:
        string_output += line + "\n"
    return string_output
# Everything below is streamlit frontend
header = st.container()
body = st.container()
file_upload = st.container()
file_upload2 = st.container() # Necessary?
with header:
    st.title("Welcome to the Praat Number Tier generator")
    st.text("This program automatically counts words in Praat.")
with body:
    st.header("How it works")
    st.text("The input must be a .TextGrid or .txt, with a tier titled \"sentence - words\" \n"
            "being the last most tier. There can be any number of tiers above. The sentence - words\n"
            " tier must contain various words, each delimited by a pair of boundaries. The program \n"
            "will ignore empty intervals and create a new file, identical to the input file, but with\n"
            " an added Number tier. The Number tier will have the same boundaries as the sentence - \n"
            "words tier. For each interval with a word in it, the Number tier will contain a number \n"
            "corresponding to the amount of times that word has occurred, starting from 1.")
with file_upload:
    st.header("File input/output")
    input_file = st.file_uploader("Upload file:", type=["TextGrid"], key='default')
    if input_file is not None:
        input_csv = pandas.read_csv(input_file, names=['data'])
        output_file = generate_number_tier(input_csv)
        st.download_button(label="Output Download",data=output_file,file_name="PraatNumGen_Output.TextGrid")
with file_upload2:
    st.header("Alternate file input/output")
    input_file2 = st.file_uploader("Upload file:", type=["TextGrid"], key='alternate')
    if input_file2 is not None:
        input_csv = pandas.read_csv(input_file2, names=['data'])
        output_file = generate_number_tier(input_csv, mode='alt')
        st.download_button(label="Output Download", data=output_file, file_name="PraatNumGen_Output.TextGrid")
