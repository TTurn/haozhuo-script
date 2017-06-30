# coding: utf-8

import re
from simhash import Simhash, SimhashIndex

def get_featuers(s):
	width = 3
	s = s.lower()
	s = re.sub(r'[^\w]', '', s)
	return [s[i:i+width] for i in range(max(len(s)-width+1, 1))]

a = Simhash(get_featuers('How are you? I am fine. Thanks.'))
b = Simhash(get_featuers('How are u? I am fine.     Thanks.'))
c = Simhash(get_featuers('How r you?I      am fine. Thanks.'))

print(a.value)
print(b.value)

print(a.distance(b))

# objs = [('1', a), ('2', b), ('3', c)]
# index = SimhashIndex(objs, k=3)
#
# print(index.bucket_size())
#
# d = Simhash(get_featuers('How are you i am fine. blar blar blar blar thank'))
# print(index.get_near_dups(d))
#
# index.add('4', d)
# print(index.get_near_dups())


