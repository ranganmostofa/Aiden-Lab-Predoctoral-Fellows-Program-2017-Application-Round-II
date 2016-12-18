class Preprocessor:
    """
    Preprocessor class that preprocesses the textual content of a Corpus object
    by converting all characters to lowercase and removing all non alphabetic characters
    """
    def __init__(self, lowercase=True, alpha=True):
        """
        Constructor for the Preprocessor class: creates an object of this class and
        initializes properties
        """
        self.lowercase = lowercase  # initialize boolean properties
        self.alpha = alpha

    def decapitalize(self, text):
        """
        Given the textual content of a corpus, converts all alphabetic characters
        to lowercase and returns this lowercased version
        """
        if self.lowercase:  # if the preprocessor is allowed to convert to lowercase
            return text.lower()  # convert to lowercase and return

        return text  # otherwise return original text

    def remove_nonalpha(self, text):
        """
        Given the textual content of a corpus, removes all characters except the alphabetic
        characters (and space) and returns this filtered alphabetic string
        """
        if self.alpha:  # if removal of non alphabetic characters is allowed
            # initialize a null string that is to later contain the preprocessed string
            alpha_text = ""

            for character in text:  # for every character in the text

                # if the character is alphabetic or is a space
                if character.isalpha() or character == " ":
                    alpha_text += character  # add it to the initialized string above
                # if the character is a newline or carriage return
                elif character == "\r" or character == "\n":
                    alpha_text += " "  # add a space

            return alpha_text  # return the preprocessed string

        return text  # otherwise return the original text

    def remove_consecutive_spaces(self, text):
        """
        Given the textual content of a corpus, removes all consecutive spaces and returns this
        filtered alphabetic string
        """
        # initialize a null string that is to later contain the preprocessed string
        preprocessed_text = ""

        for idx in range(len(text) - 1):  # for every character

            # if it is not the case that the character itself and the one following
            # it are spaces
            if not(text[idx] == " " and text[idx + 1] == " "):
                preprocessed_text += text[idx]  # add this character to the initialized string above

        return preprocessed_text  # return the preprocessed string

    def preprocess(self, text):
        """
        Given a text represented as a string, returns a preprocessed version of this string
        NOTE: "preprocessed" above depends on the values of the boolean attributes of a
              particular object of this class
        """
        decapitalized_text = self.decapitalize(text)  # convert all characters to lowercase
        alpha_text = self.remove_nonalpha(decapitalized_text)  # remove all non alphabetic characters
        # remove all consecutive spaces
        preprocessed_text = self.remove_consecutive_spaces(alpha_text)
        return preprocessed_text  # return the final preprocessed text

    def set_lowercase(self, lowercase):
        """
        Given a boolean, sets this input boolean as the new value of the property,
        self.lowercase
        """
        self.lowercase = lowercase  # set the input boolean as the new value of the property

    def set_alpha(self, alpha):
        """
        Given a boolean, sets this input boolean as the new value of the property,
        self.alpha
        """
        self.alpha = alpha  # set the input boolean as the new value of the property

    def get_lowercase(self):
        """
        Returns the boolean property which indicates whether the preprocessor converts
        all characters to lowercase
        """
        return self.lowercase  # returns the lowercase boolean property

    def get_alpha(self):
        """
        Returns the boolean property which indicates whether the preprocessor removes
        all non alphabetic characters
        """
        return self.alpha  # returns the alphabetic boolean property


