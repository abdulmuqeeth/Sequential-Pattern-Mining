
import copy

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
	return dictionary, float(sdc)

def pack_sequence(sequence):
	#[[10,40],[50]]
	seq = '<'
	for element in sequence:
		#[10,40]
		itemset = '{'
		for el in element:
			#10
			itemset = itemset + str(el) + ','
			if(element.index(el)==len(element)-1):
				itemset = itemset[:-1]
		itemset = itemset + '}'
		seq = seq + itemset
	seq = seq + '>'
	print(seq)
	return seq


def cand_min_mis_item(c, min_supp):
	# print('########')
	# print(c)
	min_value = 9999
	for itemset in c:
		for item in itemset:

			# print(item)
			if(min_supp[str(item)]< min_value):
				min_value = min_supp[str(item)]

	return min_value

# def contains_old(candidate, sequence):
# 	flag = None
# 	for itemset in candidate:
# 		for itemset_seq in sequence:
# 			if(set(itemset) <= set(itemset_seq)):
# 				sequence.pop(sequence.index(itemset_seq))
# 				flag = True
# 				break
# 			else:
# 				flag = False
# 		if(not flag):
# 			continue
# 		else:
# 			return False
# 	return True

def contains(c1,s1):
    
    c = copy.deepcopy(c1)
    s = copy.deepcopy(s1)
    for i in range(0, len(s)):
        s[i].sort
    for j in range(0,len(c)):
        c[j].sort
    #print('s sequence:', s)
    #print('c sequence', c)
    
    length_c = len(c)
    count = 0
    
    for i in range(len(c)):
        k = 0
        #print('checking: ', c[i])
        while(len(s)!=0 or k != len(s)):
            #print('checking in sqeuence itemset', s[k], 'for ', c[i])
            if(set(c[i]).issubset(set(s[k]))):
                s.pop(k)
                count = count +1
                #print('found')
                #print('new s', s)
                if(i==len(c)-1 and len(s)==0):
                    return True
                break
            else:
                #print('not found here')
                k = k + 1
                #print('in else len of s=',len(s), ' k=',k)
                if(k==len(s)):
                    return False
    if(len(s)==0):
        return False
    else:
        return True


def ms_gsp(S, I, min_supp, sdc):

	sorted_items, sorted_minsup = sort(I, min_supp)
	L, support_count = init_pass(sorted_items, S, sorted_minsup)
	F = []
	k = 2
	f_1 = []

	least_minsup_item = sorted_items[0]
	for element in L:
		index = sorted_items.index(element)
		if(support_count[index]/len(S) >= sorted_minsup[index]):
			f_1.append([element])

	# print(f_1)
	F.append(f_1)

	

	n = len(S)
	while(len(F[k-2]) != 0):
		if k == 2:
			C =lvl2_candidate_gen(L, min_supp, n, sdc, support_count, sorted_items)
			print ("LVL2 candidate gen:  ", C)
		else:
			#print("#############")
			C = ms_candidate_gen(F[k-2], min_supp, least_minsup_item)

		# print('&&&&&$$$$$$$$')
		# print(C)
		candidate_count = [0 for i in range(len(C))] 
		for sequence in S:
			for candidate in C:
				#print('$$$$$$$$$$$$$$$$')
				if(contains(candidate, sequence)):
					candidate_count[C.index(candidate)] += 1

		f = []
		# count_c = []
		for candidate in C:
			if( candidate_count[C.index(candidate)]/n >= cand_min_mis_item(candidate,min_supp )):
				f.append(candidate)
				# count_c.append(candidate_count[C.index(candidate)])
		# print(count_c)
		F.append(f)
		k = k + 1
		print("-------------", f)
		with open('output.txt', 'w') as file:
			for seq in f:
				file.write("%s\n" % pack_sequence(seq))


	return F

def sort(I, MIS):
	
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

# def supp(val):
# 	count = 0
# 	s, _ = parse_data('data.txt')
# 	for i in range(len(s)):
# 		for j in range(len(s[i])):
# 			for k in range(len(s[i][j])):
# 				if s[i][j][k] == str(val):
# 					count += 1
# 					break
# 			if count != 0:
# 				break

	return (float(count) / len(s))

def init_pass(m, s, sorted_minsup):
	print('init pass')
	# print('m: ', m)

	n = len(s)

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
	#print(support_count)
	#print(sorted_minsup)

	L = []
	counter = True
	check = True
	for item in m:
		#print('item checked: ', item)
		index = m.index(item)
		#print('index of item in m: ', index)
		#print('sorted_minsup : ', sorted_minsup)
		#print(type(sorted_minsup[0]))
		if(counter):
			if(support_count[index]/n >= sorted_minsup[index]):
				print('First item being appended :', item)
				L.append(item)
				mis_i = sorted_minsup[index]
				counter = False
				continue
			else:
				continue
		
		#print('indexes after first item', index)
		#print('min_sup for compare: ', mis_i)
		#print('support count of item :', support_count[index])
		#print('len of s: ', n )
		#print('support : ', support_count[index]/n)
		if(support_count[index]/n >= mis_i):
			L.append(item)
			#print('items appended: ', item)



	print('printing L: ')
	print(L)

	return L, support_count

def lvl2_candidate_gen(L, min_supp, n, sdc, support_count, sorted_items):
	candidate_list = []

	for i in range(len(L)):

		if str(L[i]) in min_supp.keys():
			min_supp_i = min_supp[str(L[i])]
		else:
			min_supp_i = 0.0

		print('Min supp of :',L[i],'=',min_supp_i)

		index_i = sorted_items.index(L[i])
		print('index of ', L[i], 'from initial array= ', index_i)
		supp_i = support_count[index_i]/n
		print('support', L[i], '=', supp_i)
 

		if supp_i >= min_supp_i: # array index could be different
			for j in range(i + 1, len(L)):
				if str(L[j]) in min_supp.keys():
					min_supp_j = min_supp[str(L[j])]
				else:
					min_supp_j = 0.0

				index_j = sorted_items.index(L[j])
				#print('INDEX J: ',index_j)
				supp_j = support_count[index_j]/n
				
				#SHOULD we use what TA suggested?
				if supp_j >= min_supp_i and (abs(supp_j - supp_i) <= sdc):
					if(min_supp_j == min_supp_i):
						candidate_list.append([ [L[i],L[j]] ])
						#candidate_list.append([[L[j],L[i]]])

						candidate_list.append([ [L[i]] ,[L[j]] ])
						#candidate_list.append([ [L[j]],[L[i]] ])
					else:
						candidate_list.append([[L[i],L[j]]])
						candidate_list.append([[L[i]],[L[j]]])
	print('L2 candidates--------------', candidate_list)
	return candidate_list

def calc_len(a):
	l = 0
	for i in range(len(a)):
		for j in range(len(a[i])):
			l += 1
	return l

def gen_sub_sequences(s):
	# print('GEN SUB_SEQUENCES', s)
	l = calc_len(s)
	sub_seq_set = []
	for i in range(len(s)):
		for j in range(len(s[i])):
			for k in range(len(s[i][j])):
				# print("i, j, k = ", i , j , k)
				sub_seq = copy.deepcopy(s[i])
				# print ("current work seq", sub_seq[j])
				sub_seq[j].pop(k)
				# print("sub_seq=   ", sub_seq)
				sub_seq_set.append(sub_seq)
	# print(sub_seq_set)

	for i in range(len(sub_seq_set)):
		for j in range(len(sub_seq_set[i])):
			if(len(sub_seq_set[i][j]) == 0):
				break
		if len(sub_seq_set[i][j]) == 0:
			sub_seq_set[i].pop(j)

	# print (sub_seq_set)
	return sub_seq_set


def ms_candidate_gen(fk_12, min_supp, least_minsup_item):
	print('---------RUN---')
	fk_1 = copy.deepcopy(fk_12)
	candidate_set = []
	print(fk_12)
	for i in range(len(fk_12)):
		s_1 = copy.deepcopy(fk_12[i])
		size_s_1 = len(s_1)
		len_s_1 = calc_len(s_1)
		s_1_copy = copy.deepcopy(fk_12[i])
		s_1_copy_else = copy.deepcopy(fk_12[i])
		print(s_1_copy_else)
		print('####')
				

		# print("S1 COPY :" , s_1_copy)

		for j in range(i+1, len(fk_12)):
			#print('---------FK12 @@@',fk_1)
			s_1 = copy.deepcopy(fk_12[i])
			s_2 = copy.deepcopy(fk_12[j])
			s_1_copy = copy.deepcopy(fk_12[i])
			s_2_copy = copy.deepcopy(fk_12[j])
			s_2_copy_else = copy.deepcopy(fk_12[j])
			size_s_2 = len(s_2)
			len_s_2 = calc_len(s_2)
			flag_s_1 = True
			flag_s_2 = True
			print('s1 copy')
			print(s_1_copy)
			print('s2 copy')
			print(s_2_copy)
			# print('*****')
			# print(fk_1[i], fk_1[j])
			for k_1 in range(len(s_1)):
				for k_2 in range(len(s_1[k_1])):
					if(k_1==0 and k_2==0):
						continue
					if min_supp[str(s_1[0][0])] >= min_supp[str(s_1[k_1][k_2])]:
						flag_s_1 = False

			for k_1 in range(len(s_2)):
				for k_2 in range(len(s_2[k_1])):
					if(k_1 == len(s_2)-1 and k_2 == len(s_2[k_1])-1):
						continue
					if min_supp[str(s_2[-1][-1])] >= min_supp[str(s_2[k_1][k_2])]:
						flag_s_2 = False

			if flag_s_1:
				s_1_copy = copy.deepcopy(fk_12[i])
				s_2_copy = copy.deepcopy(fk_12[j])

				if len(s_1_copy[0]) >= 2:
					second_s_1 = s_1_copy[0].pop(1)
				else:
					if len(s_1_copy[1]) ==1:
						second_s1 = s_1_copy.pop(1)
						second_s1 = second_s1[0]
					else:
						second_s_1 = s_1_copy[1].pop(0)

				last_s_2 = s_2_copy[-1].pop()
				is_seperate_s_2 = False

				#if len(s_1_copy[0]) == 0:
					#s_1_copy.pop(0)

				if len(s_2_copy[-1]) == 0:
					s_2_copy.pop()
					is_seperate_s_2 = True

				if (s_1_copy == s_2_copy) and (min_supp[str(last_s_2)] > min_supp[str(s_1[0][0])]):
					last_s_1 = s_1_copy[-1].pop()
					if is_seperate_s_2:
						s_1.append([last_s_2])
						candidate_set.append(s_1)
						s_1.pop()
						if (len_s_1 == 2 and size_s_1 == 2) and (last_s_2 > last_s_1):
							s_1[-1].append(last_s_2)
							candidate_set.append(s_1)
							# s_1[-1].pop()
					elif (((len_s_1 == 2 and size_s_1 == 1) and (last_s_2 > last_s_1)) or (len_s_1 > 2)):
						s_1[-1].append(last_s_2)
						candidate_set.append(s_1)
						# s_1[-1].pop()

			elif flag_s_2:
				s_1_copy = copy.deepcopy(fk_12[i])
				s_2_copy = copy.deepcopy(fk_12[j])

				if len(s_2_copy[-1]) >= 2:
					last_second_s_2 = s_2_copy[-1].pop(-2)
				else:
					if(len(s_2_copy[-2]) == 1):
						last_second_s_2 = s_2_copy.pop(-2)
						last_second_s_2 = last_second_s_2[0]
					else:
						last_second_s_1 = s_1_copy[-2].pop()
				
				first_s_1 = s_1_copy[0].pop(0)
				is_seperate_s_1 = False

				if len(s_1[0][0]) == 1:
					is_seperate_s_1 = True
					s_1_copy.pop(0)

				# if len(s_1_copy[-2]) == 0:
				# 	s_1_copy.pop(-2)

				# if len(s_2_copy[0]) == 0:
				# 	s_2_copy.pop(0)

				#	first s1<last s2
				if (s_1_copy == s_2_copy) and min_supp[str(s1[0][0])] > min_supp[str(s_2[-1][-1])]:
					

					###last_s_1 = s_1_copy[-1].pop()
					first_s_2 = s_2[0][0]
					if is_seperate_s_1:
						s_2 = [[s_1[0][0]]] + s_2
						candidate_set.append(s_2)
						s_2.pop(0)
						if len_s_2 == 2 and size_s_2 == 2 and first_s_1 < first_s_2:
							s_2[0] = [s_1[0][0]] + s_2[0]
							candidate_set.append(s_2)
					elif (((len_s_2 == 2 and size_s_2 == 1) and (first_s_1 < first_s_2)) or (len_s_2 > 2)):
						s_2[0] = [s_1[0][0]] + s_2[0]
						candidate_set.append(s_2)
			else:
				s_1_copy_else = copy.deepcopy(fk_12[i])
				s_2_copy_else = copy.deepcopy(fk_12[j])

				check12 = [['30'],['40']]
				check13 = [['40','70']]
				print('s1 copy else',s_1_copy_else)
				print('s2 copy else',s_2_copy_else)				
				print('In else part')
				if(s_1_copy_else == check12 and s_2_copy_else==check13):
					print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
				#if()

				first_s_1 = s_1_copy_else[0].pop(0)
				last_s_2 = s_2_copy_else[-1].pop()
				is_seperate = True

				if len(s_1_copy_else[0]) == 0:
					s_1_copy_else.pop(0)

				if len(s_2_copy_else[-1]) == 0:
					s_2_copy_else.pop()
				else:
					is_seperate = False

				if s_1_copy_else == s_2_copy_else:
					if is_seperate:
						s_1.append([last_s_2])
					else:
						s_1[-1].append(last_s_2)
					candidate_set.append(s_1)

		# Prune step

		for candidate in candidate_set:
			# print("sub for each candidate ", candidate)
			sub_sequences = gen_sub_sequences([candidate])

			for i in range(len(sub_sequences)):
				contains_item = False
				for itemset in sub_sequences[i]:
					for item in itemset:
						if(item == least_minsup_item):
							contains_item = True

				if (contains_item and (sub_sequences[i] not in fk_12)):
					candidate_set.pop(candidate_set.index(candidate))
					break
	print('MS CAND GEN')
	print(candidate_set)
	return candidate_set

def main():
	sequences, I = parse_data('data.txt')
	I.sort()
	S = copy.deepcopy(sequences)
	n = len(S)
	print(len(S))
	min_supp, sdc = parse_supports('supports.txt')
	print(sequences)
	print(I)
	print(min_supp)
	print(sdc)

	print('1#######')
	sorted_items, sorted_minsup = sort(I, min_supp)
	print('sorted items :', sorted_items)
	print('sorted_minsup :', sorted_minsup)

	print('2######')
	L, support_count = init_pass(sorted_items, sequences, sorted_minsup) 
	print('L: ', L)
	print('Support Count :', support_count)

	print('3######')
	F = []
	k = 2
	f_1 = []
	main_count = []
	counter_len1 = []


	#CHECK THIS LINE WHY DO WE NEED IT?
	least_minsup_item = sorted_items[0]

	for element in L:
		index = sorted_items.index(element)
		print('index of item ',element, 'in sorted item list= ', index)
		if(support_count[index]/len(S) >= sorted_minsup[index]):
			f_1.append([[element]])
			counter_len1.append(support_count[index])

	# print(f_1)
	main_count.append(counter_len1)
	F = []
	F.append(f_1)
	print('one length sequences-------------', f_1)


	

	while(len(F[k-2])!= 0):
		print('length of F---------',len(F))
		print('Printing K---------------',k)
		if k == 2:
			print('L passed to level2: ', L)
			C =lvl2_candidate_gen(L, min_supp, n, sdc, support_count, sorted_items)
			print ("LVL2 candidate gen:  ", C)
		else:
			######FOR TESTING REMOVE BREAK LATER-------#
			#print("#############")
			#break
			print('K NOT EQUALS 2 but', k)
			print(F)
			C = ms_candidate_gen(F[k-2], min_supp, least_minsup_item)


		####USE THIS###
		###Removing candidats having duplicate elements in an itemset
		print('length of C',  len(C))
		print(C)

		candidate_counter = 0
		while(candidate_counter<len(C)):
			#print('removing duplicate lists')
			
			#print(candidate_counter)
			#print('checking candidate: ', C[candidate_counter])
			ind_candidate = C.index(C[candidate_counter])
			for i in range(len(C[candidate_counter])):

				if(len(C[candidate_counter][i]) != len(set(C[candidate_counter][i]))):
					print('poppoing' , C[candidate_counter])
					#print('i before pop', candidate_counter)
					C.pop(ind_candidate)
					#print('C after pop', C)
					candidate_counter = candidate_counter -1
					#print('i after pop', candidate_counter)
					break
			candidate_counter = candidate_counter +1

		
		print('Length of  after cleaning: ',len(C))

		print('After cleanu',C)
		candidate_count = [0 for i in range(len(C))] 
		for sequence in S:
			for candidate in C:
				#print('$$$$$$$$$$$$$$$$')
				if(contains(candidate, sequence)):
					candidate_count[C.index(candidate)] += 1

		#####test######
		#print()
		#####

		###test###
		for z in range(len(C)):
			print('Candidate : ', C[z])
			print('Candidate Count:',candidate_count[z])

		count_array = None
		count_array = []
		f = None
		f = []
		# count_c = []
		for candidate in C:
			if( candidate_count[C.index(candidate)]/n >= cand_min_mis_item(candidate,min_supp )):
				f.append(candidate)
				count_array.append(candidate_count[C.index(candidate)])

		#k and F
		# try:
		# 	t=F[k-2]
		# except IndexError:
		# 	print('BREAKKKK')
		# 	break
				# count_c.append(candidate_count[C.index(candidate)])
		# print(count_c)
		#print(F)
		Q = []
		print('************ Q ******',  Q)		
		print('length of F---------', len(F))
		if(k==2):
			f_dummy = copy.deepcopy(f)
			print('--------------appending length 2 when k is 2-----')
			
			Q.append(f_dummy)
			main_count.append(count_array)
			print('---_Q-------: ',Q)
		else:
			main_count.append(count_array)
		
		print('%%%%%%%%%%%%%%Length of main count', len(main_count))

		
		print('LENGTH OF F initial',len(F))
	
		
		if(k==2):
			F.append(f_dummy)
		else:	
			F.append(f)
		

		if(k==3):
			print('CHECK @:', F)
		print('LENGTH OF F after appending in k step',len(F))
		print(F[len(F)-1])
		k = k + 1
		

		C= []

		print(F[1])

		print(F)

	main_count.pop()
	print(main_count)

	F.pop()
	print('-------------------------------------Final F length-------------------------------', len(F))
	print(F)

	for l in range(1,len(F)):
		print(l)
		if(calc_len(F[l-2][0]) == calc_len(F[l-1][0])):
			F = F[:l-1]

	with open("output.txt", "w") as out_file:
		for i in range(len(F)):
			text = "The number of length " + str(i + 1) + " sequential patterns is " + str(len(F[i])) + "\n"
			out_file.write(text)
			for seq in range(len(F[i])):
				inner_text = "Pattern : " + pack_sequence(F[i][seq]) + " : Count=" + str(main_count[i][seq]) + "\n"
				out_file.write(inner_text)









	# I.sort()

	# print('Sequences')
	# print(sequences)
	# print('I : ', I)
	# print('min_supp :', min_supp)
	# print('sdc :', sdc)

	# sorted_items, sorted_minsup = sort(I, min_supp)

	# print('Checking Sort')
	# print('sorted Items :',sorted_items)
	# print('sorted min_supp :', sorted_minsup)

	#F = ms_gsp(sequences, I, min_supp, sdc)

	# print("Final result:         ", F[2])

if __name__ == "__main__":
	main()
