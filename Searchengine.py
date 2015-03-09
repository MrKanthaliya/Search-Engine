# Search-Engine
#Its a simple Search Engine written in Python which crawls webpages and store words or combination of words. Page rank algorithm is used for showing best website. Luckysearch function is made to find best possible search among all websites.
#By Pritesh Kanthaliya

#!/usr/bin/python
import urllib2

def webLink(weblink):
	try:
		req=urllib2.Request(weblink)
		response = urllib2.urlopen(req)
		html= response.read()
		return html 
	except:
		return "" 

#remove tags from whole webpage content
def removeTags(string):
	start = string.find('<')
	while start != -1:
		end = string.find('>',start)
		string = string[:start] + " " + string[end + 1:]
		start = string.find('<')
	return string

#get link from tag
def getNextTarget(page):

	startLink = page.find('<a href=')
	if startLink==-1:
		return None,0
	startQuote = page.find('"',startLink)
	endQuote = page.find('"',startQuote+1)
	url=page[startQuote+1:endQuote]
	return url,endQuote

#get all links from webpage
def getAllLinks(page):
	links=[]
	while True:
		url,endPostion = getNextTarget(page)
		if url:
			links.append(url)
			page=page[endPostion:]
		else:
			break
	return links

#crwaling web to find important keywords
def crawlWeb(seed):
	toCrawl=set(seed)
	crawled=set()
	index={}
	graph = {}  #<url>,[list of pages it links to]
	while toCrawl:
		page=toCrawl.pop()
		
		if page not in crawled:
			content = webLink(page)
			outlinks = getAllLinks(content)
			content = removeTags(content)
			contentList = splitString(content,specialList)
			addPageToIndex(index,page,contentList)
			graph[page]=outlinks
			toCrawl.update(outlinks)
			crawled.add(page)
		
	return index , graph 

#adding key words to index
def addToIndex(index,keyword,url):
	if keyword in index:
		if url not in index[keyword]:
			index[keyword].append(url)
	else:
		index[keyword] = [url]

#adding to index 
def addPageToIndex(index,url,content):
	
	for words in content:
		addToIndex(index,words,url)

#computing webpage ranking
def computeRanks(graph,k):
	d = 0.8 #damping factor
	numLoops = 10

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages

	for i in range(0, numLoops):
		newranks = {}
		for page in graph:
			newrank = (1 - d)/npages
			for node in graph:
				if page in graph[node]:
					if not reciprocalLink(graph, node, page, k):
						newrank = newrank + d * (ranks[node] / len(graph[node]))
			newranks[page] = newrank
		ranks = newranks
	return ranks

def reciprocalLink(graph,source,destination,k):
	if k ==0:
		if destination == source:
			return True
		return False
	if source in graph[destination]:
		return True
	for node in graph[destination]:
		if reciprocalLink(graph,source,node, k-1):
			return True
		return False

#function to split String into words without special characters
def splitString(source,splitlist):
	output = []
	atsplit = True  # At a split point
	for char in source: #iterate through string by each letter
		if char in splitlist:
			atsplit = True
		else:
			if atsplit:
				output.append(char)
				atsplit = False
			else:
				#add character to last word
				output[-1] = output[-1] + char
	
	return output

#looking for keyword in index and returning list of urls
def lookup(index,keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

#searching for all words combined
def luckySearch(index,ranks,keyword):
	try:
		luckySearch = lookup(index,keyword)  #if sentence is present in index return
		if(luckySearch):
			return luckySearch
		words=keyword.split(" ")        #spliting each word
		urlList=lookup(index,words[0])
		newKeyword = ""
		for word in range(len(words)):
			new = lookup(index,words[word])
			if new == None:
				pass
			else:
				newKeyword = newKeyword + " "+ words[word]
				urlList = list(set(new) & set(urlList))
		searched=[]
		send=[]
		for url in urlList:
			try:
				if ranks[url]: searched.append([ranks[url],url])
			except:
				pass
		searched.sort()
		for i in range(len(searched)): send.append(searched[i][1])
		if newKeyword not in index:
			index[newKeyword.strip()] = send
		return send
	except:
		return None
		
source=webLink('www.url.com') # url from where to start crawling.

links = getAllLinks(source) # function to get all links in page
links.append('www.url.com')

#List of special Characters
specialList = [',','=',' ','>','<','	','/','\n','\r','!']  

index,graph=crawlWeb(links) 
ranks = computeRanks(graph,10)

print luckySearch(index,ranks,"search Strin")
