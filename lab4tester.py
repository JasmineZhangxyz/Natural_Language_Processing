import lab4

#file_name = 'test_text_parsing.txt'
#print(lab4.parse_story(file_name))

#ahh = lab4.get_prob_from_count([10, 20, 40, 30])
#print(ahh)

#words = ["the", "child", "will", "go", "out", "to", "play", ",", "and", "the", "child", "can", "not", "be", "sad", "anymore", "."]
# = lab4.build_ngram_counts(words, 2)
#print(run)

counts = {('i', 'love'): [['js', 'py3', 'c', 'no'], [20, 20, 10, 2]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}
ahh = lab4.prune_ngram_counts(counts, 3)
print(ahh)

#counts = {('i', 'love'): [['js', 'py3', 'c'], [20, 20, 10]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}
#argh = lab4.probify_ngram_counts(counts)
#print(argh)

#words = ['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'will', 'the', 'child', 'may', 'go', 'home', '.']
#pls_work = lab4.build_ngram_model(words, 2)
#print(pls_work)

#im_tired = lab4.gen_bot_list(pls_work, ('the', 'child'), 5)
#print(im_tired)

#token_list = ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.']
#sleep = lab4.gen_bot_text(token_list, False)
#print(sleep)
