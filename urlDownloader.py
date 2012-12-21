#! /usr/bin/python3

import urllib.parse
import urllib.request
import http.cookiejar

class UrlDownloader(urllib.request.OpenerDirector):
    def __init__(self, *args, **kargs):
        urllib.request.OpenerDirector.__init__(self, *args, **kargs)
        #agregando soporte basico
        self.add_handler(urllib.request.ProxyHandler())
        self.add_handler(urllib.request.UnknownHandler())
        self.add_handler(urllib.request.HTTPHandler())
        self.add_handler(urllib.request.HTTPSHandler())
        self.add_handler(urllib.request.HTTPDefaultErrorHandler())
        self.add_handler(urllib.request.HTTPRedirectHandler())
        self.add_handler(urllib.request.FTPHandler())
        self.add_handler(urllib.request.FileHandler())
        self.add_handler(urllib.request.HTTPErrorProcessor())

        #Agregar soporte para cookies. (en este momento no es necesario,
        #pero uno nunca sabe si se puede llegar a nececitar)
        self.cj = http.cookiejar.CookieJar()
        self.add_handler(urllib.request.HTTPCookieProcessor(self.cj))

    def downloadPage(self, link, data=None, timeout=None):
        '''Funcion para obtener el html de una pagina'''
        html = ''
        try:
            fh = self.open(link, data, timeout)
            html = fh.read()
            fh.close()
        except:
            pass
        #return html.decode('utf-8')
        if type(html) == bytes:
            return html.decode('iso-8859-1')
        else:
            return html
