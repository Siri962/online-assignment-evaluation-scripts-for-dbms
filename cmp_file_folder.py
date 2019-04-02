from fnmatch import fnmatch
from prettytable import PrettyTable
import lzma
import py7zlib
import tarfile
import rarfile
import sys
import os
import zipfile
import difflib
import re
import time
start=time.time()
def accuracy(s_data,c_data):
	s_data=s_data.replace("&amp;","&")
	c_data=c_data.replace("&amp;","&")
	s_data = re.sub(r"<!--(.|\s|\n)*?-->", "", s_data)
	c_data = re.sub(r"<!--(.|\s|\n)*?-->", "", c_data)
	s_data = re.sub(r"<meta(.|\s|\n)*?>", "", s_data)
	c_data = re.sub(r"<meta(.|\s|\n)*?>", "", c_data)
	a=s_data.replace(" ","").replace("\n","").replace("\t","")
	b=c_data.replace(" ","").replace("\n","").replace("\t","")
	seq=difflib.SequenceMatcher(None,a,b)
	d=seq.ratio()*100
	acc=round(d,1)
	return(acc)

s="6.zip"
#fol=raw_input("folder path: ")
#c_out=raw_input("Enter file to show matched files outputs: ")
#w_out=raw_input("Enter file to show mis-matched files outputs: ")
fol=sys.argv[1]
c_out=sys.argv[2]
w_out=sys.argv[3]	
w_out_file=open(w_out,'a')
c_out_file=open(c_out,'a')
li=[]
pattern="*.*"
files=os.listdir(fol)
for i in files:
	if fnmatch(i,pattern):
		li.append(os.path.join(fol,i))
li.sort() 
a=s
x=[]
m=[]
z1=zipfile.ZipFile(a,'r')
src_files=z1.namelist()
src_files.sort()
for filename in src_files:	
	if not os.path.isdir(filename):
		if filename.endswith('.html'):
			with z1.open(filename) as f1:
				src_data=f1.read()
				src_data=str(src_data)
				x.append(src_data)
				m.append(filename)

for c in li:
	try:
		b=c
		y=[]
		n=[]
		if tarfile.is_tarfile(b):
			z2 = tarfile.open(b,'r')
			cmp_files=list(z2.getnames())
			cmp_files.sort()
			for file_name in cmp_files:
				if not os.path.isdir(file_name):
					if file_name.endswith('.html'):
						f2=z2.extractfile(file_name)
						cmp_data=f2.read()
						cmp_data=str(cmp_data)
						y.append(cmp_data)
						n.append(file_name)
		elif zipfile.is_zipfile(b):
			z2=zipfile.ZipFile(b,'r')
			cmp_files=list(z2.namelist())
			cmp_files.sort()
			for file_name in cmp_files:
				if not os.path.isdir(file_name):
					if file_name.endswith('.html'):
						f2=z2.open(file_name,'r')
						cmp_data=f2.read()
						cmp_data=str(cmp_data)
						y.append(cmp_data)
						n.append(file_name)

		elif rarfile.is_rarfile(b):
			z2=rarfile.RarFile(b,'r')
			cmp_files=list(z2.namelist())
			cmp_files.sort()
			for file_name in cmp_files:
				if not os.path.isdir(file_name):
					if file_name.endswith('.html'):
						f2=z2.open(file_name,'r')
						cmp_data=f2.read()
						cmp_data=str(cmp_data)
						y.append(cmp_data)
						n.append(file_name)

		elif b.endswith(".7z"):
			z2=py7zlib.Archive7z(open(b,'rb')) 
			cmp_files=list(z2.getnames())
			cmp_files.sort()
			for file_name in cmp_files:
				if not os.path.isdir(file_name):
					if file_name.endswith('.html'):
						f2=z2.getmember(file_name)
						cmp_data=f2.read()
						cmp_data=str(cmp_data)
						y.append(cmp_data)
						n.append(file_name)

		elif b.endswith(".xz"):
			fa=lzma.LZMAFile("8.tar.xz")
			z2=tarfile.open(fileobj=fa)
			cmp_files=list(z2.getnames())
			cmp_files.sort()
			for file_name in cmp_files:
				if not os.path.isdir(file_name):
					if file_name.endswith('.html'):
						f2=z2.extractfile(file_name)
						cmp_data=f2.read()
						cmp_data=str(cmp_data)
						y.append(cmp_data)
						n.append(file_name)


		else:
			w_out_file.write("\n\nfile extension not matched in ... {} file".format(c))
			continue
		
		if(len(x)!=len(y)):
			w_out_file.write("\n\nNumber of html files not matched in ... {} file".format(c))
			w_out_file.write("\nNumber of files in {} : {}".format(s,len(x)))
			w_out_file.write("\nNumber of files in {} : {}".format(c,len(y)))		
		else:
			k=[]
			for i in range(len(x)):
				k.append(accuracy(x[i],y[i]))
			t = PrettyTable(['Source file', 'Compared file','Accuracy'])
			for j in range(len(k)):
				t.add_row([m[j],n[j],k[j]])
			table_txt = t.get_string()
			c_out_file.write("\n\n\nAccuracy of each file......in {}\n".format(c))	
			c_out_file.write(table_txt)
	except:
		w_out_file.write("\n\nexception in ... {} file".format(c))
		continue
c_out_file.close()
w_out_file.close()
print("finished....")
end=time.time()
print(end-start)
