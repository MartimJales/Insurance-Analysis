import sys
import csv

def create_instances(instances, num, instance):
	line = list(instance.values())
	while (num > 0):
		instances.append(line)
		num -= 1

def create_table(instances, row, instance):
	# instance = {'sex':'','age':'','body':'','local':'','month':''}
	if row[0] == '' and row[1].isnumeric():
		instance['age'] = row[1]
		if row[2] != '':
			instance['sex'] = 'girl'
			create_instances(instances, int(row[2]), instance)
		if row[3] != '':
			instance['sex'] = 'boy'
			create_instances(instances, int(row[3]), instance)
	elif not(row[1].isnumeric()):
		instance[row[0]] = row[1]

def main(args):
	with open(args[0], 'r') as file:
		reader = csv.reader(file)
		instances = []
		instance = {'sex':'','age':'','body':'','local':'','month':''}
		for row in reader:
			create_table(instances, row, instance)
	with open(args[1], 'w') as file:
		writer =csv.writer(file)
		writer.writerows(instances)

if __name__ == '__main__':
	main(sys.argv[1:])


