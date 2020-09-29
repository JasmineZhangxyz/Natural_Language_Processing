import utilities

def parse_story(file_name):
	"""
	(file) -> (list)
	Function separates sentences into individual tokens made of individual words. Valid punctuation are considered their own separate 		token from the word they're attached to. Bad characters (weird punctuation) are remvoved.

	>>> parse_story('test_text_parsing.txt')
	['the', 'code', 'should', 'handle', 'correctly', 'the',
	'following', ':', 'white', 'space', '.', 'sequences', 'of',
	'punctuation', 'marks', '?', '!', '!', 'periods', 'with',
	'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a',
	"don't", 'worry', 'about', 'numbers', 'like', '1', '.', '5',
	'remove', 'capitalization']

	"""
        
	#read file
	rfile = open(file_name, 'r')
	contents = rfile.read()

	#turn file into list of words separated by white space
	file_list = contents.split()

	#set up list
	working_list = []
	
	#run through characters
	for word in file_list:
		temporary = []
		for character in word:
			temporary.append(character)
			#separate punctuation
			for punctuation in ['?', '.' , '!', ',', ':', ';']:  #import utilities here
				if character == punctuation:
					temporary.pop()
					gen = ('').join(temporary)
					working_list.append(gen)
					working_list.append(punctuation)
					temporary.clear()
		working_list.append(('').join(temporary))

	temporary = []
	final_list = []
	#get rid of invalid characters
	for word in working_list:
		for character in word:
			temporary.append(character)
			for invalid in ['"', "(", ")", "{", "}", "[", "]", "_"]:
				if character == invalid:
					temporary.pop()
					gen = ('').join(temporary)
					#gen = gen.lower() #lower case
					final_list.append(gen)
		gen = ('').join(temporary)
		gen = gen.lower()
		final_list.append(gen)
		temporary.clear()

	#removing blanks that show up... why??
	number_of_blanks = final_list.count('')
	while number_of_blanks > 0:
		number_of_blanks -= 1
		final_list.remove('')

	return final_list
				
def get_prob_from_count(counts):
	"""
	(list) -> (list)
	Returns a list of probabilities from counts

	>>> get_prob_from_count([10, 20, 40, 30])
	[0.1, 0.2, 0.4, 0.3]
	
	"""
	#set up
	total = 0
	probability_list = []
	
	for number in counts:
		total += number
	for number in counts:
		probability_list.append(number/total)

	return probability_list

def build_ngram_counts(words, n):
	"""
	(list, int) -> (dictionary)
	Returns a dictionary of n-grams and the counts of the words that follow the n-gram.
	The key of the dictionary will be the N-gram in a tuple.
	The corresponding value will be a list containing two lists.
	The first list contains the words and the second list contains the corresponding counts.

	>>> words = [‘the’, ‘child’, ‘will’, ‘go’, ‘out’, ‘to’, ‘play’, ‘,’, ‘and’, ‘the’, ‘child’, ‘can’, ‘not’, ‘be’, ‘sad’, ‘anymore’, 		‘.’]
		>>> build_ngram_counts(words, 2)	{
				(‘the’, ‘child’): [[‘will’, ‘can’], [1, 1]],
		(‘child’, ‘will’): [[‘go’], [1]],		(‘will’, ‘go’): [[‘out’], [1]],		(‘go’, out’): [[‘to’], [1]],		(‘out’, ‘to’): [[‘play’], [1]],
		(‘to’, ‘play’): [[‘,’], [1]],
		(‘play’, ‘,’): [[‘and’], [1]],
		(‘,’, ‘and’): [[‘the’], [1]],
		(‘and’, ‘the’): [[‘child’], [1]],
		(‘child’, ‘can’): [[‘not’], [1]],
		(‘can’, ‘not’): [[‘be’], [1]],
		(‘not’, ‘be’): [[‘sad’], [1]],
		(‘be’, ‘sad’): [[‘anymore’], [1]],
		(‘sad’, ‘anymore’): [[‘.’], [1]]
	}
	
	"""

	word_count = len(words)
	dic = {} #dictionary

	#make dictionary with duplicate values
	for i in range(word_count - 2):
		temp_list = [] #will carry values of words that come after
		counting = [] #will count how many times
		for j in range(word_count - 2):
			if words[i] + words[i+1] == words[j] + words[j+1]:
				temp_list.append(words[j+2])
				counting.append(1)
		dic[(words[i], words[i+1])] = (temp_list, counting)
		
		#combine duplicates
		for gram in dic:
			glist = dic[gram]
			number_of_elements = len(glist[0])
			while_number = 0
			repeats = 0
			while while_number < number_of_elements:
				dup_word = glist[0].count(glist[0][while_number])
				index_list = []
				if (dup_word > 1): #if duplicates exist
					glist[1][while_number] += (dup_word - 1)
					index_list = [x for x in range(len(glist[0])) if glist[0][x] == glist[0][while_number]]
					index_list.pop(0)
					for index in index_list:
						glist[0].pop(index)
						for item in range(len((index_list))):
							index_list[item] -= 1
						repeats += 1
						glist[1].pop(index)
					number_of_elements -= repeats
					while_number += 1
				#no duplicates
				else:
					while_number += 1
	return dic

def prune_ngram_counts(counts, prune_len):
	"""
	(dictionary, int) -> (dictionary)
	Returns a dictionary of n-grams and the counts of the words that follow the n-gram.
	The lower frequency words will be removed based on the prune_len.

	>>> ngram_counts = {
		(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’, ‘no’], [20, 20, 10, 2]],
		(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],
		('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]
	}
	>>> prune_ngram_counts(ngram_counts, 3)
	{
		(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]],
		(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],
		('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]
	}
	"""
	#new dictionary
	new_counts = counts.copy()

	for item in counts: #goes through key_value one-by-one
		associated_lst = counts[item] #names the list that is associated to the item key
			
		new_lst1 = []
		new_lst2 = []		
		new_new_lst1 = []
		new_new_lst2 = []
		final_new_lst = [[], []]
		lst2, lst1 = zip(*sorted(zip(associated_lst[1], associated_lst[0])))
		for i in range(len(associated_lst[0])):
			final_new_lst[0].append(lst1[i])
			final_new_lst[1].append(lst2[i])
		final_new_lst[0].reverse() #decending order
		final_new_lst[1].reverse()
		if len(associated_lst[0]) <= prune_len:
			continue
		else:
			cut_off_num = final_new_lst[1][prune_len - 1]
			j = len(final_new_lst[1]) - 1
			while j  >= prune_len and j <= (len(final_new_lst[1])):
				if final_new_lst[1][j] == cut_off_num:
					break
				else:
					final_new_lst[0].pop()
					final_new_lst[1].pop()
				j -= 1
		new_counts[item] = final_new_lst	
	return new_counts	

def probify_ngram_counts(counts):
	"""
	(dictionary) -> (dictionary)
	Returns a dictionary with probability of each word.

	>>> ngram_counts = {
		(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]],
		(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]],
		('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]
	}
	>>> probify_ngram_counts(ngram_counts)
	{
		(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [0.4, 0.4, 0.2]],
		(‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [0.32, 0.28, 0.2, 0.2]],
		('toronto’, ‘is’): [[‘six’, ‘drake’], [0.4, 0.6]]
	}
	"""
	#set up new dictionary
	probify = counts.copy()
	
	for item in counts: #iterate through given dictionary
		associated_lst = counts[item]
		just_counts = associated_lst[1] #list of counts of words
		sum_of_counts = 0 #sum of all counts
		prob = [] #new prob list to replace just_counts list
		for count in just_counts:
			sum_of_counts += count
		for count in just_counts:
			prob.append(count/sum_of_counts)
		#del associated_lst[-1]
		#associated_lst.append(prob)
		probify[item] = [associated_lst[0], prob]
	return probify

def build_ngram_model(words, n):
	"""
	(list, int) -> (dictionary)
	Creates and returns a dictionary following format of probify_ngram_counts(counts).
	Keeps 15 most likely words that follow an N-gram (prune_len = 15)
	Words will appear in decending order of probability

	>>> words = [‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘can’, ‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘may’, ‘go’, ‘home’, ‘.’]
	>>> build_ngram_model(words, 2)
	{
		(‘the’, ‘child’): [[‘will’, ‘can’, ‘may’], [0.5, 0.25, 0.25]],
		(‘child’, ‘will’): [[‘the’], [1.0]],
		(‘will’, ‘the’): [[‘child’], [1.0]],
		(‘child’, ‘can’): [[‘the’], [1.0]],
		(‘can’, ‘the’): [[‘child’], [1.0]],
		(‘child’, ‘may’): [[‘go’], [1.0]],
		(‘may’, ‘go’): [[‘home’], [1.0]],
		(‘go’, ‘home’): [[‘.’], [1.0]]
	}
	"""
	unaltered_counts = build_ngram_counts(words, n)
	pruned_counts = prune_ngram_counts(unaltered_counts, 15)
	final_prob = probify_ngram_counts(pruned_counts)
	return final_prob	

def gen_bot_list(ngram_model, seed, num_tokens=0):
	"""
	(dictionary, tuple, positive int) -> (list)
	ngram_model is in the same format as the outut of build_ngram_model
	seed is  a tuple of strings representing the first N tokens in the list
	num_tokens is a positive int representing the limit of number of tokens to be put in the list
	Returns a randomly generated list of tokens (strings) that starts with the N tokens in seed, selecting all subsequent tokens 		using gen_next_tokens (utilities).
	if seed > num_tokens in length, then the returned list will contain the first num_tokens of the seed
	Should be 

	>>> ngram_model = {('the', 'child'): [['will', 'can','may'],[0.5, 0.25, 0.25]], \
		('child', 'will'): [['the'], [1.0]], \
		('will', 'the'): [['child'], [1.0]], \
		('child', 'can'): [['the'], [1.0]], \
		('can', 'the'): [['child'], [1.0]], \
		('child', 'may'): [['go'], [1.0]], \
		('may', 'go'): [['home'], [1.0]], \
		('go', 'home'): [['.'], [1.0]] \
		}
	>>> random.seed(10)
	>>> gen_bot_list(ngram_model, ('hello', 'world'))
	[]
	>>> gen_bot_list(ngram_model, ('hello', 'world'), 5)
	['hello', 'world']
	>>> gen_bot_list(ngram_model, ('the', 'child'), 5)
	['the', 'child', 'can']
	Note that the removal of the crossed out ('child', 'can') 2-gram is the reason for
	the termination.
	>>> gen_bot_list(ngram_model, ('the', 'child'), 5)
	['the', 'child', 'will', 'the', 'child']
	"""
	#set up output list
	final_list = []
	current_ngram = list(seed)
	#deal with extraneous cases
	if num_tokens == 0:
		return final_list
	elif len(seed) > num_tokens:
		for i in range(0, num_tokens):
			final_list.append(seed[i])
	#deal with regular case
	else:
		for word in seed:
			final_list.append(word)
		presence = ngram_model.__contains__(seed) #returns boolean for whether a key is in a dictionary
		if presence == False:
			return final_list
		else:
			print()
		while len(final_list) < num_tokens: #continued iteration until num_tokens fulfilled
			new_word = utilities.gen_next_token(tuple(current_ngram), ngram_model) #chooses random next word
			final_list.append(new_word)
			#change current_ngram to be... current
			current_ngram.pop(0)
			current_ngram.append(new_word)
			#keep iterating
			if (ngram_model.__contains__(tuple(current_ngram))) == True:
				continue
			else:
				return final_list
	return final_list

def gen_bot_text(token_list, bad_author):
	"""
	(list, boolean) -> (string)
	if bad_author == True, a string containing all tokens in token_list, separated by a space is returned
	if bad_author == False, the string will have correct punctuation spacing and capitalization.
	>>> token_list = ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.']
	>>> gen_bot_text(token_list, False)
	'This is a string of text. Which needs to be created.'
	>>> token_list = parse_story("308.txt")
	>>> text = gen_bot_text(token_list, False)
	>>> write_story('test_gen_bot_text_student.txt', text, 'Three
	Men in a Boat', 'Jerome K. Jerome', 'Jerome K. Jerome', 1889)
	"""
	new_string = " "
	output_string = ""
	if bad_author == True:
		output_string = new_string.join(token_list)
		return output_string
	else:
		#remove all capitalization
		decap_list = []
		for item in token_list:
			decap_list.append(item.lower())
		cap_list = decap_list.copy()
		for d in range(0, len(decap_list)):
			if decap_list[d].capitalize() in utilities.ALWAYS_CAPITALIZE:
				cap_list[d] = decap_list[d].capitalize()
		for d_index in range(0, (len(cap_list) - 1)):
			if decap_list[d_index] in utilities.END_OF_SENTENCE_PUNCTUATION:
				cap_list[d_index + 1] = decap_list[d_index + 1].capitalize()
				print("pls work")
		cap_list[0] = decap_list[0].capitalize()
		#combine weird strings
		for item in cap_list:
			if item in utilities.VALID_PUNCTUATION:
				output_string += item
			elif cap_list[0] == item:
				output_string += item
			else:
				output_string = output_string + " " + item
	return output_string
#file_name = 'test_text_parsing.txt'
#print(parse_story(file_name))

#ahh = get_prob_from_count([10, 20, 40, 30])
#print(ahh)

#words = ["the", "child", "will", "go", "out", "to", "play", ",", "and", "the", "child", "can", "not", "be", "sad", "anymore", "."]
#run = build_ngram_counts(words, 2)
#print(run)

#counts = {('i', 'love'): [['js', 'py3', 'c', 'no'], [20, 20, 10, 2]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}
#ahh = prune_ngram_counts(counts, 3)
#print(ahh)

#counts = {('i', 'love'): [['js', 'py3', 'c'], [20, 20, 10]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}
#argh = probify_ngram_counts(counts)
#print(argh)

#words = ['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'will', 'the', 'child', 'may', 'go', 'home', '.']
#pls_work = build_ngram_model(words, 2)
#print(pls_work)

#im_tired = gen_bot_list(pls_work, ('the', 'child'), 5)
#print(im_tired)

#token_list = ['this', 'is', 'a', 'string', 'of', 'text', '.', 'which', 'needs', 'to', 'be', 'created', '.']
#sleep = gen_bot_text(token_list, False)
#print(sleep)
