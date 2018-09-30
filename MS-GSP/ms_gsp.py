#!/usr/bin/env python

def parse_data(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close
	
	#print(lines)
	sequences = []
	for line in lines:
		print(line)
		itemsets= []
		line = line.strip()
		line = line.strip('<')
		line = line.strip()
		line = line.split('>')
		print (line[0])

		line = line[0].split('{')
		#print(line)

		sequence = []
		for b in line:
			if(b != ''):
				b = b.strip()
				b = b.split('}')
				b = b[0].split(',')

				itemset = []
				for i in b:
					if(i!=''):
						itemset.append(i.strip())
				sequence.append(itemset)
		sequences.append(sequence)
	
	print(sequences)
	return sequences


def parse_supports(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close

	dictionary = {}
	#print(lines)
	for line in lines:
		line = line.strip()
		line = line.split('=')

		element1 = line[0].strip()
		element2 = line[1].strip()

		if(element1 == 'SDC'):
			threshold = element2
		else:
			element1 = element1.split('(')
			element1 = element1[1].split(')')
			item = element1[0].strip()
			dictionary[item] = element2

	print(dictionary)
	print (threshold)
	return dictionary, threshold

def ms_gsp(s, min_supp, n):
	m = sort()
	l = init_pass(m, s)
	lvl2_candidate_gen(l, min_supp, n, val)

def sort():
	pass

def init_pass(m, s):
	pass

def lvl2_candidate_gen(f, min_supp, n, val):
	candidate_list = []

	for i in range(len(f):
		if supp(f[i]) >= min_supp[f[i]] # array index could be different
			for j in range(i + 1, len(f)):
				if supp(f[j]) >= min_supp[str(f[j])] and ((supp(f[j]) - supp(f[i])) <= val):
					candidate_list.append([f[i], f[j]])
	return candidate_list

def ms_candidate_gen():
	pass

def main():
	min_supp = []
	s = []
	parse_data('data.txt')
	parse_supports('supports.txt')
	n = 0
	ms_gsp(s, min_supp, n)

if __name__ == "__main__":
	main()
