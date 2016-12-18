class TransitionMatrix:
    """
    Transition Matrix class that builds the transition matrix which consists of the
    transition probabilities of each character in the preprocessed text
    """
    def __init__(self, preprocessed_text="", matrix=None):
        """
        Constructor for the TransitionMatrix class: Creates an object of this class
        and initializes attributes/properties
        """
        self.preprocessed_text = preprocessed_text  # initialize properties
        self.matrix = matrix

    def build_matrix(self):
        """
        Computes the transition probability of each character in the preprocessed text,
        fills in the entries of the transition matrix and stores this as a property of
        the object
        """
        matrix = self.initialize_matrix()  # initialize an empty transition matrix
        character_count = self.get_character_count()  # get the number of appearances of each character

        for idx in range(len(self.preprocessed_text) - 1):  # for every character in the preprocessed text
            rownum = self.get_entrynum(self.preprocessed_text[idx])  # get the row number
            colnum = self.get_entrynum(self.preprocessed_text[idx + 1])  # get the column number
            # store the probability in the matrix
            if character_count[self.preprocessed_text[idx]] != 0:
                matrix[rownum][colnum] += 1.0 / character_count[self.preprocessed_text[idx]]

        self.set_matrix(matrix)  # set the transition matrix to the relevant attribute of the object

    def initialize_matrix(self):
        """
        Creates an empty transition matrix containing only zeros and returns this matrix
        """
        matrix = list([])  # initialize an empty matrix
        character_count = self.get_character_count()  # get the number of appearances of each character

        for char in character_count.keys():  # for every character in the preprocessed text
            matrix.append(list([1.0 / (sum(character_count.values()) / float(len(character_count.values())))] *
                               len(character_count.keys())))  # append a row of infinitesimal floating point numbers

        return matrix  # return the transition matrix of zeros

    def get_character_count(self):
        """
        Creates a dictionary mapping characters (found in the preprocessed text) to
        the number of appearances in the preprocessed text (integers), and returns
        this dictionary
        """
        chars = {}  # initialize an empty dictionary

        for char in self.preprocessed_text:  # for every character in the preprocessed text

            if char not in chars.keys():  # if the character is not already in the dictionary
                chars[char] = 1  # add the key and set the number of occurrences to 1
            else:  # otherwise
                chars[char] += 1   # increase the count by 1

        return chars  # return the dictionary

    def get_entrynum(self, character):
        """
        Given a character, returns the row/column number of the entry pertaining to
        character in the transition matrix
        """
        ascii = ord(character)  # get the ascii of the character

        if 97 <= ascii <= 122:  # if the character is alphabetic
            return ascii - 97  # map it to the row/column number
        elif ascii == 32:  # if the character is a space
            return ascii - 6  # map it to the row/column number

    def get_character(self, entrynum):
        """
        Given a row/column number of an entry of the transition matrix, returns the
        character that this row/column number corresponds to
        """
        if 0 <= entrynum <= 25:  # if the row/column number is the first 26 of the transition matrix
            return chr(entrynum + 97)  # return the alphabetic character
        elif entrynum == 26:  # if the row/column number is the last of the transition matrix
            return chr(entrynum + 6)  # return space

    def set_preprocessed_text(self, preprocessed_text):
        """
        Given a text as a string, sets this string as the new preprocessed text
        """
        self.preprocessed_text = str(preprocessed_text)  # set the preprocessed text

    def set_matrix(self, matrix):
        """
        Given a matrix as a list of lists, sets this as the new transition matrix
        """
        self.matrix = list(matrix)  # set the transition matrix

    def get_preprocessed_text(self):
        """
        Returns the attribute, preprocessed text
        """
        return self.preprocessed_text  # return the preprocessed text

    def get_matrix(self):
        """
        Returns the attribute, transition matrix
        """
        return self.matrix  # return the transition matrix


