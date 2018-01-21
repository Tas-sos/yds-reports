"""
Προσθήκη μερικών δικών μου φίλτρων.

Το παρών αρχείο κώδικα δημιουργήθηκε με σκοπό την δημιουργία δικών μου template tag φίλτρων που έκρινα πως
είναι απαραίτητα.

Για την δημιουργία των φίλτρων ακολούθησα τις επίσημες οδηγίες :
https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/
"""

from django import template
from utilities.data_set import regions, municipality



register = template.Library()


@register.filter(name='split_id_from_url')
def split_id_from_url(arg):
    """
    Επιστροφή του id του έργου.

    Αποκόπτει το id, από το URL ενός έργου από το «linkedeconomy.org»
    :param arg: Το URL προς το έργο, π.χ. : http://linkedeconomy.org/resource/PublicWork/216004
    :return: Μονάχα το id του, π.χ. : 216004
    """
    return arg.split('/')[5]




@register.filter(name='region_gr_name')
def region_gr_name(arg):
    """
    Επιστροφή του ονόματος της περιφέρειας στα νέα ελληνικά.

    Βρίσκει από το λεξικό και επιστρέφει το όνομα της περιφέρειας στα νέα ελληνικά.
    :param arg: Το όνομα μιας περιφέρειας ( σε greeklish ) όπως είναι στο λεξικό regions ( data_set.py ), π.χ. : "Attiki".
    :return: Το όνομα της περιφέρειας στα νέα ελληνικά, π.χ. "Αττική".
    """
    return regions[arg]




@register.filter(name='municipality_gr_name')
def municipality_gr_name(a_region, a_municipality):
    """
    Επιστροφή του ονόματος του δήμου στα νέα ελληνικά.

    Βρίσκει από το λεξικό και επιστρέφει το όνομα του δήμου στα νέα ελληνικά.
    :param a_region: Το όνομα μιας περιφέρειας ( σε greeklish ) όπως είναι στο λεξικό regions ( data_set.py ), π.χ. : "Attiki".
    :param a_municipality: Το όνομα του δήμου ( σε greeklish ) όπως είναι στο λεξικό municipality ( data_set.py ), π.χ. : "N. ATHINON".
    :return: Το όνομα του δήμου στα νέα ελληνικά, π.χ. "Ν. Αθηνών".
    """
    return municipality[a_region][a_municipality]



