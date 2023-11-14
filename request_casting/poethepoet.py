from request_casting.reusing.github import download_from_github
from gettext import translation
from importlib.resources import files
#from request_casting.reusing.file_functions import replace_in_file
from request_casting import __version__
from os import system
from sys import argv

        
try:
    t=translation('request_casting', files("request_casting") / 'locale')
    _=t.gettext
except:
    _=str


def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local==False:
        download_from_github('turulomio','reusingcode','python/github.py', 'request_casting/reusing/')
        download_from_github('turulomio','reusingcode','python/casts.py', 'request_casting/reusing/')
        download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'request_casting/reusing/')
        download_from_github('turulomio','reusingcode','python/file_functions.py', 'request_casting/reusing/')
    
#    replace_in_file("request_casting/reusing/casts.py","from currency","from request_casting.reusing.currency")


def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o request_casting/locale/request_casting.pot  request_casting/*.py request_casting/reusing/*.py ")
        system("msgmerge -N --no-wrap -U request_casting/locale/es.po request_casting/locale/request_casting.pot")
        system("msgfmt -cv -o request_casting/locale/es/LC_MESSAGES/request_casting.mo request_casting/locale/es.po")
        system("msgfmt -cv -o request_casting/locale/en/LC_MESSAGES/request_casting.mo request_casting/locale/en.po")

def release():
    print("""Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Cambiar la versión en pyproject.toml
  * Modificar el Changelog en README
  * poe translate
  * linguist
  * poe translate
  * git commit -a -m 'request_casting-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * poetry build
  * poetry publish --username --password  
  * Crea un nuevo ebuild de request_casting Gentoo con la nueva versión
  * Subelo al repositorio del portage
""".format(__version__))
