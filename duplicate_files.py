import os
import shutil

def build_prefix(number):
	len_number = len(str(number))
	return 'I0' + str(number) if len_number == 2 else 'I' + str(number)

def traverse_files(files, file_directory, iteration):
	for file in sorted(files):
		if file.startswith('.'):
			continue

		# Parse prefix
		file_number = file[:4].lstrip('I').lstrip('0')
		file_name = file.split(file[:4])[1]

		new_number = (int(num_files) * iteration) + int(file_number)
		new_file_name = build_prefix(new_number) + file_name
		from shutil import copyfile
		copyfile(file_directory + file, file_directory + new_file_name)
		print(new_file_name)
		print(file)

		if new_number>=366:
			new_number = False
			break

	return new_number

# traverse root directory, and list directories as dirs and files as files
num_files = 30
iteration = 1
file_directory = './output/Daily Inspirations/'
for root, dirs, files in os.walk(file_directory):
	path = root.split(os.sep)
	new_number = True
	while new_number:
		new_number = traverse_files(files,file_directory,iteration)
		iteration+=1




