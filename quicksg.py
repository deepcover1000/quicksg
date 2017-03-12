#! /usr/bin/python
"""quicksg.py.

quicksg.py is a terminal program with some use cases.
(1) quicksg can find the current /sg thread and open a browser tab
containing that thread.

(2) quicksg can additionally with the '-f' option provide a list
of all open threads on the /pol catalog.

(3) quicksg can also find the current sg thread and any additional
threads containing additionally specified search terms
( up to a total of 2 ). It should be noted that the search terms
 are case sensitive.

Glory to Assad in Damascus!

Usage:
  quicksg.py
  quicksg.py [-h -v -f -s]
  quicksg.py [-f FIND [default: /sg]]
  quicksg.py [-s SEARCHTERMS SEARCHTERMS SEARCHTERMS [default: /sg]]
  quicksg.py [-h | --help]
  quicksg.py --version

Options:

  -h --help    Show this screen and exit.
  -f --find  FIND  --find=FIND    Get all OP threads on the catalog
  -s --search  SEARCHTERMS  --search=SEARCHTERMS     Search the catalog and
  present OP threads containing term, and open a new tab in browser for each.
  -v --version     Show version and exit.

"""
import sys
import json
from copy import deepcopy
import webbrowser
from docopt import docopt
import requests


class bcolors:
    '''
     Class to provide text colour to report
 in command line mode. Lifted gratuitously,
 from the Blender Project via stackoverflow.
'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_catalog():
    ''' A function to fetch the /pol catalog json file
    and to return it as a loaded json object. Additionally,
    to inform the user of the progress.'''
    print(bcolors.WARNING + "Getting Internetz....")
    url = 'https://a.4cdn.org/pol/catalog.json'
    req = requests.get(url)
    a_var = req.text
    b_var = json.loads(a_var)
    print(bcolors.OKGREEN + "Internetz received....")
    return b_var


def extract_catalog_info(json_file):

    # pages:
    # threads: Number, subject, comment, country of origin
    # return dicts of subject : number, subject : comment,
    # subject : country of origin

    '''A function to provide the list of threads on the catalog,
    # from the variable passed to the function by the get_catalog()
    # function. The function iterates through all the pages, in the
    # json object (b) passed to it by the call to get_catalog().
    # Additionally, the function collates the relevant info and
    # presents it back to the user at the command prompt. This
    # invokation of the reporter() function retruns only the
    # predefined /sg search strings and those netered by the user.'''
    b_var = json_file  # the json source file.
    pageNums = str(len(b_var))  # a string value of the number of pages
    subjects = []  # subject instances to be searched against by searchterms
    pages = len(b_var)  # an integer value for the number of pages in the json(b)
    dict_of_subcoms = {}  # dict to hold subject<header> : commt
    replies = {}  # an empty dict to hold subj:replies
    country_dict = {}  # dict to hold the subj:country of OP
    numbers = {}  # an empty dict to hold the subj:thread number
    print(bcolors.OKBLUE + "Processing.....")
    for page in range(pages):

        threads_per_page = len(b_var[page]['threads'])

        for thread in range(threads_per_page):

            dicts_in_q = b_var[page]['threads'][thread]

            for candidate in dicts_in_q:
                if 'sub' not in candidate:
                    pass

                else:
                    try:
                        subject = b_var[page]['threads'][thread]['sub']
                        comment = b_var[page]['threads'][thread]['com']
                        number = b_var[page]['threads'][thread]['no']
                        reply_cnt = b_var[page]['threads'][thread]['replies']
                        country_cde = b_var[page]['threads'][thread][
                            'country_name']
                        subjects.append(subject)
                        replies[str(subject)] = reply_cnt
                        numbers[str(subject)] = number
                        dict_of_subcoms[str(subject)] = comment
                        country_dict[str(subject)] = country_cde

                    except:
                        pass

    return subjects, replies, numbers, dict_of_subcoms, country_dict, pageNums


def reporter_single(searchterm, subjects, replies, numbers, dict_of_subcoms,
                    country_dict, pageNums):

    # get number comment coutry of origin for each search term + defaults
    # return output to interface
    st = searchterm
    subjects = subjects
    replies = replies
    numbers = numbers
    dict_of_subcoms = dict_of_subcoms
    country_dict = country_dict
    pageNums = pageNums

    print(bcolors.OKGREEN +
          '**********************************************************')
    print(bcolors.OKGREEN + '**' + bcolors.WARNING +
          ' QuickSG Report - Current threads on /Pol:' + bcolors.OKGREEN +
          '            **')
    print('**********************************************************')
    print(bcolors.OKGREEN + '*' + bcolors.WARNING + ' Pages: ' + bcolors.ENDC +
          pageNums + bcolors.OKGREEN +
          '                                           **')
    print('*' + bcolors.WARNING + ' Total Thread count: ' + bcolors.ENDC +
          str(len(subjects)) + bcolors.OKGREEN +
          '                                **')
    print('*' + bcolors.WARNING + ' Search Terms: ' + bcolors.ENDC +
          str(st) + bcolors.OKGREEN + '         **')

    for commen in dict_of_subcoms:
        word = str()

        commen_list = list(commen)
        for letter in commen_list:
            if letter == ' ':
                letter = '-'
                word += letter
            else:
                letter = letter
                word += letter
        word_copy = deepcopy(word)

        if len(word) > 50:

            lastdash = word.rindex('-')
            word = word[:lastdash]

        else:
            word = word_copy

        if st in word:

            print(bcolors.OKGREEN +
                  '**********************************************************')
            # print('                              ')
            print('**' + bcolors.FAIL + ' Yielding Search Term:       ' +
                  st + bcolors.OKGREEN + '                      **')
            print('**' + bcolors.OKGREEN + ' Reply count:                ' +
                  str(replies[commen]) + bcolors.OKGREEN +
                  '                       **')
            print('**' + bcolors.OKBLUE + ' Subject:  ' + commen +
                  '               ')
            print(bcolors.OKGREEN + '**' + bcolors.WARNING + bcolors.BOLD +
                  ' Link: ' + 'https://boards.4chan.org/pol/thread/' +
                  str(numbers[commen]) + '/' + word.lower())
            print(bcolors.OKGREEN +
                  '==========================================================')
            print(bcolors.OKGREEN + '**' + bcolors.OKBLUE + ' OP Origin: |' +
                  str(country_dict[commen]))
            print(bcolors.OKGREEN +
                  '==========================================================')
            print(bcolors.ENDC + ' ' + (dict_of_subcoms[commen]))
            print('                              ')
            threadlink = 'https://boards.4chan.org/pol/thread/' + str(numbers[commen]) + '/' + word.lower()

            bovine_interface(threadlink)
        else:

            pass


def reporter_multi(subjects, replies, numbers, dict_of_subcoms, country_dict,
                   pageNums):

    subjects = subjects
    replies = replies
    numbers = numbers
    dict_of_subcoms = dict_of_subcoms
    country_dict = country_dict
    pageNums = pageNums
    search_terms = ['all']
    subjects = list(set(subjects))
    subjNum = str(len(subjects))
    subjnumslist = []
    print(bcolors.OKGREEN +
          '**********************************************************')
    print(bcolors.OKGREEN + '**' + bcolors.WARNING +
          ' QuickSG Report - Current threads on /Pol:            ' +
          bcolors.OKGREEN + '**')
    print(bcolors.OKGREEN +
          '**********************************************************')
    print('*' + bcolors.WARNING + ' Pages: ' + bcolors.ENDC + str(pageNums) +
          bcolors.OKGREEN + '                                             **')
    print(bcolors.OKGREEN + '*' + bcolors.WARNING + ' Search Terms: ' +
          bcolors.ENDC + str(search_terms[0:len(
              search_terms)]) + bcolors.OKGREEN + '         **')
    print(bcolors.OKGREEN +
          '**********************************************************')

    print('*' + bcolors.WARNING + ' Total Thread count: ' + bcolors.ENDC +
          subjNum + bcolors.OKGREEN + '                                **')
    print('**********************************************************')

    subject_counter = len(subjects)

    for item in subjects:

        subject_counter -= 1
        subjnumslist.append(subject_counter)

    for commen in dict_of_subcoms:
        word = str()

        commen_list = list(commen)
        for letter in commen_list:
            if letter == ' ':
                letter = '-'
                word += letter
            else:
                letter = letter
                word += letter

        if len(word) > 50:

            lastdash = word.rindex('-')
            word = word[:lastdash]
        else:

            pass

        print(bcolors.FAIL + str(subjnumslist.pop()) + ' |' + bcolors.OKGREEN +
              commen + bcolors.OKBLUE + ' |Cnt: ' + str(country_dict[commen]) +
              bcolors.ENDC + ' |Rep_c:' + str(replies[commen]) + bcolors.BOLD +
              bcolors.WARNING +
              ' |Link:  https://boards.4chan.org/pol/thread/' +
              str(numbers[commen]) + '/' + word.lower())


def bovine_interface(link):

    '''The function that prepares firefox for opening to the
    /sg thread.'''
    webbrowser.register('firefox', 'mozilla')
    urrl = link
    webbrowser.open_new_tab(urrl)



def main():

    SG = ['/sg', ]
    ast = sys.argv
    SG = ast[1:] + SG
    arguments = docopt(__doc__, argv=SG, version='quicksg.py 1.0')
    search_term = arguments['SEARCHTERMS'] + SG
    another_var = get_catalog()
    subjects, replies, numbers, dict_of_subcoms, country_dict, pageNums = extract_catalog_info(another_var)
    arg_all = arguments['--find']
    if arg_all == True:
        reporter_multi(subjects, replies, numbers, dict_of_subcoms, country_dict, pageNums)
    else:
        for st in search_term:
            st = str(st)
            reporter_single(st, subjects, replies, numbers, dict_of_subcoms, country_dict, pageNums)


if __name__ == '__main__':

    main()
