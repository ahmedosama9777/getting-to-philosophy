import sys
import time
import urllib

import bs4
import requests, re




def find_first_link(url):
    response = requests.get(url) # sending a GET request to the random URL, recieve a response object
    html = response.text # returns the content of the response, in unicode
    
    soup = bs4.BeautifulSoup(html, "html.parser") 

    content = soup.find(id='mw-content-text')
    for t in content.find_all(class_=['navbox', 'vertical-navbox', 'toc']):
      t.replace_with("")

    paragraph = soup.select('p')[0] # Only DIRECT child
    for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']): # remove spans and smalls with language, pronounciation
      s.replace_with("")
    paragraphText = str(paragraph)
    paragraphText = re.sub(r' \(.*?\)', '', paragraphText) # Remove leftover parenthesized text
 

    reParagraph = bs4.BeautifulSoup(paragraphText,"html.parser") # back into bs4 object to find links
    firstLink = reParagraph.find(href = re.compile('^/wiki/')) # links that start with /wiki/ only

    while firstLink == None:
      # case of disambiguation: use first wiki link in list
      if '(disambiguation)' in url or '(surname)' in url:
        firstLink = content.ul.find(href = re.compile('^/wiki/'))

      else:  
        paragraph = paragraph.find_next_sibling("p")
        
        if(paragraph is None): # Catch-case

          if(content.ul is not None):
            firstLink = content.ul.find(href = re.compile('^/wiki/')) # Disambiguation-type page
          if(firstLink is None): # No links available
            print("Wikipedia not reachable.")
            return None
          continue

        for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']):
          s.replace_with("")
        paragraphText = str(paragraph)
        paragraphText = re.sub(r' \(.*?\)', '', paragraphText)
        reParagraph = bs4.BeautifulSoup(paragraphText, "html.parser")
        firstLink = reParagraph.find(href = re.compile('^/wiki/'))


    first_link = 'http://en.wikipedia.org' + firstLink.get('href')

    return first_link


def continue_crawl(search_history, target_url): # detect if philosphy reached or got in a loop
    if search_history[-1] == target_url:
        print("Phenomena is true, got to the philosophy article!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print(article_chain[-1])
        print("oops, that's a loop.")
        return False
    else:
        return True


if __name__ == '__main__':
      target_url = "https://en.wikipedia.org/wiki/Philosophy"
      print("**Getting to philosohpy page!!**")
      if (len(sys.argv) == 1):
            print("Starting with a random link.")
            start_url = "https://en.wikipedia.org/wiki/Special:Random"
      else:
            start_url = str(sys.argv[1])
            
      article_chain = [start_url]
      while continue_crawl(article_chain, target_url):
          print(article_chain[-1])

          first_link = find_first_link(article_chain[-1])
          if not first_link:
              print("not a single link found!")
              break

          article_chain.append(first_link)

          time.sleep(0.5)  # Not to slow down wikipedia servers.
