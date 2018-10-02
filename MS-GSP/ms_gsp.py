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


	# print(I)
	# print(sequences)
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

	# print(dictionary)
	# print (sdc)
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

def ms_gsp(S, I, min_supp, sdc):

	sorted_items, sorted_minsup = sort(I, min_supp)
	L, support_count = init_pass(sorted_items, S, sorted_minsup)

	F1 = []

	for element in L:
		index = sorted_items.index(element)
		if(support_count[index]/len(S) >= sorted_minsup[index]):
			F1.append(element)

	print(F1)

	n = len(S)
	c =lvl2_candidate_gen(L, min_supp, n, sdc)
	print ("LVL2 candidate gen:  ", c)

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
	s, _ = parse_data('data.txt')
	for i in range(len(s)):
		for j in range(len(s[i])):
			for k in range(len(s[i][j])):
				if s[i][j][k] == str(val):
					count += 1
					break
			if count != 0:
				break

	return (float(count) / len(s))

def init_pass(m, s, sorted_minsup):
	print('init pass')
	print(m)

	support_count = []
	for item in m:
		#print(item)
		support = 0
		for sequence in s:
			for itemset in sequence:
				if(item in itemset):
					support = support + 1
					break
			#print(sequence)
		support_count.append(support) 
	print(support_count)
	print(sorted_minsup)

	L = []
	counter = True
	check = True
	for item in m:
		index = m.index(item)
		
		if(counter):
			if((support_count[index]/len(s)) >= sorted_minsup[index]):
				L.append(item)
				mis_i = sorted_minsup[index]
				counter = False
				continue
			else:
				continue
		
		if(support_count[index]/len(s) >= mis_i):
			L.append(item)


	print('printing L: ')
	print(L)

	return L, support_count

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

def calc_len(a):
	l = 0
	for i in range(len(a)):
		for j in range(len(a[i])):
			l += 1
	return l

def ms_candidate_gen(fk_1, min_supp):

	candidate_set = []
	for i in range(len(fk_1)):
		s_1 = fk_1[i]
		size_s_1 = len(s_1)
		len_s_1 = calc_len(s_1)
		s_1_copy = s_1

		for j in range(i, len(fk_1)):
			s_2 = fk_1[j]
			s_2_copy = s_2
			size_s_2 = len(s_2)
			len_s_2 = calc_len(s_2)
			flag_s_1 = True
			flag_s_2 = True

			for k_1 in range(len(s_1)):
				for k_2 in range(len(s_1[k_1])):
					if min_supp[str(s_1[0][0])] >= min_supp[str(s_1[k_1][k_2])]:
						flag_s_1 = False

			for k_1 in range(len(s_2)):
				for k_2 in range(len(s_2[k_1])):
					if min_supp[str(s_2[-1][-1])] >= min_supp[str(s_2[k_1][k_2])]:
						flag_s_2 = False

			if flag_s_1:
				if len(s_1_copy[0]) >= 2:
					second_s_1 = s_1_copy[0].pop(1)
				else:
					second_s_1 = s_1_copy[1].pop(0)

				last_s_2 = s_2_copy[-1].pop()
				is_seperate_s_2 = False

				if len(s_1_copy[0]) == 0:
					s_1_copy.pop(0)

				if len(s_2_copy[-1]) == 0:
					s_2_copy.pop()
					is_seperate_s_2 = True

				if (s_1_copy == s_2_copy) and (min_supp[str(last_s_2)] > min_supp[str(s_1[0][0])]):
					last_s_1 = s_1_copy[-1].pop()
					if is_seperate_s_2:
						s_1.append(last_s_2)
						candidate_set.append(s_1)
						s_1.pop()
						if (len_s_1 == 2 and size_s_1 == 2) and (last_s_2 > last_s_1):
							s_1[-1].append(last_s_2)
							candidate_set.append(s_1)
					elif (((len_s_1 == 2 and size_s_1 == 1) and (last_s_2 > last_s_1)) or (len_s_1 > 2)):
						s_1[-1].append(last_s_2)
						candidate_set.append(s_1)

			elif flag_s_2:
				if len(s_1_copy[-1]) >= 2:
					last_second_s_1 = s_1_copy[-1].pop(-2)
				else:
					last_second_s_1 = s_1_copy[-2].pop()
				first_s_2 = s_2_copy[0].pop(0)
				is_seperate_s_1 = False

				if len(s_1[0][0]) == 1:
					is_seperate_s_1 = True

				if len(s_1_copy[-2]) == 0:
					s_1_copy.pop(-2)

				if len(s_2_copy[0]) == 0:
					s_2_copy.pop(0)

				#	first s1<last s2
				if (s_1_copy == s_2_copy) and min_supp[str(s1[0][0])] < min_supp[s_2[-1][-1]]:
					last_s_1 = s_1_copy[-1].pop()
					if is_seperate_s_1:
						s_2 = [[s_1[0][0]]] + s_2
						candidate_set.append(s_2)
						s_2.pop(0)
						if len_s_2 == 2 and size_s_2 == 2 and first_s_1 < first_s_2:
							s_2[0] = s_1[0][0] + s_2[0]
							candidate_set.append(s_2)
					elif (((len_s_2 == 2 and size_s_2 == 1) and (first_s_1 < first_s_2)) or (len_s_2 > 2)):
						s_2[0] = s_1[0][0] + s_2[0]
						candidate_set.append(s_2)
			else:
				first_s_1 = s_1_copy[0].pop(0)
				last_s_2 = s_2_copy[-1].pop()
				is_seperate = True

				if len(s_1_copy[0]) == 0:
					s_1_copy.pop(0)

				if len(s_2_copy[-1]) == 0:
					s_2_copy.pop()
				else:
					is_seperate = False

				if s_1_copy == s_2_copy:
					if is_seperate:
						s_1.append([last_s_2])
					else:
						s_1[-1].append(last_s_2)
					candidate_set.append(s_1)

	return candidate_set

def main():
	sequences, I = parse_data('data.txt')
	min_supp, sdc = parse_supports('supports.txt')

	ms_gsp(sequences, I, min_supp, sdc)

if __name__ == "__main__":
	main()
