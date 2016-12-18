from Cypher import Cypher

print "Please enter the 10-20 digit number to be encrypted: "

number = input()
book_name = 'war_and_peace'
corpus_filename = 'war_and_peace.txt'
cryptogram_textfile = 'cryptogram.txt'
cryptogram_json = 'cryptogram.json'


wnp_encryptor = Cypher()
wnp_encryptor.read_corpus_textfile(corpus_filename)
wnp_encryptor.set_book_name(book_name)

preprocessed_wnp_text = wnp_encryptor.preprocess(wnp_encryptor.get_text())  # preprocess the text and store it

wnp_encryptor.set_preprocessed_text(preprocessed_wnp_text)

wnp_encryptor.build_matrix()  # build the transition matrix

cryptogram = wnp_encryptor.encrypt(number)  # get the cryptogram

wnp_encryptor.write_cryptogram_textfile(cryptogram, cryptogram_textfile)  # write the cipher into a text file

wnp_encryptor.write_cryptogram_json(cryptogram, cryptogram_json)  # or save it in a json file


