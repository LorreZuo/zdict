import configparser
import getopt
import locale
import os
import readline
import sys

from argparse import ArgumentParser

from . import constants
from .completer import DictCompleter
from .dictionaries import DictBase
from .plugins.yahoo_dict import YahooDict


if not os.path.isdir(constants.BASE_DIR):
    os.mkdir(constants.BASE_DIR)

try:
    config = configparser.ConfigParser()
    config.readfp(open(os.path.join(constants.BASE_DIR, 'rc')))
    playback = config.get('zdict', 'playback')
    prefetch = config.get('zdict', 'prefetch')
except:
    pass


def cleanup():
    exit()


def main():
    # Check user's encoding settings
    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        cleanup()
    else:
        if enc != "UTF-8":
            print("zdict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            cleanup()

    # parse args
    #parser = ArgumentParser(usage="Usage: zdict [options] word1 word2 ......")
    parser = ArgumentParser()

    parser.add_argument('words',
                        metavar='word',
                        type=str,
                        nargs='*',
                        help='a word for searching its translation')

    parser.add_argument("-v", "--version",
                      dest="version",
                      help="show version.",
                      default=False,
                      action="store_true")
    parser.add_argument("-d", "--disable-db-cache",
                      dest="disable_db_cache",
                      help="temporarily not using the result from db cache.\
                            (still save the result into db)",
                      default=False,
                      action="store_true")
    args = parser.parse_args()

    if args.version is True:
        print(constants.VERSION)
        cleanup()
    elif len(sys.argv) <= 2:
        zdict = YahooDict()

        # configure readline and completer
        readline.parse_and_bind("tab: complete")
        readline.set_completer(DictCompleter().complete)
        zdict.loop_prompt(args.disable_db_cache)
    else:
        zdict = YahooDict()

        for w in args.words:
            zdict.lookup(w, args.disable_db_cache)
        cleanup()