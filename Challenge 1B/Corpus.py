import re
import json
import nltk.tokenize as tk


class Corpus:
    """
    Corpus class that stores the corpus as a string and important unique features
    related to the corpus such as tokens, sentences, number of tokens and number of
    sentences
    """
    def __init__(self, text=None, book_name=None):
        """
        Constructor for the Corpus class: creates an object of this class  and
        initializes properties
        """
        self.text = text  # initialize properties
        self.book_name = book_name

    @property
    def tokens(self):
        """
        Splits the corpus into its constituent tokens and sets it to the computed
        property, self.tokens
        """
        return tk.word_tokenize(self.text)  # return the list of tokens in the corpus

    @property
    def sentences(self):
        """
        Splits the corpus into its constituent sentences and sets it to the computed
        property, self.sentences
        """
        # use regex to split the sentences and return the list
        return list([sentence for sentence in re.split(r' *[\.\?!][\'"\)\]]* *', self.text)
                     if sentence != ""])

    @property
    def num_tokens(self):
        """
        Computes the number of tokens and sets it to the computed property, self.num_tokens
        """
        return len(self.tokens)  # return the number of tokens

    @property
    def num_sentences(self):
        """
        Computes the number of sentences and sets it to the computed property, self.sentences
        """
        return len(self.sentences)  # return the number of sentences

    def set_text(self, text):
        """
        Sets the property, self.text to the externally provided input string, text
        """
        self.text = str(text)  # set the property to the input

    def set_book_name(self, new_book_name):
        """
        Sets the property, self.book_name to the externally provided input string, new_book_name
        """
        self.book_name = new_book_name  # set the property to the input

    def get_text(self):
        """
        Returns the textual content of the corpus
        """
        return str(self.text)  # return the textual content of the corpus

    def get_book_name(self):
        """
        Returns the name of the book being used for encryption
        """
        return self.book_name  # return the name of the book

    def get_tokens(self):
        """
        Returns the computed property, the list of tokens in the corpus
        """
        return self.tokens  # return the list of tokens in the corpus

    def get_sentences(self):
        """
        Returns the computed property, the list of sentences in the corpus
        """
        return self.sentences  # return the list of sentences in the corpus

    def get_num_tokens(self):
        """
        Returns the computed property, the number of tokens in the corpus
        """
        return self.num_tokens  # return the number of tokens in the corpus

    def get_num_sentences(self):
        """
        Returns the computed property, the number of sentences in the corpus
        """
        return self.num_sentences  # return the number of sentences in the corpus

    def read_corpus_json(self, json_filename):
        """
        Given the name of a json file containing a string, opens said json file,
        reads the string and sets the text of the corpus as the imported string
        """
        with open(json_filename, 'rb') as json_file:  # open the string
            text = json.load(json_file)  # load the string

        json_file.close()  # close the json file
        self.set_text(text)  # set the imported string as the text of the corpus

    def write_corpus_json(self, json_filename):
        """
        Given the name of a json file, creates said json file and writes the string
        of the textual content of the corpus into the json file
        """
        with open(json_filename, 'wb') as json_file:  # open the json file
            json.dump(self.text, json_file)  # write the string into the json file

    def read_corpus_textfile(self, text_filename):
        """
        Given the name of a text file containing a string, opens said json file,
        reads the string and sets the text of the corpus as the imported string
        """
        with open(text_filename, 'rb') as text_file:  # open the text file
            text = text_file.read()  # load the string

        text_file.close()  # close the text file
        self.set_text(text)  # set the imported string as the text of the corpus

    def write_corpus_textfile(self, text_filename):
        """
        Given the name of a text file, opens said text file and writes the string
        of the textual content of the corpus into the text file
        """
        with open(text_filename, 'wb') as text_file:  # open the text file
            text_file.write(self.text)  # write the string into the text file


