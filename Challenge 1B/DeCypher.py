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

        :param cryptogram:
        :return:
        """
        number = ""
        cryptographic_passages = self.extract_cryptographic_passages(cryptogram)
        plain_text_passages = self.decrypt_cryptographic_passages(cryptographic_passages)
        preprocessed_sentences = [self.preprocess(sentence) for sentence in self.sentences]

        for plain_text_passage in plain_text_passages:
            number += self.determine_number(preprocessed_sentences, plain_text_passage)

        return int(number)

    def determine_number(self, preprocessed_sentences, plain_text_passage):
        """

        :param preprocessed_sentences:
        :param plain_text_passage:
        :return:
        """
        accuracy = 0.00
        number = ""

        for idx1 in range(len(preprocessed_sentences)):
            preprocessed_sentence = preprocessed_sentences[idx1]
            if len(preprocessed_sentence) > 0:
                if len(preprocessed_sentence) <= len(plain_text_passage):
                    signature = plain_text_passage[:len(preprocessed_sentence)]

                    current_accuracy = sum([1 if signature[idx2] == preprocessed_sentence[idx2] else 0 for idx2 in
                                            range(len(preprocessed_sentence))]) / float(len(preprocessed_sentence))

                    if current_accuracy > accuracy:
                        accuracy = current_accuracy
                        number = str(idx1)

        return number

    def decrypt_cryptographic_passages(self, cryptographic_passages):
        """

        :param cryptographic_passages:
        :return:
        """
        plain_text_passages = []

        for pair in cryptographic_passages:
            cryptographic_passage, encryption_key_string = pair
            plain_text_passage = ""
            decryption_key = self.build_decryption_key(encryption_key_string)

            for character in cryptographic_passage:
                decrypted_character = self.get_character(decryption_key[self.get_entrynum(character)])
                plain_text_passage += decrypted_character

            plain_text_passages.append(plain_text_passage)

        return plain_text_passages

    def extract_cryptographic_passages(self, cryptogram):
        """

        :param cryptogram:
        :return:
        """
        cryptographic_passages = []
        encryption_key_strings = []
        passage_start_idx, passage_end_idx = 0, 0
        encryption_start_idx, encryption_end_idx = 0, 0
        record_passage = True
        record_encryption = False
        alpha_count = 0

        for idx in range(len(cryptogram)):
            char = cryptogram[idx]

            if char.isalpha() or char.isspace():
                alpha_count += 1

            if alpha_count == 2 and record_encryption:
                encryption_end_idx = idx - 1
                passage_start_idx = idx - 1
                encryption_key_strings.append(cryptogram[encryption_start_idx:encryption_end_idx])
                record_encryption = False
                record_passage = True

            if char.isdigit() and record_passage:
                alpha_count = 0
                passage_end_idx = idx
                encryption_start_idx = idx
                cryptographic_passages.append(cryptogram[passage_start_idx:passage_end_idx])
                record_encryption = True
                record_passage = False

        return zip(cryptographic_passages, encryption_key_strings)

    def build_decryption_key(self, encryption_key_string):
        """

        :param encryption_key_string:
        :return:
        """
        encryption_key = self.build_encryption_key(encryption_key_string)
        decryption_key = self.reverse_encryption_key(encryption_key)
        return decryption_key

    def reverse_encryption_key(self, encryption_key):
        """

        :param encryption_key:
        :return:
        """
        decryption_key = [0] * len(encryption_key)

        for idx in range(len(encryption_key)):
            element = encryption_key[idx]
            decryption_key[element] = idx

        return decryption_key

    def build_encryption_key(self, encryption_key_string):
        """

        :param encryption_key_string:
        :return:
        """
        encryption_key = []
        shift_length = len(self.book_name)
        start_idx, end_idx = 0, 0
        record = True

        for idx in range(len(encryption_key_string)):
            char = encryption_key_string[idx]

            if char.isdigit() and record:
                start_idx = idx
                record = False

            if char.isalpha() or char.isspace() and not record:
                end_idx = idx
                element = int(encryption_key_string[start_idx:end_idx]) - shift_length
                encryption_key.append(element)
                record = True

        return encryption_key

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
        with open(text_filename, 'wb') as text_file:
            text_file.write(result)

    def write_result_json(self, result, json_filename):
        """
        Given the plain text/decrypted number and the json filename, creates a json
        file of that name and saves the plain text/decrypted number in that file
        """
        with open(json_filename, 'wb') as json_file:
            json.dump(result, json_file)



















