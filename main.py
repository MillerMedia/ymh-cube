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
first_frame_affirmations = open_binary_file('first_frame_affirmations.txt')
first_frame_daily_inspirations = open_binary_file('first_frame_daily_inspirations.txt')
first_frame_sermons = open_binary_file('first_frame_sermons.txt')

# Loop through the input directory and output converted files to the output directory
input_directory = 'input/'
output_directory = 'output/'

for content in os.listdir(input_directory):
	# If the subdirectory is not in the directories array, continue
	if content not in directories_to_add_in_order: continue

	if content=='Affirmations':
		first_frame = first_frame_affirmations
	elif content=='Daily Inspirations':
		first_frame = first_frame_daily_inspirations
	elif content=='Sermon':
		first_frame = first_frame_sermons

	# If it is a directory, continue to drill down more
	if os.path.isdir(input_directory + content):
		for file in os.listdir(input_directory + content):
			# Skip hidden files
			if file.startswith('.'): continue

			file_path = input_directory + content + '/' + file

			tmp_path = output_directory + content + '/tmp/' + file
			tmp_output, tmp_extension = os.path.splitext(tmp_path)
			tmp_path = tmp_output + '.mp3'

			output_path = output_directory + content + '/' + file
			filename_output, file_extension = os.path.splitext(output_path)
			output_path = filename_output + '.mp3'

			if not os.path.isdir(output_directory + content + '/tmp'):
				os.mkdir(output_directory + content + '/tmp')

			subprocess_array = [
				'ffmpeg',
				'-y',
				'-i',
				file_path,
				'-ar',
				'48000',
				'-acodec',
				'libmp3lame',
			]

			subprocess_array.append(tmp_path)
			subprocess.call(subprocess_array)

			audio_bytes = open_binary_file(tmp_path)
			output = first_frame + audio_bytes
			write_binary_file(output_path, output)

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
