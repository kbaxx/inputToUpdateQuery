#!/usr/bin/python
import sys

if len(sys.argv) < 2:
	print "Missing Argument: A filename parameter is needed."
	sys.exit()

filename = sys.argv[1]	
file = open(filename, "r")

counter = 0
queries = []
query = ""
for l in file:
	line = l.strip()
	query += line + " "
	if line.endswith(";"):
		if query.startswith(" "):
			query = query[1:len(query)]
		queries.append(query)
		query = ""

queryMaps = []
names = []
values = []
table = ""
for query in queries:
	table = query.split("INSERT INTO ")[1].split(" (")[0]
	names = query.split("(",1)[1].split(")",1)[0].split(", ")

	temp = query.split("VALUES")[1]	
	inputlines = temp.split("(")
	inputlines = inputlines[1:len(inputlines)]
	amount = len(inputlines)
	if amount > 1:
		for inputline in inputlines:
			values = inputline.split(")",1)[0].split(", ")
			queryMaps.append({"table":table, "names":names, "values":values})
	else:
		values = query.split("VALUES")[1].split("(",1)[1].split(")",1)[0].split(", ")
		queryMaps.append({"table":table, "names":names, "values":values})


filename = filename[0:len(filename)-4]+"_update.sql"
outputFile = open(filename, "w")

for item in queryMaps:
	table = item["table"]
	names = item["names"]
	values = item["values"]

	finalQuery = "UPDATE " + table + " SET\n"
	for i in range(1, len(names)):
		finalQuery += names[i]+"="+values[i]+", "

	finalQuery = finalQuery[0:len(finalQuery)-2]+" "
	finalQuery += "\nWHERE "+names[0]+"="+values[0]+";\n\n"

	outputFile.write(finalQuery)
	# print finalQuery

print "Successfully converted the query!"
