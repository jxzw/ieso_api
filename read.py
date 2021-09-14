import json
import datetime

# opens and read *WINDOWS* file system saved files and returns an array to be built with pandas
def retrieve(): 
	file = open(f"supply\\output.json",)
	numdays = 95
	base = datetime.datetime.now() - datetime.timedelta(days=1)
	date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
	formatted_list = []
	for date in date_list:
		year = str(date.year)
		month = str(date.month).zfill(2)
		day = str(date.day).zfill(2)
		datestring = year + month + day
		formatted_list.append(datestring)


	file_list = []
	fulldata = []

	for date in formatted_list:
		file_list.append(f"supply//\output_{date}.json")
		try:
			file = open(f"supply//\output_{date}.json",)
			data = json.load(file)
			file.close()
			fulldata.append(data)
		except FileNotFoundError as e:
			pass



	parsed_full = {}

	for day in fulldata:
		date = list(day.keys())[0]
		parsed_full[date] = day[date]


	generator_keys = dict((i, [],) for i in range(0,len(parsed_full[list(parsed_full.keys())[0]])))

	for date in parsed_full.keys():

		for i, generator in enumerate(parsed_full[date].keys()):
			name = parsed_full[date][generator]['name']

			fueltype = parsed_full[date][generator]['fueltype']
			outputs = parsed_full[date][generator]['outputs']
			out_list = list(outputs.values())
			entry = [date, name, fueltype]
			for x in out_list:
				entry.append(x)
			generator_keys[i].append(entry)
			entry = []
	
	return generator_keys
