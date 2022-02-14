import os


class Card():
    def __init__(self, deckroot):
        self.category = None
        self.name = None
        self.subtitle = None
        self.tags = []
        self.description = None
        self.notes = []
        self.images = []
        self.href = []
        self.deckroot = deckroot

    def set_all(self, category, name, sous_subtitle, tags, description, notes, images):
        self.category = category
        self.name = name
        self.subtitle = subtitle
        self.tags = tags
        self.description = description
        self.notes = notes
        self.images = images

    def set_as_new(self):
        self.category = 'new_card'
        self.name = ''
        self.subtitle = ''
        self.tags = []
        self.description = ''
        self.notes = []
        self.images = []
        self.href = []

    def save(self):
        if self.name in [None, '']:
            return False

        out = self.category + '\n|\n'
        out += self.name + '\n|\n'
        out += self.subtitle + '\n|\n'
        for tag in self.tags :
            out += tag +','
        out = out.rstrip(',')
        out += '\n|\n'
        out += self.description + '\n|\n'
        for note in self.notes :
            out += note + ','
        out = out.rstrip(',')
        out += '\n|\n'
        for image in self.images :
            out += image + ','
        out = out.rstrip(',')


        with open(self.getPath(), 'w') as file:
            file.write(out)
        return True



    def open(self, path):
        if len(path.split('.')) == 1 :
           path += '.txt'

        with open(path, 'r') as file :
            lines = file.read()
            file = []
            for line in lines.split('\n|\n') :
                file.append(line.rstrip('\n'))

            self.category = file[0]
            self.name = file[1]
            self.subtitle = file[2]
            self.tags = file[3].split(',')
            self.description = file[4]
            self.notes = file[5].split(',')
            self.images = file[6].split(',')

            for collection in [self.tags, self.notes, self.images]:
                if '' in collection : collection.remove('')


    def getPath(self):
        return self.deckroot +'/'+ self.category +'/'+ self.name + '.txt'

    def reload(self):
        path = self.getPath()
        self.set_as_new()
        self.open(path)



    def __str__(self):
        if self.name == None :
            return 'Empty card'
        else :
            out = self.category + '\n'
            out += self.name + '\n'
            out += self.subtitle + '\n'
            for tag in self.tags :
                out += tag +','
            out.rstrip(',')
            out += '\n'
            out += self.description + '\n'
            for note in self.notes :
                out += note + ','
            out.rstrip(',')
            out += '\n'
            for image in self.images :
                out += image + ','

            return out
