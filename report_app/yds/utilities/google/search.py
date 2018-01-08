#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Αναζήτηση στην μηχανή αναζήτησης της Google.

Αυτό το κομμάτι λογισμικού δημιουργήθηκε ώστε να λειτουργεί επικουρικά στο κυρίως τμήμα αυτού του έργου, που είναι η
δημιουργία των αρχείων αναφοράς PDF για δημόσια έργα.
Αυτό το τμήμα λογισμικού αναλαμβάνει να αναζητήσει στην μηχανή αναζήτησης της google με το όνομα του δημόσιου έργου
για το οποίο θα δημιουργηθεί το έγγραφο αναφοράς PDF και να επιστρέψει τα αποτελέσματα της πρώτης σελίδας.

Απαιτήσεις :
Το τμήμα λογισμικού που αναλαμβάνει να κατεβάσει, να αναλύσει και εν τέλει να φέρει τα αποτελέσματα της αναζήτησης
βασίζεται στην βιβλιοθήκη :  pyGoogleSearch  (2.05)  https://github.com/mdonnalley/pyGoogleSearch
Η εν λόγο βιβλιοθήκη βασίζεται σε ακόμη δύο βιβλιοθήκες :
- BeautifulSoup4  (4.6.0)  https://www.crummy.com/software/BeautifulSoup/
- requests  (2.18.4)  http://python-requests.org/
Οπότε απαιτείτε η εγκατάσταση των παραπάνω.
"""


from pyGoogleSearch import *
from collections import OrderedDict


__author__      = 'Tas-sos'
__maintainer__  = 'Tas-sos'
__email__       = 'tas-sos@g-lts.info'
__copyright__   = 'CopyLeft'
__licence__     = 'GNU General Public License v3.0'
__version__     = '1'
__url__         = 'https://github.com/Tas-sos/yds-reports'




def search(a_question):
    """
    Αναζήτηση στην μηχανή αναζήτηση της Google με βάση κάποιο κείμενο.

    Η συνάρτηση αυτή αναλαμβάνει να αναζητήσει ένα κείμενο στην μηχανή αναζήτησης της Google.
    Επιστρέφει τα αποτελέσματα μονάχα της *πρώτης* σελίδας. - Για εμάς προς το παρών είναι αρκετά.
    Συνολικά επιστρέφει 10 αποτελέσματα - όλα τα αποτελέσματα της πρώτης σελίδας -

    TODO: Δεν έχω ελέγξει την περίπτωση που τυχόν θα γίνουν πάρα πολλά ερωτήματα τι θα γίνει. Ίσος η google το δει
    TODO: περίεργο και με υποβάλει σε δοκιμασίες ή ακόμη να μου απαγορεύσει την είσοδο και να με βάλει σε blacklist.

    :param a_question: Το ερώτημα προς την μηχανή αναζήτησης.
    :return: Τα αποτελέσματα που βρέθηκαν σε ένα λεξικό. results[article title] = article link
    """

    results = OrderedDict()

    raw_web_data = Google(a_question).search()

    for row in raw_web_data['results']:
        results[ row['link_text'] ] = row['link']

    return results

