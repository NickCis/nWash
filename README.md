nWash

TODO: Description, readme, and examples.

The code can be read in order to understand.
In short, there is a dictionary in which the commands are added, this commands are python fuctions.
The shell provide an interactive way in which to run this commands.
A plugin system is implemented. Look into the plugin folder.



Basic structure of folders:
    ./
    	./plugins/
    		./__init__.py
    		./*plugins*
    	./nWash.py

Other files are optional.


    class nWash(builtins.object)
         |
         |  Methods defined here:
         |
         |  __init__(self)
         |
         |  command(self)
         |
         |  completionDo(self, text, state)
         |
         |  completionInit(self)
         |      Inicialices the autocompletion
         |
         |  completionQuit(self)
         |
         |  extend(self, old, new=None)
         |      Creates a copy of dict old and extends it with new.
         |
         |  extendList(self, old, new=None)
         |      Creates a copy of list old and extends it with new
         |
         |  getOptions(self, args, text)
         |
         |  loadAllPluginsDefinitions(self)
         |      Load all plugins definitions in the plugin folder
         |
         |  loadConfig(self, config, erase=True)
         |      Load Configuration list. No check is done.
         |
         |  loadPluginDefinition(self, plugin)
         |      Load a plugin
         |
         |  loadPluginsDefinitions(self, plugins)
         |      Load a list of plugins
         |
         |  loadRc(self, path='./nWashrc')
         |      Load configuration file, a file which has valid nWash command lines
         |
         |  parseArgs(self, args)
         |      Parse line in args
         |
         |  registerCallback(self, name, func)
         |      Register callbacks -> do function of the config file
         |
         |  registerCallbacks(self, config)
         |      Register many callbacks
         |
         |  runCommand(self, *argscpy)
         |      Run a command already parsed
         |
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |
         |  COMMAND_LINE = '=> '
         |
         |  DESCRIPTION = ' Bienvenido a nWash sistema de shell'

Config List (see \_\_definition\_\_ in plugin files):
     *  Config Reserved words:
     *  command -> the command keyword
     *  child -> the command childs
     *  data -> the command args
     *  do -> the function to call
     *  desc -> Command description (it is used to print in help)

Example: 

    if __name__ == '__main__':
        def pepe(*args):
            print('Soy pepe', args)
    
        def pepeA(*args):
            print('Soy A', args)
    
        def cerrar(*args):
            return -1
    
        #Create nWash instance
        nw = nWash()
        #Register some callbacks
        nw.registerCallback('pepe', pepe)
        nw.registerCallback('pepeA', pepeA)
        nw.registerCallback('cerrar', cerrar)
        #Load a config structure
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
        #Load all plugins from plugin files. (Config structures of each plugin are
        #merged to the loaded one.
        nw.loadAllPluginsDefinitions();
        try:
            nw.completionInit()
        except:
            print("Autocompletado no soportado")
        while not nw.command():
            pass

Example of use of the twitter plugin (./plugins/twit.py):
    [cisco@cisco nWash]$ ./nWash.py 
    => twit 
    search   user     
    => twit user nickcis
    [ Sun Dec 16 21:31:52 +0000 2012 ] Nicolas Cisco -> @MechidelPozo y ahora qe los pagas vos, como no bancarlos =D,, jajajaja
    [ Sun Dec 16 17:57:58 +0000 2012 ] Nicolas Cisco -> @SofiChiofalo hay programas para el celu qe te la reconocen, gila!,, indaga,, jajaja
    [ Sat Dec 15 09:38:23 +0000 2012 ] Nicolas Cisco -> @MechidelPozo amiga, ya te dije qe no agradescas!,,solo q algun dia me dspidas cn una sonrisa,,(bue una merienda nunca viene mal),tmb te amo
    [ Thu Dec 06 16:57:50 +0000 2012 ] Nicolas Cisco -> @MechidelPozo Y si, a diferencia de una amiga mia que siempre qe me viene a ver me trae una cagada a pedos por llegar tarde,, jaja
    => twit search nickcis
    [ Thu, 20 Dec 2012 14:22:47 +0000 ] nickcis -> RT @Min_Ciencia: "Becas de hasta $50 mil para estudiantes avanzados de carreras TIC" http://t.co/2xtqEs2X
    [ Thu, 20 Dec 2012 00:32:52 +0000 ] MechidelPozo -> Alto chispasooooo en casa gracias a dios que estas conmigo @nickcis
    [ Tue, 18 Dec 2012 20:02:26 +0000 ] nickcis -> RT @nico_dato: Acabo de enterarme que en las direcciones de @gmail los puntos no cuentan.... homerjsimpson@gmail.com = homer.....j...sim.....pson@gmail.com
    [ Sun, 16 Dec 2012 21:31:52 +0000 ] nickcis -> @MechidelPozo y ahora qe los pagas vos, como no bancarlos =D,, jajajaja
    => 

