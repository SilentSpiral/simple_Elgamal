#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, random, base64, time

def powmod(m, e, n):  
	c = 1
	e = bin(e)[2:]
	k = len(e)
	for i in range(k):
		c = c ** 2 % n
		if e[i] == '1':
			c = c * m % n
	return (c)

def miller(n, a, m, t):
	b = powmod(a, m, n)
	if b == 1 or b == (n - 1):
		return True
	for i in range(t - 1):
		b = powmod(b, 2, n)
		if b == (n - 1):
			return True
	return False


def MR(p, k):
	pAss = False
	block = []
	for i in range(k):
		block.append(random.randint(2, p - 2))
	m = p - 1
	t = 0
	while not m % 2:
		m = m // 2
		t += 1
	for a in block:
		pAss = miller(p, a, m, t)
		if not pAss:
			return False
	return True

def prime(A,B):
	while True:
		p = random.randrange(A,B,2)#A必须为奇数
		if MR(p, 9):
			break
	return p

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)  # g为公因子
		return (g, x - (b // a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if (g != 1):
		print('modular inverse does not exist')
	else:
		return x % m
		
		
def keyGeneration():
	flag=0
	while not flag:
		while True:
			n=prime(0x40000000001,0x7ffffffffff) #44bit
			q=prime(0x80001,0xfffff) #19bit	
			p=2*n*q+1
			if MR(p, 9):
				break		
	
		for i in range(2,60):
			#if (powmod(i,2*n,p)!=1)and(powmod(i,2*q,p)!=1)and(powmod(i,n*q,p)!=1):
			if 1 not in (powmod(i,2*n,p),powmod(i,2*q,p),powmod(i,n*q,p)):
				flag=1
				break
		if flag:
			break
	temp=prime(n,p)
	a=powmod(i,temp,p)
	d=random.randrange(300,p-1)
	y=powmod(a,d,p)
	#print("公钥: p:"+hex(p)+" a:"+hex(a)+" y:"+hex(y)," 私钥:"+hex(d))
	print("     %-18s  %-18s  %-18s      %-18s"% (hex(p),hex(a),hex(y),hex(d)))
	return 0
	
os.system("title  密钥生成")	
	
print("公钥 %-18s  %-18s  %-18s 私钥:%-18s"% ('p:','a:','y:','d:'))
start = time.clock()
for i in range(100):
	keyGeneration()
end = time.clock()	
print ("\n\n程序共生成100组密钥,耗时 %f秒" % (end - start))	
	
os.system("PAUSE")