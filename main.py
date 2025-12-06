import requests
import subprocess
from bs4 import BeautifulSoup

# Gets the HTML from the user input link
def getHTML(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        html = response.text
        print("Request successful!")

        return html

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Gets the html elements with the correct classes
def parseHTML(html):
    soup = BeautifulSoup(html, features="html.parser")
    blocks = soup.find_all(class_='rt-Text')

    strings = []

    for block in blocks:
        strings.append(block.string)

    return strings

# Gets the start and end indices of the strings that contain the article
def cleanStrings(strings):
    startInd = 0
    endInd = 0

    for i in range(len(strings)):
        if strings[i] == 'Listen':
            startInd = i+1
            break

    goodStartStrings = strings[startInd:-1]

    for i in range(len(goodStartStrings)):
        if goodStartStrings[i] == 'Share':
            endInd = i
            break

    goodStrings = goodStartStrings[:endInd]

    return goodStrings

# Removes empty strings from the list
def removeNoneStrings(strings):
    newStrings = []

    for s in strings:
        if s:
            newStrings.append(s)

    return newStrings

# Creates a text file with the cleaned strings to read the article
def createTextFile(strings, filename):
    with open(f"{filename}.txt", 'w') as file:
        for s in strings:
            file.write(s)
            file.write('\n')

    file.close()

# Optional: writes the HTML to a file for observability 
def writeHTML(html, filename):
    with open(f"{filename}.html", 'w') as file:
        file.write(html)

    file.close()

def main():
    filename = input('Enter a title with no spaces for the article: ')
    link = input('Enter the link to the Star Tribune article: ')

    html = getHTML(link)
    # Optional if you want to view the HTML
    writeHTML(html, filename)
    strings = parseHTML(html)
    cleanedStrings = cleanStrings(strings)
    cleanerStrings = removeNoneStrings(cleanedStrings)
    createTextFile(cleanerStrings, filename)

if __name__ == '__main__':
    main()
