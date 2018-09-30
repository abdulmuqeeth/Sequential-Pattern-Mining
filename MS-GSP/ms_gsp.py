#!/usr/bin/env python

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
	n = 0
	ms_gsp(s, min_supp, n)

if __name__ == "__main__":
	main()
