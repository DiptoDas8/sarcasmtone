import sys
from translate import Translator

translator= Translator(to_lang='en', from_lang='bn')

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
import codecs

for i in range(2, 31):
    filename = str(i)+'.txt'
    bn_file = open(filename, 'rb')
    en_file = open('./english/'+filename, 'a')
    bn_file_text = bn_file.read()
    '''for line in bn_file:
        bn_file_text += repr(line)'''
    bn_file_text = bn_file_text.decode("utf-16")
    print(bn_file_text)
    bn_text_list = bn_file_text.split(' ')
    temp_bn_text = ''
    en_text = ''
    for word in bn_text_list:
        if len(temp_bn_text)+len(word)+len(' ')<480:
            temp_bn_text += (word + ' ')
        else:
            print(temp_bn_text)
            translation = translator.translate(temp_bn_text)
            print(translation)
            en_file.write(translation)
            en_file.write(' ')
            en_text += translation
            temp_bn_text = ''
    en_file.close()
    break
