# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: clean special characters
"""

import re
import os

def clean(content):
	p2 = re.compile('[（\(][，；。？！\s]*[）\)]')
	p3 = re.compile('[「『]')
	p4 = re.compile('[」』]')

	content = p2.sub('', content)
	content = p3.sub('“', content)
	content = p4.sub('”', content)
	content = content.replace("\n", " ")
	content = content.replace("\t", " ")


	return content

if __name__ == '__main__':
	os.chdir("../data/")
	for file in os.listdir():
		if file[-1].isdigit():
			clean(file)