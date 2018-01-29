import os, random, base64, time

def powmod(m, e, n):  # 不知道自带的pow也能这样搞,心态大崩
	c = 1
	e = bin(e)[2:]
	k = len(e)
	for i in range(k):
		c = c ** 2 % n
		if e[i] == '1':
			c = c * m % n
	return (c)

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

def EncryptedDiv(A):
	C1 = []
	C2 = []
	r=len(A)//16
	for i in range(r):
		C1.append((A[0]<<0x38)+(A[1]<<0x30)+(A[2]<<0x28)+(A[3]<<0x20)+(A[4]<<0x18)+(A[5]<<0x10)+(A[6]<<0x8)+A[7])
		C2.append((A[8]<<0x38)+(A[9]<<0x30)+(A[10]<<0x28)+(A[11]<<0x20)+(A[12]<<0x18)+(A[13]<<0x10)+(A[14]<<0x8)+A[15])
		A = A[16:]
	return (C1,C2,r)	

def MessageDiv(A):
	if (len(A))%7!=0:
		A=A+bytes(7-(len(A))%7)
	blk = []
	for i in range(len(A) // 7):
		blk.append((A[0]<<0x30)+(A[1]<<0x28)+(A[2]<<0x20)+(A[3]<<0x18)+(A[4]<<0x10)+(A[5]<<0x8)+A[6])
		A = A[7:]
	return blk


def encrypt(message,a,y,p):
	block = MessageDiv(message)
	data = []
	for i in block:
		k=random.randrange(300,p-1)
		U=powmod(y, k, p)
		data.append(powmod(a, k, p))
		data.append((U*i%p))
	text = []
	for i in data:
		A = i
		text.append((A >> 0x38) % 0x100)
		text.append((A >> 0x30) % 0x100)
		text.append((A >> 0x28) % 0x100)
		text.append((A >> 0x20) % 0x100)
		text.append((A >> 0x18) % 0x100)
		text.append((A >> 0x10) % 0x100)
		text.append((A >> 0x8) % 0x100)
		text.append(A % 0x100)
	text = bytes(text)
	return text

def decrypt(message, d, p):
	C1,C2,r = EncryptedDiv(message)
	data = []
	for i in range(r):
		V=powmod(C1[i], d, p)
		V=modinv(V, p)
		data.append((C2[i]*V)%p)
	text = []
	for i in data:
		A = i
		text.append((A >> 0x30) % 0x100)
		text.append((A >> 0x28) % 0x100)
		text.append((A >> 0x20) % 0x100)
		text.append((A >> 0x18) % 0x100)
		text.append((A >> 0x10) % 0x100)
		text.append((A >> 0x8) % 0x100)
		text.append(A % 0x100)
	text = bytes(text)
	return text

os.system("title  Elgamal")
coding=['utf-8','GBK','unicode_internal']
Inv = input('请选择:1.加密 2.解密: ')


#start = time.clock()

p = eval(input('\n请输入公钥p(模数): '))


if Inv == '2':
	#t1 = time.clock()
	d = eval(input('请输入私钥d(私钥): '))
	Message = bytes(input('\n请输入base64格式的密文: '), encoding='ascii')
	start = time.clock()
	Message = base64.b64decode(Message)
	text = decrypt(Message, d, p)
else:
	a = eval(input('请输入公钥a(原根): '))
	y = eval(input('请输入公钥y(α^d): '))
	choose=int(input('\n请选择明文编码:1.utf-8 2.GBK 3.unicode: '))-1
	EnCo=coding[choose]
	Message = bytes(input('请输入明文: '), encoding=EnCo)
	start = time.clock()
	text = encrypt(Message,a,y,p)

ans = ['UTF-8','GBK','Unicode']

if Inv == '1':
	text = base64.b64encode(text)
	text = str(text, encoding="ascii")
	print('\n密文(以base64形式输出):\n', text)
else:
	print(text)
	print(len(text))
	flag=0
	print('\n明文:\n')
	for i in range(3):
		try:
			plaintext = " "+ans[i]+': '+str(text, encoding=coding[i])
			print(plaintext)
			flag+=1
		except:
			#print("*"+ans[i]+"解码失败!")
			pass
	if flag==0:
		print("\n解密失败!\n请核对密文/密钥的完整性或使用其他编码字符集\n")
	elif flag==1:
		print("")
	else:
		print("-----------------------------\n*请根据语义判断明文内容\n")
		
end = time.clock()
print("\n运算耗时 %f秒" % (end  - start))

os.system("PAUSE")