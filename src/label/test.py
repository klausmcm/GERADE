# import itertools
# import string
# 
# perms = itertools.permutations(string.digits*2, 8)
# 
# count = 0
# print(len(perms))

from src.label.LabelFullDataMatrix import LabelFullDataMatrix

l = LabelFullDataMatrix("a\nb\nc", 2, 1, 1)
