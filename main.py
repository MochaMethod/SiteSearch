import googlesearch
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from tkinter import *
import sys

DRIVER = None

def output(root, outputWidget, message):
    outputWidget.insert("end", message)
    outputWidget.see("end")

def exit():
    if DRIVER is not None:
        DRIVER.quit()
    sys.exit()

def googleQuery(query, resultsAmt, site=None):
    resultsDict = {}

    searchQuery = query

    if site is not None:
        searchQuery = f"site:{site} {query}" 

    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options) 
    global DRIVER
    DRIVER = driver

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

def handleSubmit(root, outputWidget, queryEntry, resultsEntry, siteEntry):
    query = queryEntry.get()
    amount = int(resultsEntry.get())
    site = siteEntry.get()

    resultsDict = googleQuery(query, amount, site)
    for k, v in resultsDict.items():
        message = (f"\nTitle: {k}\nURL: {v}\n")
        print(message)
        output(root, outputWidget, message)
    

def createUI(root):
    optionsGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    siteGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    queryGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    amountGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    submitGrid = Frame(root, width=450, height=50, padx=5, pady=5)
    outputGrid = Frame(root, width=450, height=50, padx=10, pady=10)

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    menuBar = Menu(optionsGrid)
    menuBar.add_command(label="Exit", command=exit)

    root.config(menu=menuBar)
    
    queryLabel = Label(queryGrid, text="* Search: ")
    queryEntry = Entry(queryGrid, width=110)

    resultsLabel = Label(amountGrid, text="* Desired amount of results: ")
    resultsEntry = Entry(amountGrid, width=5)

    siteLabel = Label(siteGrid, text="Site-specific search: ")
    siteEntry = Entry(siteGrid, width=100)

    outputLabel = Label(outputGrid, text="Output: ")
    outputText = Text(outputGrid, width=100)
    outputText.configure(bg="#e9e9e9")
    
    resultsSubmit = Button(submitGrid, text="Search", command=lambda: handleSubmit(root, outputText, queryEntry, resultsEntry, siteEntry))

    queryLabel.grid(row=0, column=0, sticky=W)
    queryEntry.grid(row=0, column=1)

    resultsLabel.grid(row=0, column=0, sticky=W)
    resultsEntry.grid(row=0, column=1)

    resultsSubmit.grid(row=0, column=2, padx=25)

    siteLabel.grid(row=0, column=0, sticky=W)
    siteEntry.grid(row=0, column=1)

    outputLabel.grid(row=0, column=0, sticky=W)
    outputText.grid(row=1, column=0)

    queryGrid.grid(row=0, column=0, sticky=NW)
    amountGrid.grid(row=1, column=0, sticky=NW)
    siteGrid.grid(row=2, column=0, sticky=NW)
    submitGrid.grid(row=0, column=1, sticky=NE)
    outputGrid.grid(row=3, column=0, sticky=NW)

    root.bind(
        "<Return>", 
        lambda root=root, outputText=outputText, queryEntry=queryEntry, amountEntry=resultsEntry, siteEntry=siteEntry: handleSubmit(
            root, outputText, queryEntry, resultsEntry, siteEntry
            )
        )

def main():
    root = Tk()
    createUI(root)
    root.mainloop()

    query = "C++ arrays"
    resultsDict = googleQuery(query, 1, "stackoverflow.com")

    for k, v in resultsDict.items():
        print(f"\nTitle: {k}\nURL: {v}\n")

    return 0

main()