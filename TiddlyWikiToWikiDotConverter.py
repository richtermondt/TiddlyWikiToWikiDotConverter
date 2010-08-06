import sys
#class TiddlySpotUtils

WIKI_PAGE_LOCATION = "../coder.html"
BEGIN_TIDDLY_DATA = "<!--POST-SHADOWAREA-->"
END_TIDDLY_DATA = "<!--POST-STOREAREA-->"
DEFAULT_OUTFILE = "tiddlyWikiExtract.txt"

def main(args) :
	if len(args) > 0 :
		entry = args[0]
		if entry == 'list' :
			listAllEntries()
		else :
			getEntryByName(entry)
			convertTiddlyToDot(entry + '.txt')
	else :	
		extractTiddlySpotEntries()
		convertTiddlyToDot() 
	

def listAllEntries() :
	# open input file
	infile = file(WIKI_PAGE_LOCATION, "r")
	
	start = False
	count = 0
	
	# loop through each line
	for line in infile:
		
		i = line.find(BEGIN_TIDDLY_DATA)
		
		if i != -1 :
			start = True
			
		if start == True:
			k = line.find(END_TIDDLY_DATA)
			if k != -1:
				start = False
				break

			
			else :

				j = line.find('<div title=')
				if j != -1 :
					count = count + 1
					print line
					

			
	infile.close()
	print 'Total entries: ' 
	print count

def convertTiddlyToDot(extractFilename=DEFAULT_OUTFILE) :
	s = ""
	infile = file(extractFilename, "r")
	
	handleCode = False
	
	for line in infile :
	
		if handleCode == False :
			
			if line.find('{{{') > -1 :
				
				handleCode = True
		
		if handleCode == True :
			
			t = line.replace('{{{','[[code]]')
			
			if t.find('}}}') > -1 :
				
				s = s + t.replace('}}}','[[/code]]')
				handleCode = False
				
			else :

				s = s + t
				
		else :
			
			s = s + convertTiddlyTablesAndHeadlinesToDot(line)
		
	infile.close()
		
	outfile = file("wikiDotTransitional.txt", "w")
	outfile.write(s)
	outfile.close()
	

def getEntryByName(name) :
	
	# open input file
	infile = file(WIKI_PAGE_LOCATION, "r")
	
	s = ""
	
	start = False
	foundEntry = False
	
	# loop through each line
	for line in infile:
		
		i = line.find(BEGIN_TIDDLY_DATA)
		
		if i != -1 :
			start = True
			
		if start == True:
			k = line.find(END_TIDDLY_DATA)
			if k != -1:
				start = False
				break

			if foundEntry == True :
				m = line.find('</div>')
				if m != -1 :
					entryFound = False
					break

				s = s + line
			else :

				j = line.find('<div ')
				if j != -1 :
					h = line.find(name)
					if h != -1 :
						foundEntry = True
					

			
	infile.close()
	
	outfile =file(name + ".txt", "w")
	outfile.write(s)
	outfile.close()	
	
	

def convertTiddlyTablesAndHeadlinesToDot(line) :
	s = line

	if s[0] == '|' :
		s = s.replace('|','||')
		s = s.replace('||!','||~')
	
	s = convertTiddlyHeadlineToDot(s, 0)
	
	return s


def convertTiddlyHeadlineToDot(line, index) :
	s = line
	if s[index] == '!' :
		s = s.replace('!','+', 1)
		
		s = convertTiddlyHeadlineToDot(s, index + 1)
		
	return s
	

def extractTiddlySpotEntries() :
	
	# open input file
	infile = file(WIKI_PAGE_LOCATION, "r")
	
	s = ""
	
	
	start = False
	
	
	# loop through each line
	for line in infile:
		
		i = line.find(BEGIN_TIDDLY_DATA)
		
		if i != -1 :
			start = True
			
		
		if start == True:
			
			j = line.find(END_TIDDLY_DATA)
			
			if j != -1:
				start = False
				break
					
			s = s + line
	
	infile.close()
	
	outfile =file(DEFAULT_OUTFILE, "w")
	outfile.write(s)
	outfile.close()


if __name__ == '__main__':

	args = sys.argv[1:]
	main(args)
