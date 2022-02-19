import os, shutil




def load_configuration(obj):
    # cttrpg.conf file
    if not 'deck.conf' in os.listdir(obj.DECKROOT) :
        if obj.YNquestion('No configuration file found. Copy the default configuration ?', default=True) :
            shutil.copy('DefaultConfiguration/deck.conf', obj.DECKROOT+'/deck.conf')
        else :
            with open(path, 'w') as file :
                file.write("#Configuration file for cttrpg\n")
                file.write("#Can be edited directly or in the cttrpg program\n")
                file.write("#Categories\n|\n#Tags\n|\n")

    with open(obj.DECKROOT+'/deck.conf', 'r') as file :
        obj.CATEGORIES = []
        obj.TAGS = {}
        obj.COLORS = []
        skips = 0
        for line in file.readlines() :
            line = line.rstrip('\n')
            if line == '|' :
                skips += 1
            elif line != '' and line[0] != '#':
                if skips == 1:
                    obj.CATEGORIES.append(line)
                elif skips == 2:
                    obj.TAGS[line.split(':')[0]] = int(line.split(':')[1])
                elif skips == 3:
                    obj.COLORS.append((int(line.split(',')[0]), int(line.split(',')[1])))

    # check for sanity of configuration
    for category in obj.CATEGORIES :
        if not category in os.listdir(obj.DECKROOT) :
            os.mkdir(obj.DECKROOT +'/'+ category)

    # names
    obj.NAMES = []
    obj.NAMES_lower = []
    for cat in obj.CATEGORIES :
        for name in os.listdir(obj.DECKROOT+'/'+cat) :
            obj.NAMES.append(name[:-4])
            obj.NAMES_lower.append(name[:-4].lower())

def save_configuration(obj):
    out = '#Configuration file for cttrpg\n#can be edited here or in the cttrpg program\n\n'
    out += '#Categories\n|\n'
    for category in obj.CATEGORIES :
        out += category + '\n'

    out += '\n#Tags\n|\n'
    for tag,colorpair in obj.TAGS.items() :
        out += tag+':'+str(colorpair) + '\n'

    out += '\n#Colors (background,text)\n|\n'
    for color in obj.COLORS :
        out += str(color[0])+','+str(color[1]) + '\n'

    with open(obj.DECKROOT+'/deck.conf', 'w') as file :
        file.write(out)

def copy_default_configuration():
    #TODO:copy_default_configuration
    pass

def copy_sample_deck():
    #TODO: copy_sample_deck
    pass
