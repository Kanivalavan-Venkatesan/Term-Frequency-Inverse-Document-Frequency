"""
Implementation of term frequency inverse document frequency.
"""
# Import the required modules
import json
import math
import numpy as np


def main():
    count = 0
    uniqueWords = set()
    tf_idfMatrix, tf_idfValues, headerRow = [], [], []
    fileName = input("Enter the file name with extension: ").lower()
    readFile(fileName)
    documents = create_documents(fileName)
    for document_key, document_content in documents.items():
        for content in document_content:
            uniqueWords.add(content)
    # Sort the words list
    uniqueWords = sorted(uniqueWords)
    tf_idfMatrix.append(uniqueWords)
    print("Builidng tf_idf matrix, Please wait !!!")
    # Calculate the term frequency inverse document frequency
    for document_key, document_content in documents.items():
        for term in uniqueWords:
            if term in sorted(set(documents[document_key])):
                tf = term_frequency(term, document_content)
                idf = inverse_document_frequency(term, documents)
                tf_idf = tf * idf
                tf_idfValues.append(str("{0:.2f}".format(tf_idf)))
            else:
                tf_idfValues.append(str(0.00000))
        tf_idfMatrix.append(tf_idfValues)
        tf_idfValues = []
    # Length of matrix
    length = len(tf_idfMatrix)
    # Transpose the list of list to write in .csv file
    tf_idfMatrix = np.array(tf_idfMatrix).T.tolist()
    # Write the data in .csv file
    file = fileName[:fileName.rfind('.')]
    for i in range(1, length):
        headerRow.append("d" + str(i))
    headerRow.insert(0, "Words")
    outfile = open(file+"_tfidf.csv", "w")
    outfile.write(",".join(headerRow)+"\n")
    outfile.close()
    for tf_idf in tf_idfMatrix:
        outfile = open(file+"_tfidf.csv", "a")
        outfile.write(",".join(tf_idf))
        outfile.write("\n")
    outfile.close()
    print("Completed!!!, Please check the file")


# Read the files and write the contents into input.txt
def readFile(fileName):
    i = 1
    file = fileName[:fileName.rfind('.')]
    headerRow = "document_key, document_contents\n"
    outfile = open(file+"_input.txt", "w")
    outfile.write(headerRow)
    outfile.close()
    # for file in fileName:
    fileExtension = fileName[fileName.rfind('.') + 1:]
    if fileExtension != "json":
        # Read the .txt files
        infile = open(fileName, "r")
        for line in infile:
            # Remove the punctuation marks from the text
            line = clean_document_contents(line)
            outfile = open(file+"_input.txt", "a")
            outfile.write("d" + str(i) + "," + " " + " ".join(line) + "\n")
            i += 1
        outfile.close()
        infile.close()
    else:
        # Read the .json files
        with open(fileName) as json_data:
            data = json.load(json_data)
            for key in data["paper"]:
                for content in key["review"]:
                    line = clean_document_contents(content["text"])
                    outfile = open(file+"_input.txt", "a")
                    outfile.write("d" + str(i) + "," + " " + " ".join(line) + "\n")
                    i += 1
                outfile.close()


def create_documents(fileName):
    """
    Cleans a corpus and returns a dictionary with unique keys for each document
    and values containing a sequence of terms (i.e. document contents).
    """

    document = {}
    file = fileName[:fileName.rfind('.')]

    documents_file = open(file+"_input.txt", "r")
    header = documents_file.readline()
    line = documents_file.readline()


    while line != "":
        row = line.rstrip().split(",")
        document_key = row[0]
        document_contents = row[1]
        document_contents = clean_document_contents(document_contents)
        document[document_key] = document_contents
        line = documents_file.readline()

    # ...

    return document


def clean_document_contents(document_contents):
    """
    Cleans document content of all non-word characters, makes all words
    lowercase, and returns a list of strings.

    :param document_content: A string representing the contents of a document
    :type document_content: string
    """
    clean_document_contents = ""
    startPosition = document_contents.find('|', 20)
    endPosition = document_contents.find("http")
    if document_contents[0:18].isdigit():
        if document_contents[(startPosition + 1):(startPosition + 3)] == 'RT':
            document_contents = document_contents[document_contents.find(':', startPosition):endPosition]
            for letter in document_contents:
                if isWordCharacter(letter):
                    clean_document_contents += letter
        else:
            document_contents = document_contents[startPosition:endPosition]
            for letter in document_contents:
                if isWordCharacter(letter):
                    clean_document_contents += letter
    else:
        for letter in document_contents:
            if isWordCharacter(letter):
                clean_document_contents += letter
    clean_document_contents = clean_document_contents.lower()
    document_content_list = clean_document_contents.strip().split()
    clean_document_contents = ""
    return document_content_list

# Clean the contents
def isWordCharacter(letter):
    # letter is A-Za-z or (space)
    if (65 <= ord(letter) <=122 and not 96 >= ord(letter) >= 90) or ord(letter) == 32:
        return letter


def term_frequency(term, document_content):
    """
    Computes the term frequency statistic for a term in the document at document_key

    :param term: An word
    :type term: string
    :param document_content: A list of strings containing the terms from a document
    :type term: list
    """
    term_count = 0
    word_count = 0
    for word in document_content:
        if word == term:
            term_count += 1
        word_count += 1
    tf = term_count / word_count
    return tf


def inverse_document_frequency(term, documents):
    """
    Computes the inverse document frequency statistic for a term given a
    collection of documents.

    :param term: An word
    :type term: string
    :param documents: A dictionary with unique keys for each document
    and values containing a sequence of terms (i.e document_content)s
    :type term: dictonary

    """
    count = 0
    for document in documents:
        if term in documents[document]:
            count += 1
    idf = math.log10(len(documents)/count)
    return idf


# Call the main()
main()
