import urllib.parse
#import traceback
import json
import urlDownloader

__persistent__ = {}
__version__ = "1.0.0"
__definition__ = {
    "command": "crat",
    "name": "crat",
    "method": "get",
    "do": "cratworker",
    "child" : [
        {
            "command": "login",
            "name": "Login",
            "method": "get",
            "url": "home/",
            "data": [
                {
                    "name": "username",
                    "show": "Usuario: ",
                    "type": "text"
                },{
                    "name": "password",
                    "show": "Contrasena: ",
                    "type": "pass"
                }
            ],
            "down": "doLogin"
        },{
            "command": "autologin",
            "name": "Auto Login",
            "method": "get",
            "url": "usuarios/info.php",
            "down": "doAutoLogin"
        },{
            "command": "mytickets",
            "name": "Tickets Propios",
            "url": "tareas/",
            "get": {
                "event": "list",
                "idusuario": 0,
                "tareas_order_by": "prioridad DESC",
                "estado": -1
            },
            "down": "doList"
        },{
            "command": "tareas",
            "name": "Tareas",
            "url": "tareas/",
            "child": [
                {
                    "command": "set",
                    "name": "Asignar",
                    "down": "doSet",
                    "child":[
                        {
                            "command": "unworking",
                            "get": {
                                "event": "tarea_unworking"
                            }
                        },{
                            "command": "working",
                            "get": {
                                "event": "tarea_working"
                            }
                        }
                    ],
                    "data": [{
                        "name": "tareas_id",
                        "show": "Id tarea: ",
                        "type": "text"
                    }],
                },{
                    "command": "info",
                    "name": "Informacion",
                    "data": [{
                        "name": "id",
                        "show": "Id tarea: ",
                        "type": "text"
                    }],
                    "get": {
                        "event": "edit",
                        "info": '1'
                    },
                    "down": "doInfo"
                },{
                    "command": "list",
                    "down": "doList",
                    "name": "Listar",
                    "get": {
                            "event": "list",
                            "idusuario": 0,
                            "tareas_order_by": "prioridad DESC"
                    },
                    "child": [
                        {
                            "name": "Creadas",
                            "command": "myown",
                            "get": {
                                "idusuario_create": 0
                            }
                        },{
                            "name": "Asignadas",
                            "command": "myassign"
                        }
                    ]
                }
            ]
        }
    ]
}


def run(data, extra, args, struct, config, self):
    #print(data, extra, args, struct)
    if not 'twsd' in __persistent__:
        __persistent__['twsd'] = twsDownloader()
    if not 'down' in __persistent__:
        __persistent__['down'] = {
            'doLogin': doLogin,
            'doAutoLogin': doAutoLogin,
            'doList': doList,
            'doSet': doSet,
            'doInfo': doInfo
        }

    post = None
    if 'post' in struct:
        if data and'method' in struct and struct['method'].lower() == 'post':
            post = self.extend(struct['post'], data)
        else:
            post = self.extend(struct['post'])
    elif data and'method' in struct and struct['method'].lower() == 'post':
            post = data

    get = None
    if 'get' in struct:
        if data and (not ('method' in struct)) or ( 'method' in struct and struct['method'].lower() == 'get'):
            get = self.extend(struct['get'], data)
        else:
            get = self.extend(struct['get'])
    elif data and (not ('method' in struct)) or ( 'method' in struct and struct['method'].lower() == 'get'):
        get = data

    html = __persistent__['twsd'].downloadPage(struct['url'], get=get, post=post)

    if 'down' in struct and struct['down'] in __persistent__['down']:
        __persistent__['down'][struct['down']](html, data, struct)
    else:
        print(html)
    return 0


class twsDownloader(urlDownloader.UrlDownloader):
    BASE_URL = 'http://crat.3way.com.ar/'

    def downloadPage(self, method, get=None, post=None, extendMethod=True):
        if extendMethod:
            page = urllib.parse.urljoin(self.BASE_URL, method)
        if get:
            if not (type(get) is str):
                get = urllib.parse.urlencode(get)
            page = "%s?%s" % (page, get)

        if post and (not (type(post) is str)):
            post = urllib.parse.urlencode(post)

        html = urlDownloader.UrlDownloader.downloadPage(self, page, post)

        try:
            html = json.loads(html)
        except:
            #traceback.print_exc()
            pass
        return html

def doInfo(html, data, struct):
    #print('type', type(html['edit']['tarea']))
    #print('html', html)
    print("Nombre: %s" % html['edit']['tarea']['nombre'])
    print("\tProyecto: %s" % html['edit']['tarea']['proyecto']['nombre'])
    print("\tCliente: %s" % html['edit']['tarea']['cliente']['nombre'])
    print("\tCreador: %s" % html['edit']['tarea']['usuario_create']['username'])
    print("\tEstado: %s" % html['edit']['tarea']['estado_nice'])
    print("\tPrioridad: %s" % html['edit']['tarea']['prioridad_nice'])
    print("\tTiempo: %s" % html['edit']['tarea']['tiempo_nice'])
    print("\n-- Descripcion --")
    print(html['edit']['tarea']['descripcion_nice'])
    print("\n-- Log --")
    for log in html['tareas_log']:
        print(log['comentario'])


def doSet(html, data, struct):
    for key, item in html.items():
        err = "[Ok]" if(item == 0)else '[Error]'
        print("%s %s" % (key, err))

def doAutoLogin(html, data, struct):
    id = int(html[16:-1])
    if id:
        __persistent__['cratId'] = id;
        print("[Done]")
    else:
        print('[Fail]')

def doLogin(html, data, struct):
    if html.find(data['username']) >=0:
        doAutoLogin(__persistent__['twsd'].downloadPage("usuarios/info.php"), 0, 0)
    else:
        print('[Fail]')

def doList(html, data, struct):
    #print('type', type(html))
    print(
        (" ").center(3), '|',
        ("Id").center(5), '|',
        "Prioridad".center(10), '|',
        "Desc / Cliente".center(40), '|',
        "Nombre"
    )
    for tarea in html['list']['tareas']:
        dat = tarea['proyecto']['nombre'] if(len(tarea['proyecto']['nombre']) > 0)else tarea['cliente']['nombre']
        working = "*" if(int(tarea['estado']) == 2 and int(tarea['idusuario']) == __persistent__['cratId'])else ' '
        print(
            (working).center(3),'|',
            ("#%s" % tarea['id']).center(5),'|',
            tarea['prioridad_nice'].center(10),'|',
            dat[:40].center(40),'|',
            tarea['nombre']
        )
