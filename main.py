import googlesearch
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from tkinter import *

def createUI(root):
    siteGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    queryGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    amountGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    outputGrid = Frame(root, width=450, height=50, padx=10, pady=10)

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    siteLabel = Label(siteGrid, text="Site: ")
    siteEntry = Entry(siteGrid, width=100)

    queryLabel = Label(queryGrid, text="Search: ")
    queryEntry = Entry(queryGrid, width=100)

    resultsLabel = Label(amountGrid, text="Results Amount: ")
    resultsEntry = Entry(amountGrid, width=5)

    outputLabel = Label(outputGrid, text="Output: ")
    outputText = Text(outputGrid)
    outputText.configure(state="disabled", bg="#e9e9e9")

    siteLabel.grid(row=0, column=0, sticky=W)
    siteEntry.grid(row=0, column=1)

    queryLabel.grid(row=0, column=0, sticky=W)
    queryEntry.grid(row=0, column=1)

    resultsLabel.grid(row=0, column=0, sticky=W)
    resultsEntry.grid(row=0, column=1)

    outputLabel.grid(row=0, column=0, sticky=W)
    outputText.grid(row=1, column=0)

    siteGrid.grid(row=0, column=0, sticky=NW)
    queryGrid.grid(row=1, column=0, sticky=NW)
    amountGrid.grid(row=2, column=0, sticky=NW)
    outputGrid.grid(row=3, column=0, sticky=NW)

def googleQuery(query, resultsAmt, site=None):
    resultsDict = {}

    searchQuery = query

    if site is not None:
        searchQuery = f"site:{site} {query}" 

    driver = webdriver.Chrome() 

    for j in googlesearch.search(searchQuery, tld="com", lang="en", num=resultsAmt, stop=resultsAmt, pause=2):
        parsedQuery = urllib.parse.quote_plus(searchQuery)
        requestsSearch = f"https://google.com/search?q={parsedQuery}"
        print(requestsSearch)

        driver.get(requestsSearch)
        content = driver.page_source.encode("utf-8").strip()
        soup = BeautifulSoup(content, "html.parser")

        titles = soup.findAll("h3", class_="LC20lb")

        count = 0
        for t in titles:
            if count < resultsAmt:
                parTitle = str(t)
                parTitle = parTitle[19:]
                parTitle = parTitle[:-5]

                resultsDict[parTitle] = j

                count += 1

            else:
                break

    driver.quit()

    return resultsDict

def main():
    root = Tk()
    createUI(root)
    root.mainloop()

    #query = "C++ arrays"
    #resultsDict = googleQuery(query, 1, "stackoverflow.com")

    #for k, v in resultsDict.items():
    #    print(f"\nTitle: {k}\nURL: {v}\n")

    return 0

main()