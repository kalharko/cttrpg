import curses, os, shutil, locale, random
from curses.textpad import Textbox, rectangle
from datetime import datetime

import data
from Card import Card


class CursesApp() :
    def __init__(self, stdscr):
        # encoding
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.code = locale.getpreferredencoding()
        curses.curs_set(0)

        # constants
        self.ESCAPE = ['quit', 'exit', 'q']

        self.screen = stdscr
        self.screenH, self.screenW = self.screen.getmaxyx()

        self.pad = curses.newpad(self.screenH, self.screenW//3)
        self.padH, self.padW = self.pad.getmaxyx()
        self.screen.refresh()

        self.mainwin = curses.newwin(self.screenH-2, self.screenW-self.padW)
        self.bottomwin = curses.newwin(1, self.screenW-self.padW, self.screenH-1, 0)
        self.messagewin = curses.newwin(1, self.screenW-self.padW, self.screenH-1-1, 0)

        self.messagewin.hline(0,0, curses.ACS_HLINE ,self.screenW-self.padW)
        self.messagewin.refresh()

        curses.init_pair(1, 0,255)
        if not self.deck_selection() : return
        self.CURRENT = Card(self.DECKROOT)

        self.updatePad()
        self.clear_logs()
        data.load_configuration(self)
        self.set_colorpairs()
        self.mainLoop()

    def mainLoop(self):
        self.commands = {
            'open':self.open,
            'close':self.close,
            'new':self.new,
            'delete':self.delete,
            'debug':self.debug,
            'colors':self.colordisplay,
            'refresh':self.refresh_all,
            'add':self.add,
            'remove':self.remove,
            'list':self.list,
            'tag':self.add_tag,
            'note':self.add_note,
            'edit':self.edit,
            'reload':self.reload,
            'show':self.show,
            'roll':self.roll,

            'ls':self.list,
            'rm':self.remove,
            'del':self.delete,
            'sh':self.show,

            'quit':self.quit,
            'q':self.quit,
            'exit':self.quit
        }

        y = 1
        self.loop = True
        while self.loop :
            self.screen.refresh()
            #user_input = self.box.edit(enter_is_terminate)[:-1]
            user_input = self.bottom_input()
            if user_input.split(' ')[0] in self.commands.keys():
                self.commands[user_input.split(' ')[0]](user_input[len(user_input.split(' ')[0])+1:])
            else :
                self.open(user_input)


    ################
    # Commands

    def open(self, args=None):
        self.CURRENT.save()

        if args.lower() in self.NAMES_lower :
            name = self.NAMES[self.NAMES_lower.index(args.lower())]
            self.log(name)
            for cat in self.CATEGORIES :
                if name+'.txt' in os.listdir(self.DECKROOT+'/'+cat) :
                    category = cat
                    break
            self.CURRENT.set_as_new()
            self.CURRENT.open(self.DECKROOT +'/'+ category+'/'+name)

        self.updatePad()

    def close(self, args=None):
        if args != 'nosave' :
            self.CURRENT.save()
        self.CURRENT.set_as_new()
        self.updatePad()

    def new(self, args=None):
        if args == '' :
            args = self.bottom_input('New what ?  [card | tag | category | color]')

        if args == 'card' :
            self.new_card()
        elif args == 'tag' :
            self.new_tag()
        elif args == 'category' or args == 'cat':
            self.new_category()
        elif args == 'color' :
            self.new_color()
        else :
            return

    def delete(self, args=None):
        if args == '' :
            args = self.bottom_input('Delete what ?  [card|tag|category|color]')

        pass_on_args = args[len(args.split(' ')[0])+1:]
        args = args.split(' ')[0]

        if args == 'card' :
            self.delete_card()
        elif args == 'tag' :
            self.delete_tag()
        elif args == 'category' or args == 'cat':
            self.delete_category()
        elif args == 'color':
            self.delete_color(pass_on_args)
        else :
            return

    def add(self, args=None):
        if self.CURRENT.name == '' or self.CURRENT.name == None:
            self.message('A card needs to be opened first')
            return
        if args == '' :
            args = self.bottom_input('Add what ?  [note | tag]')

        if args.split(' ')[0] == 'tag' :
            self.add_tag()
        elif args.split(' ')[0] == 'note' :
            self.add_note()
        else :
            return

    def remove(self, args=None):
        if self.CURRENT.name == '' or self.CURRENT.name == None:
            return
        if args == '' :
            args = self.bottom_input('Remove what ?  [note | tag]')
            if args in self.ESCAPE : return

        pass_on_args = args[len(args.split(' ')[0])+1:]
        args = args.split(' ')[0]

        if args.split(' ')[0] == 'tag' :
            self.remove_tag(pass_on_args)
        elif args.split(' ')[0] == 'note' :
            self.remove_note(pass_on_args)
        else :
            return
        self.CURRENT.save()
        self.updatePad()

    def list(self, args=None):
        if args in ['', 'category', 'cat']:
            self.list_categories()
        elif args == 'tag':
            self.list_tags()
        else :
            return

    def quit(self, args=None):
        if args != 'nosave' :
            self.CURRENT.save()
        data.save_configuration(self)
        self.loop = False

    def edit(self, args=None):
        self.CURRENT.save()

        if args == '' :
            args = self.bottom_input('Edit what ?  [name|subtitle|description|tag]')
            if args in self.ESCAPE : return

        pass_on_args = args[len(args.split(' ')[0])+1:]
        args = args.split(' ')[0]


        if ((self.CURRENT.name == '' or self.CURRENT.name == None)
            and args in ['name', 'subtitle', 'sub', 'description', 'desc']):
            self.message("A card need to be opened to edit it's " + args )
            return

        if args == 'name' :
            newname = self.main_input(self.CURRENT.name).split('\n')[0]
            os.remove(self.DECKROOT+'/'+self.CURRENT.category+'/'+self.CURRENT.name+'.txt')
            self.NAMES.remove(self.CURRENT.name)
            self.NAMES_lower.remove(self.CURRENT.name.lower())
            self.NAMES.append(newname)
            self.NAMES_lower.append(newname.lower())
            self.CURRENT.name = newname
            self.CURRENT.save()
        elif args in ['subtitle', 'sub']:
            self.CURRENT.subtitle = self.main_input(self.CURRENT.subtitle).split('\n')[0]
        elif args in ['description', 'desc'] :
            self.CURRENT.description = self.main_input(self.CURRENT.description)
        elif args == 'tag' :
            user_input = pass_on_args.split(' ')[0]
            pass_on_args = pass_on_args[len(pass_on_args.split(' ')[0])+1:]
            if user_input == '' :
                user_input = self.bottom_input('Edit what from tag ? [name|color|both]')
                if user_input in self.ESCAPE : return
            if user_input == 'name' :
                self.edit_tag_name(pass_on_args)
            elif user_input == 'color' :
                self.edit_tag_color(pass_on_args)
            elif user_input == 'both' :
                self.edit_tag_name(pass_on_args)
                self.edit_tag_color(pass_on_args)

        else :
            return

        self.CURRENT.reload()
        self.updatePad()

    def reload(self, args=None):
        data.load_configuration(self)
        self.set_colorpairs()
        self.refresh_all()

    def show(self, args=None):
        if args == '':
            args = self.bottom_input('Show what ?  [tag_name|category_name]')
            if args in self.ESCAPE : return

        if args in self.CATEGORIES :
            self.mainwin.erase()
            self.mainwin.addstr(1,1, args.upper(), curses.A_BOLD)
            y = 3
            for card in os.listdir(self.DECKROOT+'/'+args) :
                self.mainwin.addstr(y, 3, card[:-4])
                y += 2
            self.mainwin.refresh()

        elif args in self.TAGS :
            self.mainwin.erase()
            self.mainwin.addstr(1,1, args.upper(), curses.A_BOLD)
            y = 3
            current = Card(self.DECKROOT)
            for category in self.CATEGORIES :
                for card in os.listdir(self.DECKROOT+'/'+category) :
                    current.open(self.DECKROOT+'/'+category+'/'+card)
                    if args in current.tags :
                        self.mainwin.addstr(y, 3, current.name)
                        y += 2
            self.mainwin.refresh()

        else :
            return

    def roll(self, args=None):
        if args == '':
            args = self.bottom_input('Roll what ?  x d y + z, xyz integers')
            if args in self.ESCAPE : return

        x = args.split('d')[0]
        y = args.split('d')[1].split('+')[0]
        if '+' in args :
            z = args.split('+')[-1]

        try :
            x = int(x)
            y = int(y)
            if '+' in args :
                z = int(z)
        except :
            self.message('Invalid Input')
            return

        rolls = [random.randrange(1,y+1) for i in range(x)]
        message = 'Result : ' + str(rolls)
        if '+' in args :
            message += '+' + str(z)
        message +=' = '
        if '+' in args :
            message += str(sum(rolls)+z)
        else :
            message += str(sum(rolls))

        self.message(message)




    ####################
    # Dialogs


    def list_categories(self):
        self.mainwin.erase()
        y = 0
        for category in self.CATEGORIES :
            y += 1
            self.mainwin.addstr(y, 0, category.upper(), curses.A_BOLD)
            y += 1
            for line in os.listdir(self.DECKROOT+'/'+category) :
                self.mainwin.addstr(y, 2, line[:-4])
                y += 1
        self.mainwin.refresh()

    def list_tags(self):
        self.mainwin.erase()
        index = {}
        for tag in self.TAGS :
            index[tag] = []

        current = Card(self.DECKROOT)
        for category in self.CATEGORIES :
            for card in os.listdir(self.DECKROOT+'/'+category) :
                current.open(self.DECKROOT+'/'+category+'/'+card)
                for tag in current.tags:
                    index[tag].append(current.name)

        y = 0
        x = 0
        maxlen = 5
        for tag in index.keys() :
            if y + len(index[tag])+2 > self.screenH-2 :
                y = 0
                x = maxlen + 3
                maxlen = 0

            y += 1
            self.mainwin.addstr(y, x, tag, curses.A_BOLD | curses.color_pair(self.TAGS[tag]))
            if len(tag) > maxlen : maxlen = len(tag)
            y += 1
            for name in index[tag] :
                self.mainwin.addstr(y, x + 2, name)
                y += 1
                if len(name)+2 > maxlen : maxlen = len(name)+2

        self.mainwin.refresh()

    def deck_selection(self):
        self.mainwin.erase()
        self.mainwin.addstr(2,1, '0  New')
        for i,line in enumerate(os.listdir('data')) :
            self.mainwin.addstr(4+i*2,1, f'{i+1}  ' + line)
        self.mainwin.refresh()

        user_input = self.bottom_input('Chose which deck to open')
        if user_input in self.ESCAPE : return False
        try:
            user_input = int(user_input)
        except:
            self.message('Invalid Input, action canceled')
        if user_input < 0 or user_input > len(os.listdir('data')):
            self.message('Invalid Input, action canceled')

        if user_input == 0 :
            user_input = self.bottom_input('Chose a name for a new deck')
            if not user_input in os.listdir('data') :
                self.DECKROOT = 'data/'+user_input
                os.mkdir(self.DECKROOT)
                shutil.copy('DefaultConfiguration/deck.conf', self.DECKROOT+'/deck.conf')
        else :
            self.DECKROOT = 'data/'+os.listdir('data')[user_input-1]

        self.mainwin.erase()
        self.mainwin.refresh()
        return True

    def new_card(self):
        self.CURRENT.save()
        self.CURRENT.set_as_new()
        self.updatePad()
        # category
        user_input = self.bottom_input('Category')
        if user_input in self.ESCAPE : return
        if not user_input in self.CATEGORIES :
            if self.YNquestion(f'Créer nouvelle categorie "{user_input}" ?', default=True) :
                os.mkdir(self.DECKROOT +'/'+ user_input)
                self.CATEGORIES.append(user_input)
                self.CURRENT.category = user_input
            else : return
        else :
            self.CURRENT.category = user_input
        self.updatePad()
        # name
        user_input = self.bottom_input('Name')
        if user_input in self.ESCAPE : return
        if not user_input in self.NAMES and not user_input.lower() in self.NAMES_lower:
            self.CURRENT.name = user_input
        self.updatePad()
        # subtitle
        user_input = self.bottom_input('Subtitle')
        if user_input in self.ESCAPE : return
        self.CURRENT.subtitle = user_input
        self.updatePad()
        # tags
        user_input = self.bottom_input('Tags    ("next" to skip)')
        if user_input in self.ESCAPE : return
        while user_input != 'next' :
            if not user_input in self.TAGS.keys() :
                if self.YNquestion(f'Créer nouveau tag "{user_input}" ?', default=True) :
                    self.TAGS[user_input] = 0
                    self.CURRENT.tags.append(user_input)
            else :
                self.CURRENT.tags.append(user_input)
            self.updatePad()
            user_input = self.bottom_input('Tags    ("next" to skip)')
            if user_input in self.ESCAPE : return
        # description
        self.CURRENT.description = self.main_input('')
        self.updatePad()

    def new_tag(self):
        user_input = self.bottom_input('New tag name')
        if user_input in self.ESCAPE : return
        if user_input in self.TAGS.keys() :
            self.message('Tag "'+user_input+'" already exists')
            return
        newtag = user_input

        self.colordisplay()
        user_input = self.bottom_input('Chose an available color pair')
        if user_input in self.ESCAPE : return
        try :
            user_input = int(user_input)
        except :
            self.mainwin.clear()
            self.mainwin.refresh()
            self.message('Invalid input')
            return

        self.TAGS[newtag] = user_input

    def new_category(self):
        user_input = self.bottom_input('New category name')
        if user_input in self.ESCAPE : return
        if user_input in self.CATEGORIES :
            self.message('Category "'+user_input+'" already exists')
            return
        os.mkdir(self.DECKROOT+'/'+user_input)
        self.CATEGORIES.append(user_input)

    def new_color(self):
        self.mainwin.clear()

        for i in range(255):
            if i in [0, 16, 17, 52, 232, 233, 234, 235] :
                curses.init_pair(i+1, 255, i+1)
            else :
                curses.init_pair(i+1, 0, i+1)
        i = 1
        for y in range(17):
            for x in range(15):
                for suby in range(1):
                    self.mainwin.addstr(y*2, x*6, '.'+str(i)+('.'*(4-len(str(i)))), curses.color_pair(i-1))
                i += 1
        self.mainwin.refresh()

        user_input = self.bottom_input('Select a pair of color, separated by a comma : text,background')
        if not ',' in user_input or user_input in self.ESCAPE:
            self.mainwin.erase()
            self.mainwin.refresh()
            self.message('Invalid input')
            return

        try :
            c1 = int(user_input.split(',')[0])
            c2 = int(user_input.split(',')[1])
        except :
            self.mainwin.erase()
            self.mainwin.refresh()
            self.message('Invalid input')
            return

        self.COLORS.append((c1-1,c2-1))
        self.set_colorpairs()

    def delete_card(self):
        user_input = self.bottom_input('Name of card to delete [Case sensitive]')
        if user_input in self.ESCAPE : return
        if not user_input in self.NAMES :
            self.message('Card "'+user_input+'" not found')
            return

        for category in self.CATEGORIES :
            if user_input in os.listdir(self.DECKROOT+'/'+category) :
                break
        os.remove(self.DECKROOT+'/'+category+'/'+user_input+'.txt')
        self.NAMES.remove(user_input)
        self.NAMES_lower.remove(user_input.lower())

    def delete_tag(self):
        user_input = self.bottom_input('Name of tag to delete')
        if user_input in self.ESCAPE : return
        if not user_input in self.TAGS.keys() :
            self.message('Tag "'+user_input+'" not found')
            return

        current = Card(self.DECKROOT)
        for category in self.CATEGORIES :
            for card in os.listdir(self.DECKROOT+'/'+category) :
                current.open(self.DECKROOT+'/'+category+'/'+card)
                if user_input in current.tags :
                    current.tags.remove(user_input)
                    current.save()

        self.TAGS.pop(user_input)

    def delete_category(self):
        user_input = self.bottom_input('Name of category to delete')
        if user_input in self.ESCAPE : return
        if not user_input in self.CATEGORIES :
            self.message('Category "'+user_input+'" not found')
            return

        # TODO: show(category:user_input)
        if self.YNquestion('Are you sure about deleting this category ?', default=False) :
            shutil.rmtree(self.DECKROOT+'/'+user_input)
            self.CATEGORIES.remove(user_input)

    def delete_color(self, args):
        if args == '' :
            self.colordisplay()
            args = self.bottom_input('Select one color to delete')

        try:
            args = int(args)
        except:
            self.message(f'Input not recognised "{args}"')
            return

        del self.COLORS[args-1]

        for tag in self.TAGS.keys() :
            if self.TAGS[tag] == args :
                self.TAGS[tag] = 1
            elif self.TAGS[tag] > args :
                self.TAGS[tag] -= 1

        self.set_colorpairs()
        self.colordisplay()

    def edit_tag_name(self, args):
        tag2edit = args.split(' ')[0]
        newname = args[len(args.split(' ')[0])+1:].split(' ')[0]

        if tag2edit == '':
            tagkeys = list(self.TAGS.keys())
            tag2edit = self.list_choice(tagkeys, 'Chose a tag to edit the name')
            if user_input == None : return
            tag2edit = tagkeys[tag2edit]

        if newname == '':
            newname = self.bottom_input('Chose a new name for tag "'+tag2edit+'"')
            if newname in self.ESCAPE : return

        current = Card(self.DECKROOT)
        for category in self.CATEGORIES :
            for card in os.listdir(self.DECKROOT+'/'+category) :
                self.log(card)
                current.open(self.DECKROOT+'/'+category+'/'+card)
                if tag2edit in current.tags :
                    current.tags.remove(tag2edit)
                    current.tags.append(newname)
                    self.log(str(current.tags))
                current.save()

        self.TAGS[newname] = self.TAGS[tag2edit]
        del self.TAGS[tag2edit]

    def edit_tag_color(self, args):
        tag2edit = args.split(' ')[0]
        newcolor = args[len(args.split(' ')[0])+1:].split(' ')[0]
        try:
            newcolor = int(newcolor)
        except:
            newcolor = ''

        if tag2edit == '':
            tagkeys = list(self.TAGS.keys())
            tag2edit = self.list_choice(tagkeys, 'Chose a tag to edit the name')
            if user_input == None : return
            tag2edit = tagkeys[tag2edit]

        if newcolor == '':
            self.colordisplay()
            newcolor = self.bottom_input('Chose a new color for tag "'+tag2edit+'"')
            if newcolor in self.ESCAPE : return
            try :
                newcolor = int(newcolor)
            except :
                self.mainwin.clear()
                self.mainwin.refresh()
                self.message('Invalid input')
                return

        self.TAGS[tag2edit] = newcolor

    def add_note(self, args=''):
        if args == '' :
            args = self.bottom_input('Add Note')

        if args in self.ESCAPE : return
        self.CURRENT.notes.append(args)
        self.updatePad()

    def add_tag(self, args=''):
        if args == '' :
            args = self.bottom_input('Add tag(s)')

        for tag in args.split(' ') :
            if tag in self.ESCAPE : return
            if not tag in self.TAGS.keys() :
                if self.YNquestion(f'Créer nouveau tag "{tag}" ?', default=True) :
                    self.TAGS[tag] = 0
                    self.CURRENT.tags.append(tag)
            else :
                self.CURRENT.tags.append(tag)
        self.updatePad()

    def remove_note(self, args=''):
        try :
            args = int(args)
            if 0 < args and args <= len(self.CURRENT.notes) :
                del self.CURRENT.notes[args-1]
                return
        except :
            pass

        user_input = self.list_choice(self.CURRENT.notes, 'Chose a note to remove')
        if user_input == None : return

        del self.CURRENT.notes[user_input]

    def remove_tag(self, args=''):
        if args in self.CURRENT.tags :
            self.CURRENT.tags.remove(args)
            return

        user_input = self.list_choice(self.CURRENT.tags, 'Chose a tag to remove')
        if user_input == None : return

        del self.CURRENT.tags[user_input]


    ####################################
    # Display and miscelaneous functions

    def bottom_input(self, message=None):
        # message
        if message != None :
            self.messagewin.hline(0,0, curses.ACS_HLINE, self.screenW-self.padW)
            self.messagewin.addstr(0,0, message)
            self.messagewin.refresh()

        out = ''
        newchar = self.screen.get_wch()
        pos_cursor = 0
        while newchar != '\n' : #TODO: stop from inputing longer than window size
            if type(newchar) == int :
                if newchar == 263 : ## delete
                    if len(out) > 0 and pos_cursor > 0:
                        out = out[:pos_cursor-1] + out[pos_cursor:]
                        pos_cursor -= 1
                        self.bottomwin.erase()
                elif newchar == 260 : #left arrow
                    pos_cursor = pos_cursor - 1 if pos_cursor > 0 else 0
                    self.bottomwin.erase()
                elif newchar == 261 : #right arrow
                    pos_cursor = pos_cursor + 1 if pos_cursor < len(out) else pos_cursor
                elif newchar == 258 : # down arrow
                    pos_cursor = len(out)
                    self.bottomwin.erase()
                elif newchar == 259 : # up arrow
                    pos_cursor = 0
                    self.bottomwin.erase()
                else :
                    with open('log.txt', 'a') as file :
                        file.write(str(type(newchar)) + '     ' + str(newchar) + '\n')
            else :
                out = out[:pos_cursor] + newchar + out[pos_cursor:]
                pos_cursor += 1

            self.bottomwin.addstr(0, 0, out[:pos_cursor])
            if pos_cursor == len(out) :
                self.bottomwin.addch(0,pos_cursor, ' ', curses.color_pair(1))
            else :
                self.bottomwin.addch(0, pos_cursor, out[pos_cursor], curses.color_pair(1))
            self.bottomwin.addstr(0, pos_cursor+1, out[pos_cursor+1:])
            self.bottomwin.refresh()
            newchar = self.screen.get_wch()

        self.bottomwin.clear()
        self.bottomwin.refresh()
        self.messagewin.hline(0,0, curses.ACS_HLINE, self.screenW-self.padW)
        self.messagewin.refresh()
        return out

    def YNquestion(self, message, default=True):
        added = '  (Y/n)' if default else '  (y/N)'
        self.message(message+added)

        answer = self.screen.get_wch()
        self.messagewin.hline(0,0, curses.ACS_HLINE, self.screenW-self.padW)
        self.messagewin.refresh()
        if answer in ['Y','y'] :
            return True
        elif answer in ['N', 'n'] :
            return False
        else :
            return default

    def message(self, message):
        self.messagewin.hline(0,len(message), curses.ACS_HLINE, self.screenW-self.padW)
        self.messagewin.addstr(0,0, message)
        self.messagewin.addch(0,len(message), curses.ACS_LTEE)
        self.messagewin.refresh()

    def main_input(self, og_content):
        self.mainwin.erase()
        self.mainwin.hline(0,0, curses.ACS_HLINE, self.screenW-self.padW)
        self.mainwin.vline(0,0, curses.ACS_VLINE, 20)
        self.mainwin.vline(0,self.screenW-self.padW-1 , curses.ACS_VLINE, 20)
        self.mainwin.addch(0,0, curses.ACS_ULCORNER)
        self.mainwin.addch(0,self.screenW-self.padW-1, curses.ACS_URCORNER)

        lines = og_content.split('\n')
        y = len(lines)-1  #cursor at end of last line
        x = len(lines[-1])
        for i,line in enumerate(lines) :
            if i != y :
                self.mainwin.addstr(i+1,1, line)
            else :
                self.mainwin.addstr(i+1,1, line[:x])
                self.mainwin.addch(i+1, x+1, ' ', curses.color_pair(1))
                self.mainwin.addstr(i+1, x+2, line[x:])
        self.mainwin.refresh()
        self.message('Type "~" to exit editing mode')

        newchar = self.screen.get_wch()
        while newchar != '~' :
            if type(newchar) == int :
                if newchar == 263 : ## delete
                    if len(lines[y]) > 0 and x > 0:
                        lines[y] = lines[y][:x-1] + lines[y][x:]
                        x -= 1
                    elif x == 0:
                        if len(lines[y]) + len(lines[y-1]) < self.mainwin.getmaxyx()[1] :
                            x = len(lines[y-1])
                            lines[y-1] += lines[y]
                            lines[y] = None
                            lines.remove(None)
                            y -= 1
                elif newchar == 260 : #left arrow
                    if x == 0 :
                        if y != 0 :
                            y -= 1
                            x = len(lines[y])
                    else :
                        x = x - 1 if x > 0 else 0
                elif newchar == 261 : #right arrow
                    if x == len(lines[y]) :
                        if y != len(lines)-1 :
                            x = 0
                            y += 1
                    else :
                        x = x + 1 if x < len(lines[y]) else x
                elif newchar == 259 : # up arrow
                    if y == 0 :
                        x = 0
                    else :
                        y = y - 1
                        x = x if x < len(lines[y]) else len(lines[y])
                elif newchar == 258 : #down arrow
                    if y == len(lines)-1 :
                        x = len(lines[y])
                    else :
                        y = y + 1
                        x = x if x < len(lines[y]) else len(lines[y])
                else :
                    with open('log.txt', 'a') as file :
                        file.write(str(type(newchar)) + '     ' + str(newchar) + '\n')
            else :
                if newchar == '\n' :
                    if x == len(lines[y]) :
                        lines.insert(y+1, '')
                        y += 1
                        x = 0
                    else :
                        lines.insert(y+1, lines[y][x:])
                        lines[y] = lines[y][:x]
                        y += 1
                        x = 0
                else :
                    lines[y] = lines[y][:x] + newchar + lines[y][x:]
                    x += 1

            self.mainwin.erase()
            self.mainwin.hline(0,0, curses.ACS_HLINE, self.screenW-self.padW)
            self.mainwin.vline(0,0, curses.ACS_VLINE, 20)
            self.mainwin.vline(0,self.screenW-self.padW-1 , curses.ACS_VLINE, 20)
            self.mainwin.addch(0,0, curses.ACS_ULCORNER)
            self.mainwin.addch(0,self.screenW-self.padW-1, curses.ACS_URCORNER)
            for i,line in enumerate(lines) :
                if i != y :
                    self.mainwin.addstr(i+1,1, line)
                else :
                    self.mainwin.addstr(i+1,1, line[:x])
                    if x == len(line) :
                        self.mainwin.addch(i+1,x+1, ' ', curses.color_pair(1))
                    else :
                        self.mainwin.addch(i+1, x+1, line[x], curses.color_pair(1))
                    self.mainwin.addstr(i+1, x+2, line[x+1:])
            self.mainwin.refresh()

            newchar = self.screen.get_wch()

        self.mainwin.erase()
        self.mainwin.refresh()
        self.message('')
        out = ''
        for line in lines :
            out += line + '\n'
        return out.lstrip('\n').rstrip('\n')

    def updatePad(self):
        self.pad.erase()
        self.pad.border()
        self.pad.addch(self.padH-2, 0, curses.ACS_RTEE) #right T connection with bottomwin

        if self.CURRENT.name == None:
            self.pad.refresh(0,0, 0,self.screenW-self.padW, self.screenH,self.screenW)
            return

        # Category
        self.pad.addstr(0,(self.padW-len(self.CURRENT.category))//2, self.CURRENT.category.upper())#, curses.color_pair(1))
        # Name
        self.pad.addstr(2, (self.padW-len(self.CURRENT.name))//2, self.CURRENT.name, curses.A_BOLD)
        # Subtitle
        self.pad.addstr(3, (self.padW-len(self.CURRENT.subtitle))//2, self.CURRENT.subtitle, curses.A_UNDERLINE)
        # Tags
        y = 5
        x = 1
        for i,tag in enumerate(self.CURRENT.tags) :
            self.pad.addstr(y, x, tag, curses.color_pair(self.TAGS[tag]))
            x += len(tag) + 1
            if x + len(self.CURRENT.tags[i]) > self.padW :
                x = 1
                y += 2
        y += 2
        # Description
        x = 1
        if self.CURRENT.description != '' :
            for line in self.CURRENT.description.split('\n') :
                for word in line.split(' '):
                    if x + len(word) >= self.padW :
                        x = 1
                        y += 1
                    self.pad.addstr(y, x, word)
                    x += len(word) + 1
                x = 1
                y += 1
        y += 2
        # Notes
        x = 1
        for line in self.CURRENT.notes :
            for i,word in enumerate(line.split(' ')) :
                self.pad.addstr(y, x, word)
                x += len(word) + 1
                if x + len(line[i]) > self.padW :
                    x = 1
                    y += 1
            y += 2
            x = 1

        self.pad.refresh(0,0, 0,self.screenW-self.padW, self.screenH,self.screenW)

    def debug(self, args=None):
        self.mainwin.clear()
        to_display = [
            "Categories: " + str(self.CATEGORIES),
            "Names:      " + str(self.NAMES),
            "Names_lower " + str(self.NAMES_lower),
            "Tags:       " + str(self.TAGS),
            "",
            "screenH,W:  " + str(self.screenH) + ", " + str(self.screenW),
            "padH,W:     " + str(self.padH) + ', ' + str(self.padW)
        ]

        x = 1
        y = 1
        for line in to_display :
            for word in line.split(' '):
                if x + len(word) >= self.screenW-self.padW :
                    x = 1
                    y += 1
                self.mainwin.addstr(y, x, word)
                x += len(word) + 1
            x = 1
            y += 1
        self.mainwin.refresh()

    def set_colorpairs(self):
        for i,pair in enumerate(self.COLORS) :
            curses.init_pair(i+1, pair[0], pair[1])

    def colordisplay(self, args=None):
        self.mainwin.clear()
        i = 1
        for y in range(8):
            for x in range(8):
                self.mainwin.addstr(y*5, x*5, ' '+str(i)+' ', curses.color_pair(i))
                i += 1
                if i > len(self.COLORS) :
                    self.mainwin.refresh()
                    return

    def refresh_all(self, args=None):
        self.set_colorpairs()
        self.screen.refresh()
        self.mainwin.refresh()
        self.messagewin.refresh()
        self.bottomwin.refresh()
        self.updatePad()

    def log(self, message):
        with open(self.DECKROOT+'/logs.txt', 'a') as file:
            file.write('['+ str(datetime.now()).split(' ')[1].split('.')[0] +'] '+ message+'\n')

    def clear_logs(self):
        with open(self.DECKROOT + '/logs.txt', 'w') as file:
            file.write('Logs cttrpg : ' + str(datetime.now()).split(' ')[0] + '\n')

    def list_choice(self, list, message):
        self.mainwin.erase()

        y = 2
        x = 2
        maxlen = 5
        i = 1
        for line in list :
            self.mainwin.addstr(y,x, str(i)+'. '+line)
            i += 1
            y += 1
            if len(line) + 3 > maxlen : maxlen = len(line)+3
            if y > self.screenH - 2 :
                y = 2
                x += maxlen+2
        self.mainwin.refresh()

        user_input = self.bottom_input(message)
        if user_input in self.ESCAPE :
            self.mainwin.erase()
            self.mainwin.refresh()
            return None
        if user_input in list :
            self.mainwin.erase()
            self.mainwin.refresh()
            return list.index(user_input)

        try :
            user_input = int(user_input)
        except :
            self.message('Input not recognised')
            self.mainwin.erase()
            self.mainwin.refresh()
            return None

        if user_input < 1 or user_input > len(list) :
            self.message('Input not recognised')
            self.mainwin.erase()
            self.mainwin.refresh()
            return None

        self.mainwin.erase()
        self.mainwin.refresh()
        return user_input - 1
