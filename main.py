import os
import subprocess
from shutil import copyfile

def open_binary_file(file_path):
	f = open(file_path, 'rb')
	binary_contents = f.read()
	f.close()
	return binary_contents

def write_binary_file(output_path, contents):
	f = open(output_path, "wb")
	f.write(contents)
	f.close()

volume_name = 'YMH'
directories_to_add_in_order = ['Affirmations', 'Daily Inspirations', 'Sermon']

# Load frame we are prepending to all audio files
first_frame = open_binary_file('first-frame.txt')

# Loop through the input directory and output converted files to the output directory
input_directory = 'input/'
output_directory = 'output/'

for content in os.listdir(input_directory):
	# If the subdirectory is not in the directories array, continue
	if content not in directories_to_add_in_order: continue

	# If it is a directory, continue to drill down more
	if os.path.isdir(input_directory + content):
		for file in os.listdir(input_directory + content):
			file_path = input_directory + content + '/' + file
			audio_bytes = open_binary_file(file_path)

			output = first_frame + audio_bytes
			output_path = output_directory + content + '/' + file
			write_binary_file(output_path, output)

			# Convert it to 48000 mp3 if not already
			filename_output, file_extension = os.path.splitext(output_path)

			#if file_extension is not '.mp3':
			# Create file in tmp directory
			tmp_path = output_directory + content + '/tmp/' + file

			if not os.path.isdir(output_directory + content + '/tmp'):
				os.mkdir(output_directory + content + '/tmp')

			copyfile(output_path, tmp_path)
			subprocess.call(['ffmpeg', '-y', '-i', tmp_path, '-ar', '48000', filename_output + '.mp3'])
			os.remove(tmp_path)

		# when done with directory, remove tmp folder
		if os.path.isdir(output_directory + content + '/tmp'):
			os.rmdir(output_directory + content + '/tmp')


# Once files are converted, write them to the Volume
volume_path = '/Volumes/' + volume_name + '/'

if os.path.isdir(volume_path):
	for directory in os.listdir(volume_path):
		# Have not figured out how to find an empty directory so just ignoring all hidden directories, leaving us
		# with one left over
		if '.' not in directory:
			# We are now in the correct directory

			# Start adding files in order
			for output_dir in directories_to_add_in_order:
				write_path = volume_path + directory + '/' + output_dir
				if not os.path.exists(write_path):
					os.makedirs(write_path)

				affirmation_list = sorted(os.listdir('output/' + output_dir))
				for file in affirmation_list:
					copyfile('output/' + output_dir + '/' + file, write_path + '/' + file)
else:
	print('External volume named ' + volume_name + ' not present.')
