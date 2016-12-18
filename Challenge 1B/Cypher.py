import json
import math
import random
from Corpus import Corpus
from Preprocessor import Preprocessor
from TransitionMatrix import TransitionMatrix


class Cypher(Corpus, Preprocessor, TransitionMatrix):
    """
    Cypher class that inherits from the Corpus, Preprocessor and TransitionMatrix
    classes and their attributes/properties to encrypt a 10-20 digit number
    using the Markov Chain Metropolis-Hastings Algorithm
    """

    def __init__(self, max_iter=10**4, passage_length=10, passage_min_char_count=700):
        """
        Constructor for the Cypher class: Creates an object of this class and initializes
        attributes/properties of this class
        """
        # multiple inheritance
        Corpus.__init__(self)  # initialize the inherited classes
        Preprocessor.__init__(self)
        TransitionMatrix.__init__(self)

        self.max_iter = max_iter  # set the properties/attributes
        self.passage_length = passage_length
        self.passage_min_char_count = passage_min_char_count

    def encrypt(self, number):
        """
        Given a 10-20 digit number, uses the Markov Chain Metropolis Algorithm to encrypt
        the input number
        """
        cryptogram = ""  # initialize the cipher
        raw_passages = self.extract_plain_text(number)  # extract the corresponding plain text

        for raw_passage in raw_passages:  # for every raw passage
            encrypted_passage = ""  # initialize the encrypted text to a null string
            encryption_key = self.build_encryption_key(raw_passage)  # build the encryption key
            encryption_key_string = self.build_encryption_key_string(encryption_key)  # build the corresponding string

            for character in raw_passage:  # for every character in the plain text
                # encrypt the character
                encrypted_character = self.get_character(encryption_key[self.get_entrynum(character)])
                # add the encrypted character to the encrypted passage null string initialized above
                encrypted_passage += encrypted_character

            # add the encrypted passages with the encryption key string as a delimiter
            cryptogram += encrypted_passage + encryption_key_string

        return cryptogram  # return the cryptogram

    def extract_plain_text(self, number):
        """
        Given a 10-20 digit number, chops up the number to a random number of
        pieces, builds the passage corresponding to each piece and returns this
        list of raw passages
        """
        raw_passages = []  # initialize list of raw passages
        num_string = str(number)  # get the string of the number
        # get the list of preprocessed numbers
        preprocessed_sentences = [self.preprocess(sentence) for sentence in self.sentences]

        while len(num_string) > 0:  # while there are more numbers to chop
            # get the number of digits randomly
            num_digits = random.randint(1, len(str(len(preprocessed_sentences))))

            # if the random number of digits cannot be afforded by the number of remaining digits
            if num_digits > len(num_string):
                num_digits = len(num_string)  # assign the number of remaining digits
                # if the string starts with a 0, the 0 will be lost after the casting to int
            if num_string[:num_digits][0] == '0':  # if the first digit is 0
                num_digits = 1  # take only that digit

            start_sentence_idx = int(num_string[:num_digits])  # get the start sentence index

            # if the start sentence index is more than the number of sentences
            if start_sentence_idx >= len(preprocessed_sentences):
                num_digits -= 1  # cut off a digit
                start_sentence_idx = int(num_string[:num_digits])  # recalculate the start sentence index

            # get the raw passage corresponding to this start sentence index
            raw_passage = self.extract_passage(preprocessed_sentences, start_sentence_idx)
            # append to the list
            raw_passages.append(raw_passage)

            if num_digits == len(num_string):  # if this is the last iteration
                num_string = ""  # trim the num string variable down to a null string
            else:  # otherwise
                num_string = num_string[num_digits:]  # trim it normally

        return raw_passages  # return the raw passages

    def extract_passage(self, preprocessed_sentences, start_idx):
        """
        Given a list of preprocessed sentence found in the book and the index
        the first sentence to be included in the passage, builds the passage
        and returns it
        """
        delimiter = " "  # initialize the delimiter
        end_idx = start_idx + self.passage_length  # calculate the end index

        if len(preprocessed_sentences) < end_idx:  # if the corpus is not long enough
            end_idx = len(preprocessed_sentences)  # let the end index be the pointer to the last sentence

        # join the sentences to build the passage
        raw_passage = delimiter.join(preprocessed_sentences[start_idx:end_idx])

        if len(raw_passage) < self.passage_min_char_count:  # ensure that the passage has enough characters
            # as long as the passage is not long enough and there are more sentences to add
            while len(raw_passage) < self.passage_min_char_count and len(preprocessed_sentences) > end_idx:
                end_idx += 1
                raw_passage = delimiter.join(preprocessed_sentences[start_idx:end_idx])  # add the next sentence

        return raw_passage  # return the final raw passage

    def build_encryption_key_string(self, encryption_key):
        """
        Given an encryption key, creates a string that has the encryption key
        encoded in it and returns this string
        """
        encryption_key_string = ""  # initialize a null string
        # get the length of the book name (See Readme for more details)
        signature_number = len(self.get_book_name())
        for num in encryption_key:  # for every element in the encryption key list
            # shift the number to the right of the real number line by the signature calculated above
            encryption_key_string += str(num + int(signature_number))
            if encryption_key.index(num) != len(encryption_key) - 1:  # if it is not the last element
                # concatenate a random alphabetic character at the end of each shifted element
                encryption_key_string += self.get_character(random.randrange(len(self.get_matrix())))
        return encryption_key_string  # return the encryption string

    def build_encryption_key(self, raw_text):
        """
        Given the raw text, builds an encryption key specific to the raw text using
        the Metropolis Algorithm
        """
        count_iter = 0  # initialize the number of iterations
        encryption_key = range(len(self.get_matrix()))  # initialize an encryption key list

        while count_iter <= self.max_iter:  # while the number of iterations do not exceed the limit
            new_encryption_key = list(encryption_key)  # make a copy of the current encryption key

            idx1 = random.randrange(len(encryption_key))  # get random indices
            idx2 = random.randrange(len(encryption_key))
            # switch the elements of the random integers
            new_encryption_key[idx1], new_encryption_key[idx2] = new_encryption_key[idx2], new_encryption_key[idx1]

            # compute the log likelihood of the encryption keys before and after the change
            old_score, new_score = self.compute_log_likelihood(raw_text, encryption_key), \
                                   self.compute_log_likelihood(raw_text, new_encryption_key)

            if new_score < old_score:  # if the new score is worse
                encryption_key = list(new_encryption_key)  # keep the change
            elif new_score == old_score:  # if the score is same
                count_iter += 1  # increase the counter and continue
                continue
            else:  # otherwise
                rand = random.random()  # roll a die
                # calculate the threshold probability
                threshold_probability = math.pow(math.e, round(old_score - new_score, 5))

                if threshold_probability <= rand:  # if the random number is higher than the threshold probability
                    encryption_key = list(new_encryption_key)  # keep the change
                else: # otherwise
                    new_encryption_key = list(encryption_key)  # discard the change

            count_iter += 1  # increase the counter every iteration

        return encryption_key  # return the final encryption key

    def compute_log_likelihood(self, raw_text, encryption_key):
        """
        Given a raw text and a test encryption key, measures the log likelihood or
        chance of the given test encryption key being the actual encryption key
        """
        sigma = 0.00  # initialize sum to zero
        transition_matrix = self.get_matrix()  # get the transition matrix

        for idx in range(len(raw_text) - 1):  # for every character in the raw text
            # find the entry numbers of the character in the transition matrix
            rownum = encryption_key[self.get_entrynum(raw_text[idx])]
            colnum = encryption_key[self.get_entrynum(raw_text[idx + 1])]
            # access the transition probability
            transition_probability = transition_matrix[rownum][colnum]
            sigma += math.log(transition_probability)  # add the log of that probability to the total

        return sigma  # return the sum/log likelihood

    def set_max_iter(self, new_max_iter):
        """
        Given the new number of maximum iterations, sets the property of maximum
        iterations as this new limit
        """
        self.max_iter = new_max_iter  # set the new maximum number of iterations

    def set_passage_length(self, new_passage_length):
        """
        Given a new passage length, sets the property of passage length (in terms
        of number of sentences) as this new passage length
        """
        self.passage_length = new_passage_length  # sets the new passage length

    def set_passage_min_char_count(self, new_passage_min_char_count):
        """
        Given a new minimum number of characters in each encrypted passage, sets
        the property of minimum number of characters as this new limit
        """
        self.passage_min_char_count = new_passage_min_char_count  # set the new minimum number of characters

    def get_max_iter(self):
        """
        Returns the value of the maximum number of iterations used by the encryptor
        """
        return self.max_iter  # return the new maximum number of iterations

    def get_passage_length(self):
        """
        Returns the passage length of each encrypted passage interms of number of sentences
        """
        return self.passage_length  # return the length of the passage

    def get_passage_min_char_count(self):
        """
        Returns the minimum number of characters that must be in each encrypted passage
        """
        return self.passage_min_char_count  # return the minimum number of characters

    def write_cryptogram_textfile(self, cryptogram, text_filename):
        """
        Given the cipher text and the text filename, creates a text file of that name
        and saves the cipher in that file
        """
        with open(text_filename, 'wb') as text_file:  # create the text file
            text_file.write(cryptogram)  # save the cryptogram in the file

    def write_cryptogram_json(self, cryptogram, json_filename):
        """
        Given the cipher text and the json filename, creates a json file of that name
        and saves the cipher in that file
        """
        with open(json_filename, 'wb') as json_file:  # create the json file
            json.dump(cryptogram, json_file)  # save the cryptogram in the file


