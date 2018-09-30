#!/usr/bin/env python

def parse_data(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close
	
	#print(lines)
	sequences = []
	for line in lines:
		# print(line)
		itemsets= []
		line = line.strip()
		line = line.strip('<')
		line = line.strip()
		line = line.split('>')
		# print (line[0])

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
	
	# print(sequences)
	return sequences


def parse_supports(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close

	dictionary = {}
	# print(lines)
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

	# print(dictionary)
	# print (threshold)
	return dictionary, threshold

def ms_gsp(s, min_supp, n, threshold):
	m = sort()
	l = init_pass(m, s)
	
	# for i in range(len(l)):
		# print l[i], supp(l[i])
	
	c =lvl2_candidate_gen(l, min_supp, n, threshold)
	print c

def sort():
	pass

def supp(val):
	count = 0
	s = parse_data('data.txt')
	for i in range(len(s)):
		for j in range(len(s[i])):
			for k in range(len(s[i][j])):
				if s[i][j][k] == str(val):
					count += 1
					break
			if count != 0:
				break

	return (float(count) / len(s))

def init_pass(m, s):
	return [10, 30, 40, 50, 70, 80, 90]

def lvl2_candidate_gen(f, min_supp, n, val):
	candidate_list = []

	for i in range(len(f)):
		if str(f[i]) in min_supp.keys():
			min_supp_i = min_supp[str(f[i])]
		else:
			min_supp_i = 0.0

		if supp(f[i]) >= min_supp_i: # array index could be different
			for j in range(i + 1, len(f)):
				if str(f[j]) in min_supp.keys():
                        		min_supp_j = min_supp[str(f[j])]
                		else: 
                        		min_supp_j = 0.0
				if supp(f[j]) >= min_supp_i and (abs(supp(f[j]) - supp(f[i])) <= val):
					candidate_list.append([f[i], f[j]])
	return candidate_list

def ms_candidate_gen():
	pass

def main():
	s = parse_data('data.txt')
	min_supp, threshold = parse_supports('supports.txt')
	n = len(s)
	
	ms_gsp(s, min_supp, n, threshold)

if __name__ == "__main__":
	main()
