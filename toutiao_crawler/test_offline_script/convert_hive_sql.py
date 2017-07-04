# coding: utf-8

file_path = "/Users/mountain/Desktop/haozhuo/标签规则0628(未开发)/100个标签开发.txt"

with open(file_path, 'r') as f:
	print(f.read().split("\n\n#"))