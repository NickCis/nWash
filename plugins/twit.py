import json
import urlDownloader

__persistent__ = {}
__definition__ = {
    #Command to be executed in the shell
    "command": "twit",
    "name": "twit",
    #In this case, as it is a plugin, is the name of the file
    "do": "twit",
    "child": [ #Childs are extended with parent data
        {
            #Argument of the parent command
            "command": "user",
            "data": [ #List of arguments
                {
                    #Name the argument will have in the struct dict
                    "name": "screenname",
                    "type": "text"
                }
            ],
            #Extra data used internally by the command
            "url": "https://api.twitter.com/1/statuses/user_timeline.json?screen_name={{user}}",
            "doDown": "doUser"
        },
        {
            "command": "search",
            "data": [
                {
                    "name": "q",
                    "type": "text"
                }
            ],
            "url": "http://search.twitter.com/search.json?q={{q}}&rpp=5&include_entities=true",
            "doDown": "doSearch"
        }
    ],
    #Extra data:
    "url": "https://api.twitter.com/"

}



def run(data, extra, args, struct, config, self):
    if not 'Downloader' in __persistent__:
        __persistent__['Downloader'] = urlDownloader.UrlDownloader()

    if "doDown" in struct and struct["doDown"] in __downDict:
        funcs = __downDict[struct["doDown"]]
        funcs[1](funcs[0](data, extra, args, struct, config, self))


    return


def parserUser(data, extra, args, struct, config, self):
    url = struct['url'].replace("{{user}}", data["screenname"])
    html = __persistent__['Downloader'].downloadPage(url)
    try:
        html = json.loads(html)
    except:
        pass

    return html

def doUser(tweets):
    for tw in tweets:
        print('[', tw['created_at'], ']', tw['user']['name'], "->", tw['text'])

def parserSearch(data, extra, args, struct, config, self):
    url = struct['url'].replace("{{q}}", data["q"])
    html = __persistent__['Downloader'].downloadPage(url)
    try:
        html = json.loads(html)
    except:
        pass

    return html

def doSearch(tweets):
    for tw in tweets['results']:
        print('[', tw['created_at'], ']', tw['from_user'], "->", tw['text'])

__downDict = {
    'doUser': (parserUser, doUser),
    'doSearch': (parserSearch, doSearch)
}
