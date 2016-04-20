"""
Fisier de configurare
"""

from __future__ import print_function


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


OPTIONS = {
    '-w': 'number of workers',
    '-h': 'usage information'
}


def help_function(name):
    """Metoda afiseaza un mesaj de ajutor
    in cazul in care datele introduse sunt gresite
    """
    print('{0}NAME{1}'.format(BOLD, END))
    print('\t {0}\n'.format(name))
    print('{0}SYNOPSIS{1}'.format(BOLD, END))
    print('\t python {0}{1}{2} [OPTIONS] HTML_FILES_DIR SPECIAL_WORDS_DIR OUTPUT_DIR\n'
          .format(BOLD, name, END))
    print('{0}DESCRIPTION{1}'.format(BOLD, END))
    print('\t {0}{1}{2} parses a given set of html files returning'
          'the {3}DIRECT{4} and {5}INVERSE{6} index\n'
          .format(BOLD, name, END, UNDERLINE,
                  END, UNDERLINE, END))
    print('{0}OPTIONS{1}'.format(BOLD, END))
    for key, value in OPTIONS.iteritems():
        print('\t {0}{1}{2} {3}\t'
              .format(BOLD, key, END, value))
    print('{0}EXAMPLE{1}'.format(BOLD, END))
    print('\t python {0}{1}{2} var/www/riw special_files result'
          .format(BOLD, name, END))
