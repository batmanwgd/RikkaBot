from source import Source

class Insource(Source):
    def __init__(data_file):
       Source.__init__(data_file)

    def get_message(self):
        return ''
