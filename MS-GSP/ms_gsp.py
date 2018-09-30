#!/usr/bin/env python

def parse_data(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close
	I =[]
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
						if(i.strip() not in I):
							I.append(i.strip())
				sequence.append(itemset)
		sequences.append(sequence)


	print(I)
	print(sequences)
	return sequences , I

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
			sdc = element2
		else:
			element1 = element1.split('(')
			element1 = element1[1].split(')')
			item = element1[0].strip()
			dictionary[item] = float(element2)

	print(dictionary)
	print (sdc)
	return dictionary, sdc

def pack_sequence(sequence):
	#[[10,40],[50]]
	seq = '<'
	for element in sequence:
		#[10,40]
		itemset = '{'
		for el in element:
			#10
			itemset = itemset + str(el) + ' '
		itemset = itemset + '}'
		seq = seq + itemset
	seq = seq + '>'
	print(seq)
	return seq

def ms_gsp(s, min_supp, n, threshold):

	m = sort()
	l = init_pass(m, s)
	
	# for i in range(len(l)):
		# print l[i], supp(l[i])
	
	c =lvl2_candidate_gen(l, min_supp, n, threshold)
	print c

def sort(I,MIS):
	
	for i in I :
		if(i not in MIS):
			MIS[str(i)] = 0.0

	s = sorted(MIS.items(), key=lambda x: x[1])
	
	sorted_items = []
	sorted_minsup = []
	
	for i in s:
		sorted_items.append(i[0]) 
		sorted_minsup.append(i[1])
	#print(sorted_items)
	#print(sorted_minsup)
	return sorted_items, sorted_minsup

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
	min_supp = []
	s = []
	#ms_gsp(s, min_supp)
	sequences, I = parse_data('data.txt')
	mis, sdc = parse_supports('supports.txt')
	#pack_sequence([[10,40],[50]])
	sort(I, mis)

if __name__ == "__main__":
	main()
