import json
from Corpus import Corpus
from Preprocessor import Preprocessor
from TransitionMatrix import TransitionMatrix


class DeCypher(Corpus, Preprocessor, TransitionMatrix):
    """
    DeCypher class that inherits from the Corpus, Preprocessor and TransitionMatrix
    classes and their attributes/properties to decrypt passages into a 10-20 digit
    number
    """
    def __init__(self, max_iter=10**4):
        """
        Constructor for the DeCypher class: Creates an object of this class and initializes
        attributes/properties of this class
        """
        # multiple inheritance
        Corpus.__init__(self)  # initialize the inherited classes
        Preprocessor.__init__(self)
        TransitionMatrix.__init__(self)

        self.max_iter = max_iter  # set the property/attribute

    def decrypt(self, cryptogram):
        """
        Given a cryptogram, decrypts it into a 10-20 digit number and returns it
        """
        number = ""  # initialize the string form of the number
        # get the pairs of cryptographic passages and encryption key strings
        cryptographic_passages = self.extract_cryptographic_passages(cryptogram)
        # decrypt to plain text
        plain_text_passages = self.decrypt_cryptographic_passages(cryptographic_passages)
        # get a list of preprocessed sentences
        preprocessed_sentences = [self.preprocess(sentence) for sentence in self.sentences]

        # for every plain text passage
        for plain_text_passage in plain_text_passages:
            # determine the number and concatenate to the string
            number += self.determine_number(preprocessed_sentences, plain_text_passage)

        return int(number)  # convert to integer and return

    def determine_number(self, preprocessed_sentences, plain_text_passage):
        """
        Given a list of preprocessed sentences and a plain text passage, returns the
        number that is referred to by the plain text passasge
        """
        accuracy = 0.00  # initialize variables
        number = ""

        for idx1 in range(len(preprocessed_sentences)):  # for every preprocessed sentence
            preprocessed_sentence = preprocessed_sentences[idx1]
            if len(preprocessed_sentence) > 0:  # if the sentence is not a null string
                # if the sentence is not longer than the passage itself
                if len(preprocessed_sentence) <= len(plain_text_passage):
                    # extract the candidate for the first sentence from the passage
                    signature = plain_text_passage[:len(preprocessed_sentence)]

                    # calculate how similar the candidate is to the sentence
                    current_accuracy = 0.00  # initialize the current accuracy to 0
                    # for every character in the preprocessed sentence
                    for idx2 in range(len(preprocessed_sentence)):
                        # if the corresponding character in the candidate is the same
                        if signature[idx2] == preprocessed_sentence[idx2]:
                            current_accuracy += 1  # increase accuracy
                    # calculate current accuracy
                    current_accuracy /= len(preprocessed_sentence)

                    # if current accuracy is higher than default accuracy
                    if current_accuracy > accuracy:
                        accuracy = current_accuracy  # store it
                        number = str(idx1)  # store the corresponding number

        return number  # return the final number

    def decrypt_cryptographic_passages(self, cryptographic_passages):
        """
        Given a list of cryptographic passages and encryption key strings, iterates
        through each passage and decrypts each passage to a plain text passage and
        returns a list of these plain text passages
        """
        plain_text_passages = []  # initialize an empty list of plain text passages

        # for every pair of cryptographic passage and encryption key string
        for pair in cryptographic_passages:
            # unpack tuple
            cryptographic_passage, encryption_key_string = pair
            plain_text_passage = ""  # initialize null string
            # build the decryption key using the encryption key string
            decryption_key = self.build_decryption_key(encryption_key_string)

            # for every character in the cryptographic passage
            for character in cryptographic_passage:
                # retrieve the decrypted character
                decrypted_character = self.get_character(decryption_key[self.get_entrynum(character)])
                plain_text_passage += decrypted_character  # concatenate to plain text

            plain_text_passages.append(plain_text_passage)  # add the plain text passage to the list

        return plain_text_passages  # return the list of plain text passages

    def extract_cryptographic_passages(self, cryptogram):
        """
        Given a cryptogram, returns a list of pairs of cryptographic passages
        and their respective encryption key strings
        """
        cryptographic_passages = []  # initialize variables
        encryption_key_strings = []
        passage_start_idx, passage_end_idx = 0, 0
        encryption_start_idx, encryption_end_idx = 0, 0
        record_passage = True
        record_encryption = False
        alpha_count = 0

        # for every character
        for idx in range(len(cryptogram)):
            char = cryptogram[idx]

            if char.isalpha() or char.isspace():  # if the character is alphabetic or is a space
                # increase the number of alphabetic characters encountered consecutively by 1
                alpha_count += 1

            # if there have been two alphabetic characters in a row and the encryption key string
            # was being recorded
            if alpha_count == 2 and record_encryption:
                encryption_end_idx = idx - 1  # stop recording the encryption key string
                passage_start_idx = idx - 1  # start recording the passage
                # extract and append the encryption key string
                encryption_key_strings.append(cryptogram[encryption_start_idx:encryption_end_idx])
                record_encryption = False  # reset the booleans
                record_passage = True

            # if the character is a digit and a cryptographic passage is being recorded
            if char.isdigit() and record_passage:
                # reset the consecutive alphabetic letter count
                alpha_count = 0
                passage_end_idx = idx  # stop recording the cryptographic passage
                encryption_start_idx = idx  # start recording the encryption key string
                # extract and append the cryptographic passage
                cryptographic_passages.append(cryptogram[passage_start_idx:passage_end_idx])
                record_encryption = True  # reset the booleans
                record_passage = False

        return zip(cryptographic_passages, encryption_key_strings)  # return the pairs

    def build_decryption_key(self, encryption_key_string):
        """
        Given the encryption key string for a particular cryptographic passage,
        builds the decryption key and returns it
        """
        # build the encryption key from the string
        encryption_key = self.build_encryption_key(encryption_key_string)
        # reverse engineer the encryption key to get the decryption key
        decryption_key = self.reverse_encryption_key(encryption_key)
        return decryption_key  # return the decryption key

    def reverse_encryption_key(self, encryption_key):
        """
        Given an encryption key, returns the corresponding decryption key
        """
        decryption_key = [0] * len(encryption_key)  # initialize the decryption key

        for idx in range(len(encryption_key)):  # for every element in the encryption key
            element = encryption_key[idx]  # store the element
            decryption_key[element] = idx  # switch roles of element and idx

        return decryption_key  # return the decryption key

    def build_encryption_key(self, encryption_key_string):
        """
        Given an encryption key string, builds an encryption key and returns it
        """
        encryption_key = []  # initialize variables
        shift_length = len(self.book_name)
        start_idx, end_idx = 0, 0
        record = True

        # for every character in the string
        for idx in range(len(encryption_key_string)):
            char = encryption_key_string[idx]

            if char.isdigit() and record:  # if the character is a digit
                start_idx = idx  # start recording an element
                record = False

            # if the character is alphabetic or is a space
            if char.isalpha() or char.isspace() and not record:
                end_idx = idx  # stop recording the element
                element = int(encryption_key_string[start_idx:end_idx]) - shift_length  # shift the element back
                encryption_key.append(element)  # store the element
                record = True

        return encryption_key  # return the encryption key

    def set_max_iter(self, new_max_iter):
        """
        Given the new number of maximum iterations, sets the property of maximum
        iterations as this new limit
        """
        self.max_iter = new_max_iter  # set the new maximum number of iterations

    def get_max_iter(self):
        """
        Returns the value of the maximum number of iterations used by the decryptor
        """
        return self.max_iter  # return the new maximum number of iterations

    def write_number_textfile(self, result, text_filename):
        """
        Given the plain text/decrypted number and the text filename, creates a text
        file of that name and saves the plain text/decrypted number in that file
        """
        with open(text_filename, 'wb') as text_file:  # create the text file
            text_file.write(result)  # save the cryptogram in the file

    def write_result_json(self, result, json_filename):
        """
        Given the plain text/decrypted number and the json filename, creates a json
        file of that name and saves the plain text/decrypted number in that file
        """
        with open(json_filename, 'wb') as json_file:  # create the json file
            json.dump(result, json_file)  # save the cryptogram in the file


