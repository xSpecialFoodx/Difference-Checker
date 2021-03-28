import string
import sys, os
import argparse
import distutils.dir_util

#
# #
# # #
# # # # difference checker
# # #
# #
#

class MyParser(argparse.ArgumentParser):
	def error(self, message):
		self.print_help()
		sys.stderr.write('\nerror: {0}\n'.format(message))
		sys.exit(2)


def CheckHexText(source, length, add_0x):  # returns the hex text
    source_hex = str(hex(source)[2:])
    source_hex_length = len(source_hex)
    source_hex_index = None
    source_hex_cell = None

    for source_hex_index in range(0, source_hex_length):
        source_hex_cell = source_hex[source_hex_index]

        if (source_hex_cell in string.hexdigits) is False:
            source_hex = source_hex[:source_hex_index]

            break

    result = str(source_hex.zfill(length))

    if add_0x is True:
        result = "0x" + result

    return result

def add_difference(location, offset, first_file_byte, second_file_byte):
	result = None

	first_file_byte_fixed = CheckHexText(first_file_byte, 2, False) if first_file_byte is not None else ""

	second_file_byte_fixed = CheckHexText(second_file_byte, 2, False) if second_file_byte is not None else ""

	result = [location, 1, first_file_byte_fixed, second_file_byte_fixed]

	return result

def combine_differences(differences):
	result = None

	current_result = None

	differences_amount = len(differences)

	if differences_amount > 0:
		differences_index = None
		difference = None

		current_result = []
		current_result_amount = 0
		current_result_cell = None
		
		difference = differences[0]

		current_result_cell = difference
		current_result.append(current_result_cell)
		current_result_amount += 1

		for differences_index in range(1, differences_amount):
			difference = differences[differences_index]

			if current_result_cell[0] + current_result_cell[1] == difference[0]:
				current_result_cell[1] += difference[1]
				current_result_cell[2] = current_result_cell[2] + difference[2]
				current_result_cell[3] = current_result_cell[3] + difference[3]
			else:
				current_result_cell = difference
				current_result.append(current_result_cell)
				current_result_amount += 1

	result = current_result

	return result

Debug = False

parser = MyParser(description='files difference checker')

if Debug is False:
	parser.add_argument('--first', required=False, type=str, help='first file')
	parser.add_argument('--second', required=False, type=str, help='second file')
	parser.add_argument('--output', required=False, default="", type=str, help='new file')
	parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
	parser.add_argument('--verbose', required=False, default=False, action='store_true', help='detailed printing')

	if len(sys.argv) == 1:
		parser.print_usage()
		sys.exit(1)
else:
	parser.add_argument('--first', required=False, default="C:/somefolder/somefileA.bin", type=str, help='first file')
	parser.add_argument('--second', required=False, default="C:/somefolder/somefileB.bin", type=str, help='second file')
	parser.add_argument('--output', required=False, default="", type=str, help='new file')
	parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
	parser.add_argument('--verbose', required=False, default=False, action='store_true', help='detailed printing')

args = parser.parse_args()

def main():
	global parser

	global args

	first_file_path = os.path.abspath(args.first).replace('\\','/')

	if not os.path.isfile(first_file_path):
		parser.error('invalid first file: {0}'.format(first_file_path))

	first_file_size = os.path.getsize(first_file_path)

	second_file_path = os.path.abspath(args.second).replace('\\','/')

	if not os.path.isfile(second_file_path):
		parser.error('invalid second file: {0}'.format(second_file_path))

	second_file_size = os.path.getsize(second_file_path)

	if args.output == "":
		first_file_name = os.path.basename(first_file_path)
		first_file_name_length = len(first_file_name)
		first_file_name_splitted = first_file_name.split(".")
		first_file_name_splitted_amount = len(first_file_name_splitted)
		first_file_name_extension = first_file_name_splitted[first_file_name_splitted_amount - 1]
		first_file_name_extension_length = len(first_file_name_extension)
		first_file_name_without_extension = first_file_name[:first_file_name_length - first_file_name_extension_length - 1]

		second_file_name = os.path.basename(second_file_path)
		second_file_name_length = len(second_file_name)
		second_file_name_splitted = second_file_name.split(".")
		second_file_name_splitted_amount = len(second_file_name_splitted)
		second_file_name_extension = second_file_name_splitted[second_file_name_splitted_amount - 1]
		second_file_name_extension_length = len(second_file_name_extension)
		second_file_name_without_extension = second_file_name[:second_file_name_length - second_file_name_extension_length - 1]

		output_file_name_extension = "txt"
		output_file_name_without_extension = first_file_name_without_extension + '-' + second_file_name_without_extension + '-' + "comparison_result"

		output_file_name = output_file_name_without_extension + '.' + output_file_name_extension

		output_file_path = os.path.abspath(output_file_name).replace('\\','/')
	else:
		output_file_path = os.path.abspath(args.output).replace('\\','/')

	output_folder_path = os.path.dirname(output_file_path).replace('\\','/')

	if output_folder_path[len(output_folder_path) - 1] == '/':
		output_folder_path = output_folder_path[:-1]
	
	if args.dry_run is False:
		distutils.dir_util.mkpath(output_folder_path)
	
	if os.path.exists(output_file_path) and not os.path.isfile(output_file_path):
		parser.error('invalid output file: {0}'.format(output_file_path))
	
	print(
		"First File:" + ' ' + first_file_path + "\n"
		+ "Second File:" + ' ' + second_file_path + "\n"
		+ "Output:" + ' ' + output_file_path + "\n"
		+ "Dry Run:" + ' ' + ("True" if args.dry_run is True else "False") + "\n"
		+ "Verbose:" + ' ' + ("True" if args.verbose is True else "False")
	)

	print("")
	print('processing comparison result file: {0}'.format(output_file_path))

	Headers = None
	Fields = None
	Field = None

	AddressesLength = 8#16
	SizeLength = 8#16

	first_file_data = None
	first_file_data_size = None
	first_file_data_cell = None

	second_file_data = None
	second_file_data_size = None
	second_file_data_cell = None

	output_file_data_list = None
	output_file_data_list_amount = 0
	output_file_data_list_cell = None
	output_file_data = None

	differences = []
	differences_amount = 0
	difference = None

	differences_sequences = None
	differences_sequences_amount = None

	buffer_size = 512
	buffer_index = None

	location = 0

	smaller_file_size = first_file_size if first_file_size < second_file_size else second_file_size
	bigger_file_size = first_file_size if first_file_size > second_file_size else second_file_size
	
	with open(first_file_path, 'rb') as ff:
		with open(second_file_path, 'rb') as sf:
			while location < smaller_file_size:
				if location >= first_file_size:
					first_file_data = None
					first_file_data_size = 0
				elif location + buffer_size > first_file_size:
					first_file_data = ff.read(first_file_size - location)
					first_file_data_size = first_file_size - location
				else:
					first_file_data = ff.read(buffer_size)
					first_file_data_size = buffer_size
				
				if location >= second_file_size:
					second_file_data = None
					second_file_data_size = 0
				elif location + buffer_size > second_file_size:
					second_file_data = sf.read(second_file_size - location)
					second_file_data_size = second_file_size - location
				else:
					second_file_data = sf.read(buffer_size)
					second_file_data_size = buffer_size

				buffer_index = 0

				while buffer_index < buffer_size:
					if buffer_index < first_file_data_size:
						first_file_data_cell = first_file_data[buffer_index]
					else:
						first_file_data_cell = None

					if buffer_index < second_file_data_size:
						second_file_data_cell = second_file_data[buffer_index]
					else:
						second_file_data_cell = None

					if first_file_data_cell != second_file_data_cell:
						difference = (
							add_difference(
								location
								, buffer_index
								, first_file_data_cell
								, second_file_data_cell
							)
						)

						differences.append(difference)
						differences_amount += 1

					location += 1

					buffer_index += 1

			if smaller_file_size < bigger_file_size:
				bigger_file_size = None
				bigger_file_f = None
				bigger_file_data = None
				bigger_file_data_size = None
				bigger_file_data_cell = None

				if first_file_size > second_file_size:
					bigger_file_size = first_file_size
					bigger_file_f = ff
				else:
					bigger_file_size = second_file_size
					bigger_file_f = sf

				while location < bigger_file_size:
					if location + buffer_size > bigger_file_size:
						bigger_file_data = bigger_file_f.read(bigger_file_size - location)
						bigger_file_data_size = bigger_file_size - location
					else:
						bigger_file_data = bigger_file_f.read(buffer_size)
						bigger_file_data_size = buffer_size

					buffer_index = 0

					while buffer_index < buffer_size and buffer_index < bigger_file_data_size:
						bigger_file_data_cell = bigger_file_data[buffer_index]

						difference = (
							add_difference(
								location
								, buffer_index
								, (bigger_file_data_cell if first_file_size > second_file_size else None)
								, (bigger_file_data_cell if second_file_size > first_file_size else None)
							)
						)

						differences.append(difference)
						differences_amount += 1

						location += 1

						buffer_index += 1

	if differences_amount > 0:
		differences_sequences = combine_differences(differences)
		differences_sequences_amount = len(differences_sequences)

		print("")
		print(
			"Found" + ' ' + str(differences_amount) + ' ' + "differences"
			+ ',' + ' ' + 'and' + ' ' + str(differences_sequences_amount) + ' ' + "differences sequences"
		)

		output_file_data_list = []

		Headers = []
								
		Headers.append("First File Path")
		Headers.append("Second File Path")
		Headers.append("Output File Path")

		Fields = []

		Fields.append(Headers[0] + ':' + ' ' + first_file_path)
		Fields.append(Headers[1] + ':' + ' ' + second_file_path)
		Fields.append(Headers[2] + ':' + ' ' + output_file_path)

		for Field in Fields:
			output_file_data_list.append(Field)

		output_file_data_list.append("")

		Headers = []
								
		Headers.append("Found differences")
		Headers.append("Found differences sequences")

		Fields = []

		Fields.append(Headers[0] + ':' + ' ' + str(differences_amount))
		Fields.append(Headers[1] + ':' + ' ' + str(differences_sequences_amount))

		for Field in Fields:
			output_file_data_list.append(Field)

		output_file_data_list.append("")

		Headers = []
								
		Headers.append("Location")
		Headers.append("Size")
		Headers.append("First File Data")
		Headers.append("Second File Data")

		Fields = []

		Fields.append(None)
		Fields.append(None)
		Fields.append(None)
		Fields.append(None)

		for difference in differences_sequences:
			Fields[0] = Headers[0] + ':' + ' ' + CheckHexText(difference[0], AddressesLength, True)
			Fields[1] = Headers[1] + ':' + ' ' + CheckHexText(difference[1], SizeLength, True)
			Fields[2] = Headers[2] + ':' + ' ' + "0x" + difference[2]
			Fields[3] = Headers[3] + ':' + ' ' + "0x" + difference[3]

			output_file_data_list_cell = '\t'.join(Fields)
			output_file_data_list.append(output_file_data_list_cell)
			output_file_data_list_amount += 1

			if args.verbose is True:
				print(output_file_data_list_cell)
	else:
		print("")
		print("Didn't find any differences")

	if output_file_data_list_amount > 0:
		output_file_data = "\r\n".join(output_file_data_list)

		if args.dry_run is False:
			with open(output_file_path, 'w') as crf:
				crf.write(output_file_data)
	else:
		print("")
		print("Not writing to the output file, as no difference have been found")
		
	print("")
	print('finished processing:' + ' ' + output_file_path)

main()
