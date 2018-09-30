#!/usr/bin/env python

def parse_data(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	f.close
	I =[]
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
	#print(lines)
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

def ms_gsp(s, min_supp):
	m = sort()
	l = init_pass(m, s)

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

def init_pass(m, s):
	pass

def lvl2_candidate_gen():
	pass

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
