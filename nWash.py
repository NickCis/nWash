#! /usr/bin/python3

import shlex
import readline
import os
import os.path
import traceback
from getpass import getpass

import plugins

class nWash():
    '''Config Reserved words:
        command -> the command keyword
        child -> the command childs
        data -> the command args
        do -> the function to call
        desc -> Command description (it is used to print in help)'''

    COMMAND_LINE = '=> '
    DESCRIPTION = ''' Bienvenido a nWash sistema de shell'''
    def __init__(self):
        self.do = {}
        self.plugins = plugins.plugins
        self.com = {}
        self.config = []

    def registerCallbacks(self, config):
        '''Register many callbacks'''
        for key, val in config.items():
            self.registerCallback(key, val)

    def registerCallback(self, name, func):
        '''Register callbacks -> do function of the config file'''
        if name in self.do:
            return -1

        self.do[name] = func
        return 0

    def loadConfig(self, config, erase=True):
        '''Load Configuration list. No check is done.'''
        if not config:
            return
        if erase:
            self.config = []
            self.com = {}

        #self.config = self.extendList(self.config, config)
        #FIXME: it doesn't copy the dictionary
        #self.config = config
        self.config.extend(config)

        for i in range(0, len(config)):
            if 'command' in config[i]:
                self.com[config[i]['command']] = i

    def loadPluginDefinition(self, plugin):
        plugDef = plugins.getDefinition(plugin)
        if plugDef:
            self.loadConfig([plugDef], False)

    def loadPluginsDefinitions(self, plugins):
        for i in plugins:
            self.loadPluginDefinition(i)

    def loadAllPluginsDefinitions(self):
        self.loadPluginsDefinitions(plugins.plugins)

    def loadRc(self, path='./nWashrc'):
        with open(path) as rc:
            for line in rc.readlines():
                try:
                    self.runCommand(*self.parseArgs(line))
                except:
                    print("[Error] Con archivo rc '%s'" % path)
                    print("Linea: '%s'" % line)
                    traceback.print_exc()

    def extendList(self, old, new=None):
        '''Creates a copy of list old and extends it with new'''
        ret =[]
        for val in old:
            if type(val) == dict:
                ret.append(self.extend(val))
            elif type(val) in (tuple, list):
                ret.append(self.extendList(val))
            else:
                ret.append(val)
        if new:
            for val in new:
                if type(val) == dict:
                    ret.append(self.extend(val))
                elif type(val) in (tuple, list):
                    ret.append(self.extendList(val))
                else:
                    ret.append(val)

        return ret

    def extend(self, old, new=None):
        '''Creates a copy of dict old and extends it with new.'''
        ret = {}

        for key, item in old.items():
            if key == 'child':
                continue
            if type(old[key]) == dict:
                if type(new) == dict and key in new:
                    ret[key] = self.extend(old[key], new[key])
                else:
                    ret[key] = self.extend(old[key])
            elif type(old[key]) in (tuple, list):
                if type(new) == dict and key in new:
                    ret[key] = self.extendList(old[key], new[key])
                else:
                    ret[key] = self.extendList(old[key])
            else:
                ret[key] = new[key] if(new and key in new)else item

        if type(new) == dict:
            for key, item in new.items():
                if key == 'child':
                    continue
                if not (key in ret):
                    if type(item) == dict:
                        ret[key] = self.extend(item)
                    elif type(item) in (tuple, list):
                        ret[key] = self.extendList(item)
                    else:
                        ret[key] = item

        return ret

    def parseArgs(self, args):
        '''Parse line in args'''
        #return args.split(" ")
        return shlex.split(args)

    def runCommand(self, *argscpy):
        '''Run a command already parsed'''
        if not argscpy:
            return 0

        args = [x for x in argscpy]

        if args[0] in self.com:
            scope = self.config
            struct = {}

            noChild = False
            #noArg = False
            #while len(args) and not (noChild) and not (noArg):
            while len(args) and not (noChild):
                child = args.pop(0)
                for val in scope:
                    if 'command' in val and child == val['command']:
                        struct = self.extend(struct, val)
                        if 'child' in val:
                            scope = val['child']
                        else:
                            noChild = True

                        break

            #if noArg:
            #    print("[Error]: Argumento inexistente")
            #    return 0

            if(not noChild):
                print("[Error]: Faltan argumentos")
                #FIXME: hay que arreglar el manejo de errores
                #devuelve 0 para poder seguir loopeando
                return 0

            dataSend = None

            if 'data' in struct:
                dataAsk = {}
                dataSend = {}
                for item in struct['data']:
                    if 'type' in item and not ('text', 'path').count(item['type']):
                        if not item['type'] in dataAsk:
                            dataAsk[item['type']] = []
                        dataAsk[item['type']].append(item)
                        continue

                    if not len(args):
                        print('[Error] Argumentos Insuficientes')
                        #FIXME: hay que arreglar el manejo de errores
                        #devuelve 0 para poder seguir loopeando
                        return 0

                    dataSend[item['name']] = args.pop()

                for key, val in dataAsk.items():
                    for it in val:
                        if key == 'pass':
                            dataSend[it['name']] = getpass(it['show'])
                        else:
                            print("[Error] '%s' data type not implemented" % key)
                            return 0

            if 'do' in struct:
                funct = None
                if struct['do'] in self.do:
                    funct = self.do[struct['do']]
                elif struct['do'] in self.plugins:
                    funct = plugins.plugin(struct['do']).run

                if type(funct) != type(lambda x: x):
                    print("[Error] do '%s' isn't registered" % struct['do'])

                return funct(
                        dataSend, #Dicionario de data
                        args, #argumetnos extra
                        argscpy, #linea de llamada parseada
                        struct, #dict de informacion extendida pedida y obtenida
                        self.config, #configuracion
                        self #instancia
                    )
            else:
                print("[Error] do isn't defined")

        else:
            print("[Error]: '%s' Comando inexistente" % args[0])

        return 0


    def command(self):
        args = self.parseArgs(input(self.COMMAND_LINE))
        return self.runCommand(*args)

    def completionInit(self):
        '''Inicialices the autocompletion'''
        readline.set_completer(self.completionDo)
        readline.parse_and_bind("tab: complete")

    def getOptions(self, args, text):
        scope = self.config
        options = []
        child = True
        struct = {}
        while len(args) and  child:
            child = False
            options = []
            for it in scope:
                if 'command' in it:
                    if args[0] == it['command']:
                        struct = self.extend(struct, it)
                        args.pop(0)
                        if 'child' in it:
                            scope = it['child']
                            child = True
                        break
                    elif it['command'].startswith(args[0]):
                        options.append("%s " % it['command'])

        if child:
            options = []
            for it in scope:
                if 'command' in it:
                    options.append("%s " % it['command'])
        elif not options and (args or not text):
            options = []
            self.completionFile = True
            if not args or (os.path.basename(args[-1]) and not text):
                args.append(os.path.join(os.getcwd(), ''))

            if 'data' in struct and len(struct['data']) >= len(args) and 'type' in struct['data'][len(args)-1] and struct['data'][len(args)-1]['type'] == 'path':
                dir = os.path.dirname(args[-1]) or os.getcwd()
                base = os.path.basename(args[-1])
                for x in os.listdir(dir):
                    if x.startswith(base):
                        if os.path.isdir(os.path.join(dir, x)):
                            x = os.path.join(x, '')
                        else:
                            x = "%s " % x
                        options.append(x)

                #options = [x for x in os.listdir(dir) if x.startswith(base)]

        return options

    def completionDo(self, text, state):
        response = None

        if state == 0:
            options = self.getOptions(self.parseArgs(readline.get_line_buffer()), text)
            self.matches = self.getOptions(self.parseArgs(readline.get_line_buffer()), text)
            # This is the first time for this text, so build a match list.
            #if text:
            #    self.matches = [s
            #                    for s in options
            #                    if s and s.startswith(text)]
            #else:
            #    self.matches = options[:]
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


    def completionQuit(self):
        pass


if __name__ == '__main__':
    def pepe(*args):
        print('Soy pepe', args)

    def pepeA(*args):
        print('Soy A', args)

    def cerrar(*args):
        return -1

    nw = nWash()
    nw.registerCallback('pepe', pepe)
    nw.registerCallback('pepeA', pepeA)
    nw.registerCallback('cerrar', cerrar)
    nw.loadConfig([
        {
            'command': 'pepe',
            'do': 'pepe',
            'child' : [
                {
                    'command': 'a',
                    'do': 'pepeA'
                },
                {
                    'command': 'b'
                }
            ]
        },{
            'command': 'exit',
            'do': 'cerrar'
        }
    ])
    nw.loadAllPluginsDefinitions();
    try:
        nw.completionInit()
    except:
        print("Autocompletado no soportado")
    while not nw.command():
        pass
