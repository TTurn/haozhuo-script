import re

a = "hello_world"

p1 = re.compile("h")
p2 = re.compile("a")

if re.search(p1, a):
	print(1)
if not re.search(p2, a):
	print(2)