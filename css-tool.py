from sys import argv
import re
import string
import StringIO

script, action, file_name = argv

def main(action, file_name):
  if not action or not file_name:
		print "Arguments error!"
		return
	
	if action != "-c" and action != '-f':
		return
	
	file = open(file_name)
	data = file.read()
	file.close()
	
	if not data:
		print "Data error!"
		return
	
	nameList = string.split(file_name, ".")
	file_name = ''
	i = 0 
	while i <= len(nameList)-2:
		if i == len(nameList)-2:
			file_name += str(nameList[i])
		else:
			file_name += str(nameList[i]) + "."
		i += 1
		
	if action == "-f":
		format(data, file_name)
	elif action == "-c":
		compress(data, file_name)

def delete_blank(data):
	data = string.strip(data);
	data = re.sub('\s*{\s*', '{', data)
	data = re.sub('\s*}\s*', '}', data)
	data = re.sub('\s*;\s*', ';', data)
	data = re.sub('\s*,\s*', ',', data)
	return data
		
def format(data, file_name):

	data = delete_blank(data)
	
	strlen = len(data)
	i = 0
	begin = 0
	strBuffer = StringIO.StringIO()
	
	while i < strlen:
		if data[i] == "{":
			strBuffer.write(data[begin:i] + ' {\r')
			i = i + 1
			begin = i
		
		elif data[i] == ";":
			line = string.strip(data[begin:i])
			if line.find('@') == 0:
				strBuffer.write(line + ';\r')
			else:
				strBuffer.write(" "*4 + line + ';\r')
			i = i + 1
			begin = i
		
		elif data[i] == "}":
			last = string.strip(data[begin:i])
			if last:
				strBuffer.write(" "*4 + last + ';\r')
			strBuffer.write(' }\r')
			i = i + 1
			begin = i
		elif data[i] == ",":
			last = string.strip(data[begin:i])
			strBuffer.write(data[begin:i] + ' ')
			i = i + 1
			begin = i
		else:
			i = i + 1
	
	strBuffer.write(data[begin:i+1])
			
	new_file = open(file_name + "_format.css", 'w')
	new_file.truncate()
	new_file.write(strBuffer.getvalue())
	new_file.close()
	print "Format css file complete!"
	
	
def compress(data, file_name):

	data = re.sub('\/\*[\s\S]*?\*\/', '', data)
	data = delete_blank(data)
	data = string.replace(data, ';}', '}')
	
	new_file = open(file_name + "_compress.css", 'w')
	new_file.truncate()
	new_file.write(data)
	new_file.close()
	print "Compress css file complete!"

if __name__ == "__main__":
	main(action, file_name)
	
