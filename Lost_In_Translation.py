from nltk import word_tokenize,pos_tag,ne_chunk
from nltk.tokenize import RegexpTokenizer
import string

file_path = "english_dict.txt"
with open(file_path) as file:
    text_file = file.read()
all_words = word_tokenize(text_file)
all_words = [w.lower() for w in all_words]
punc_remover = RegexpTokenizer(r'\w+')
specific_tag = "NNP"
proper_nouns = set()
set_of_nnp = set()
temp = str()
incorrect_words = set()
corrected_words = set()
test_case = str()
max_distance = 0

test_cases = {"In April 2023, Sundar Pichai did announce that Google would be launehing a new AI product namcd Gemini. Barack Obama also gave a speech at Harvard University, cmphasizing the role of technology in modern education.","Project X is an exclusive elub at Veermata Jijabai Technological Institute, Mumbai, mcant to 5erve as a healthy environment for 5tudents to learn from each other and grow together. Through the guidance of their mcntors these 5tudents are able to complete daunting tasks in a relatively short time frame, gaining significant exposure and knowledge in their domain of choice.","I will be eompleting my BTech dcgree in Mechanical Engineering from VJTI in 2028","However the rcsults were clear"}

def words_tokenizer(str):
    return word_tokenize(str)

def punctuation_remover(str):
    return punc_remover.tokenize(str)

def pos_tagger(str):
    return pos_tag(str)

def nnp_tagger(str):
    return ne_chunk(str)

def word_corrector(a, all_words):
    return [w for w in all_words if one_substitution_match(a,w)]

def one_substitution_match(word1,word2):
    if len(word1) != len(word2):
        return False
    diff_count = sum(c1 != c2 for c1,c2 in zip(word1,word2))
    return diff_count == 1

for i in test_cases:
    test_case = str(i)
    words = words_tokenizer(i)
    no_punc_text = punctuation_remover(i)
    words_pos_tagged = pos_tagger(words)
    nnp_tagged = nnp_tagger(words_pos_tagged)
    
    for word,tag in words_pos_tagged:
        if tag == specific_tag:
            set_of_nnp.add(word)
            if temp in proper_nouns:
                proper_nouns.remove(temp)
                new = temp + " " + word
                proper_nouns.add(new)
            else:
                proper_nouns.add(word)
        temp = word
    print("PROPER NOUNS:")
    print(proper_nouns if proper_nouns else "[]")
    
    for i in no_punc_text:
        if i not in set_of_nnp:
            i = i.lower()
            if i not in all_words:
                if not i.isdigit():
                    incorrect_words.add(i)
    print("INCORRECT WORDS:")
    print(incorrect_words)

    for i in incorrect_words:
        if '5' in i:
            wrong = i
            i = i.replace('5','s')
            corrected_words.add(i)
            test_case = test_case.replace(wrong,i)
        elif '0' in i:
            wrong = i
            i = i.replace('0','o')
            corrected_words.add(i)
            test_case = test_case.replace(wrong,i)
        else:
            wrong = i
            possible_words = [w for w in all_words if len(w) == len(i) and one_substitution_match(i,w)]
            corrected_words.add(possible_words[0] if possible_words else i)
            i = possible_words[0] if possible_words else i
            test_case = test_case.replace(wrong,i)
    print("CORRECTED WORDS:")
    print(corrected_words)

    words.clear()
    no_punc_text.clear()
    words_pos_tagged.clear()
    nnp_tagged.clear()
    proper_nouns.clear()
    incorrect_words.clear()
    corrected_words.clear()

    print("CORRECTED SENTENCE:")
    if test_case[-1] not in string.punctuation:
        test_case = test_case + '.'
    if "however" in test_case:
        test_case = test_case.replace("however","however,")
    if "However" in test_case:
        test_case = test_case.replace("However","However,")
    print(test_case)
    print("\n")