#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Υλοποίηση βοηθητικών συναρτήσεων για την διαχείριση των API calls και των δεδομένων που επιστρέφουν.

Με την υλοποίηση των παρακάτω συναρτήσεων γίνεται μια προσπάθεια εξομάλυνσης και απλούστευσης του τρόπου με τον οποίο
θα γίνουν τα API calls στο yourdatastories. Εφόσον γίνουν τα API calls αναλύονται τα επιστρεφόμενα δεδομένα
( JSON format ) ώστε οι συναρτήσεις να επιστρέψουν εν τέλει μονάχα την καθαρή και απαραίτητη πληροφορία.

Οι κλήσεις των συναρτήσεων είναι όσο το δυνατόν πιο απλές, που σημαίνει πως αναμένουν μονάχα τα εντελώς απαραίτητα ώστε
να δημιουργήσουν στην συνέχεια, δυναμικά οι συναρτήσεις τα API calls και όχι να δίνεται κατευθείαν σε αυτές το URL API
call. Έτσι τις περισσότερες φορές αρκεί να δώσεις π.χ. μονάχα τον νομό όπου θέλεις να βρεις όλα τα έργα του και η
συνάρτηση θα σου τα επιστρέψει. Ο χρήστης λοιπόν δεν χρειάζεται να ξέρει ποιο API call χρειάζεται να καλεστεί, για να
πάρει τις πληροφορίες που θέλει, αρκεί να ξέρει μονάχα τι θέλει. :)
"""


import json
from urllib.request import urlopen
from urllib.parse import quote
from datetime import datetime
from utilities.data_set import reverse_short_regions
from utilities.tex import latex2pdf
from utilities.latex_template import set_latex

__author__      = 'Tas-sos'
__maintainer__  = 'Tas-sos'
__email__       = 'tas-sos@g-lts.info'
__copyright__   = 'CopyLeft'
__licence__     = 'GNU General Public License v3.0'
__version__     = '0.7'
__url__         = 'https://github.com/Tas-sos/yds-reports'




def get_json(url):
    """
    Συνάρτηση όπου φορτώνει σε κατάλληλη μορφή το επιστρεφόμενο JSON από ένα URL call.

    Η συνάρτηση αυτή έχει ως σκοπό να χρησιμοποιείται σε HTTP αιτήματα τα οποία επιστρέφουν τα δεδομένα JSON μορφή.
    Η λειτουργία της είναι πολύ εύκολο αλλά και πολύ σημαντική ώστε να έχουμε έναν ποιοτικό και αναγνώσιμο κώδικα.
    Απλώς εκτελεί το URL HTTP call request που της δύνεται και φορτώνει την επιστρεφόμενη JSON απάντηση στη σωστή δομή
    ( dictionary ) ώστε να είναι έτοιμη για την διαχείριση των δεδομένων.

    :param url: Η πηγή στην οποία θα γίνει το αίτημα και αναμένετε να επιστρέψει ένα JSON.
    :return: Ένα αντικείμενο τύπου JSON ( κατ' ουσία dictionary )
    """

    return json.loads(urlopen(url).read().decode('utf8'))




def print_json(json_src):
    """
    Συνάρτηση η οποία εμφανίζει με ωραίο δομημένο τρόπο/μορφή ένα JSON τύπου string.

    :param json_src: Το JSON string.
    :return: Εμφανίζει το JSON string με ευπρεπή τρόπο.
    """

    print(json.dumps(json_src, sort_keys=True, indent=4, ensure_ascii=False))




def get_projects_by_region(a_region):
    """
    Συνάρτηση όπου ζητάει και συλλέγει όλα τα έργα που υπάρχουν σε μια συγκεκριμένη *περιφερειακή ενότητα*.

    Δημιουργείτε ένα API call όπου ζητάει όλα τα έργα για την περιφερειακή ενότητα που δέχεται ως παράμετρο.
    Εφόσον εκτελεστεί το API call, επιστρέφει ένα JSON όπου περιέχει τα έργα της περιφερειακής ενότητας ("region_code").
    Επειδή δεν λαμβάνει μόνο τα έργα, αλλά και πολλές πληροφορίες για αυτά, φροντίζει να διαχωρίσει από τα
    δεδομένα και να κρατήσει, μονάχα τα id των έργων της περιφερειακής ενότητας.

    Αυτή η συνάρτηση :
    1. Λαμβάνει την περιφερειακή ενότητα για την οποία ζητούνται να βρεθούν *όλα* τα έργα,
    2. Εκτελεί το κατάλληλο URL API call και λαμβάνει την απάντηση του (που είναι σε JSON μορφή).
    3. Διαχωρίζει τα δεδομένα του JSON
    4. Τέλος κρατάει όλα τα id των έργων όπως είναι στο «linkedeconomy.org», δηλαδή τέτοιου είδους:
    «http://linkedeconomy.org/resource/PublicWork/371514».

    Εκτελείτε ένα τέτοιου είδους API call :
    http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject AND Duration:[1997 TO 2018] AND hasRelatedFeature.hasGeometry.Address.region_code:GR.AT&rows=250&start=0

    Προσοχή! Τα URL πρέπει να είναι encoded! Όχι έτσι όπως τα έχω, αλλά έτσι όπως τα κάνουν οι browsers ( για τους ειδικούς χαρακτήρες )

    :param a_region: Η περιφερειακή ενότητα π.χ. «Ipeiros» για τη οποία ζητούντα όλα τα δημόσια έργα.

    :return: Επιστρέφει ένα λεξικό όπου, «λέξη κλειδί» είναι το όνομα του έργου και η «τιμή» το id του.
    """

    year = str(datetime.now().year)  # Current year.
    region = reverse_short_regions[a_region]  # ex : 'Attiki' => 'GR.AT'

    call_url = "http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject%20AND%20Duration:[1997%20TO%20"
    call_url += year + "]%20AND%20hasRelatedFeature.hasGeometry.Address.region_code:" + region + "&rows=250&start=0"

    projects_json = get_json(call_url)

    temp_projects = {}

    for project in projects_json['data']['response']['docs']:
        temp_projects[ project['title.el'] ] = project['id']

    return temp_projects




def get_projects_by_municipality(a_municipality):
    """
    Συνάρτηση όπου ζητάει και συλλέγει όλα τα έργα που υπάρχουν σε ένα συγκεκριμένο *νομό*.

    Δημιουργείτε ένα API call όπου ζητάει όλα τα έργα για τον νομό που δέχεται ως παράμετρο.
    Εφόσον εκτελεστεί το API call, επιστρέφει ένα JSON όπου περιέχει όλα τα έργα του νομού ("region_unit.en").
    Επειδή δεν λαμβάνει μόνο τα έργα, αλλά και πολλές πληροφορίες για αυτά, φροντίζει να διαχωρίσει από τα δεδομένα και
    να κρατήσει, μονάχα τα id των έργων του νομού.

    Αυτή η συνάρτηση :
    1. Λαμβάνει τον νομό για τον οποίο ζητούνται να βρεθούν *όλα* τα έργα.
    2. Εκτελεί το κατάλληλο URL API call και λαμβάνει την απάντηση του (που είναι σε JSON μορφή).
    3. Διαχωρίζει τα δεδομένα του JSON
    4. Τέλος κρατάει όλα τα id των έργων όπως είναι στο «linkedeconomy.org», δηλαδή τέτοιου είδους:
    «http://linkedeconomy.org/resource/PublicWork/371514».

    Εκτελείτε ένα τέτοιου είδους API call :
    http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject AND Duration:[1997 TO 2018] AND hasRelatedFeature.hasGeometry.Address.region_unit.en:"N. PIREOS KE NISON"&rows=250&start=0

    Προσοχή! Τα URL πρέπει να είναι encoded! Όχι έτσι όπως τα έχω, αλλά έτσι όπως τα κάνουν οι browsers ( για τους ειδικούς χαρακτήρες )

    :param a_municipality: Τον νομό π.χ. «N. IOANNINON», για τον οποίο θα αναζητήσει όλα τα δημόσια έργα.

    :return: Επιστρέφει ένα λεξικό όπου, «λέξη κλειδί» είναι το όνομα του έργου και η «τιμή» το id του.
    """

    year = str(datetime.now().year)  # Current year.

    call_url = "http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject%20AND%20Duration:[1997%20TO%20"
    call_url += year + "]%20AND%20hasRelatedFeature.hasGeometry.Address.region_unit.en:%22" + quote(a_municipality) + "%22&rows=250&start=0"

    projects_json = get_json(call_url)

    temp_projects = {}

    for project in projects_json['data']['response']['docs']:
        temp_projects[ project['title.el'] ] = project['id']

    return temp_projects




def get_project_data(a_project_url_id, view=False):
    """
    Συνάρτηση όπου συλλέγει και επιστρέφει τα δεδομένα ενός έργου.

    Η συνάρτηση αυτή δέχεται το URL id του έργου από το «linkedeconomy.org» και έπειτα κρατάει από αυτό τα βασικά του
    χαρακτηριστικά, τα οποία προς το παρών είναι :
        - id            : Το "linkedeconomy.org" URL προς το έργο.
        - title         : Ο τίτλος του έργου.
        - description   : Η περιγραφή του έργου.
        - region        : Η περιφερειακή ενότητα του έργου.
        - municipality  : Ο δήμος του έργου.
        - buyer_name    : Το όνομα του αγοραστή του έργου.
        - start_date    : Πότε άρχισε το έργο.
        - end_date      : Πότε τελείωσε το έργο.
        - document_URL  : TODO : ????
        - coordinates   : Η συντεταγμένες του έργου.

    :param a_project_url_id: Το URL id ενός συγκεκριμένου έργου προς το «linkedeconomy.org» π.χ. :
    http://linkedeconomy.org/resource/PublicWork/216004

    :param view: Παράμετρος ελέγχου εκτύπωσης στην κονσόλα ή όχι των στοιχείων του έργου.

    :return: Επιστρέφει ένα λεξικό το οποίο εμπεριέχει τα στοιχεία του έργου που αναγράφονται παραπάνω.
    Όμως αν κατά την κλήση της, τεθεί ρητά τιμή "True" στην προαιρετική παράμετρο "view", τότε επιπλέον θα εμφανίσει τα
    δεδομένα του έργου και στην κονσόλα.
    """

    call_url = "http://platform.yourdatastories.eu/api/json-ld/model/describe.tcl?context=0&id=" + a_project_url_id

    project = get_json(call_url)

    if view:
        print("Project id : ",              project['data']['id'], end="\n\n" )
        print("Project Title : ",           project['data']['title']['el'], end="\n\n" )
        print("Project Description : ",     project['data']['description']['el'], end="\n\n" )
        print("Project Region : ",          project['data']['hasRegion']['name'], end="\n\n" )
        print("Project Municipality : ",    project['data']['hasOperationalCode']['prefLabel']['el'], end="\n\n" )
        print("Project completion : ",      project['data']['completionOfPayments'], end="\n\n")
        print("Project Buyer name : ",      project['data']['buyer']['name']['el'], end="\n\n" )
        print("Project Start date : ",      project['data']['startDate'], end="\n\n" )
        print("Project End date : ",        project['data']['endDate'], end="\n\n" )
        print("Document URL : ",            project['data']['documentUrl'], end="\n\n" )
        print("Project coordinates : {0}".format( project['data']['hasRelatedFeature']['hasGeometry']['asWKT'] ) )

    data = {
        "id":           project['data']['id'] ,
        "title":        project['data']['title']['el'] ,
        "description":  project['data']['description']['el'] ,
        "region":       project['data']['hasRegion']['name'] ,
        "municipality": project['data']['hasOperationalCode']['prefLabel']['el'] ,
        "completion":   project['data']['completionOfPayments'],
        "buyer_name":   project['data']['buyer']['name']['el'],
        "start_date":   project['data']['startDate'],
        "end date":     project['data']['endDate'],
        "document_URL": project['data']['documentUrl'],
        "coordinates":  project['data']['hasRelatedFeature']['hasGeometry']['asWKT']
         }

    return data



def pdf_save(pdf_source, target_file):
    """
    Δημιουργεία ενός PDF.

    Συνάρτηση όπου έχει ένα πολύ απλό σκοπό :
    Αναλαμβάνει να πάρει όλον τον κώδικα pdf και να τον γράψει απλώς σε ένα (δυαδικό - PDF) αρχείο.

    :param pdf_source: Ο κώδικας PDF.
    :param target_file: Το όνομα του αρχείου PDF που θα δημιουργήσει.
    :return: Δημιουργεί ένα PDF.
    """

    file = open(target_file, 'wb')
    file.write(pdf_source)
    file.close()




def generate_pdf(project_data, file_name):

    # document = r"""
    #     \documentclass{article}
    #     \begin{document}
    #     Hello, World!
    #     \end{document}
    #     """
    document = set_latex(project_data)

    pdf = latex2pdf(document)
    pdf_save(pdf, file_name)




if __name__ == '__main__':

    # Get list of projects:
    # projects = get_projects_by_region("Ipeiros")
    # projects = get_projects_by_municipality("N. IOANNINON")

    # for k, v in projects.items():
    #     print(k, " ~ ", v, end="\n\n")

    # Get data of a project:
    project_url = "http://linkedeconomy.org/resource/PublicWork/299500"
    project_data = get_project_data(project_url)
    # for k, v in project_data.items():
    #     print(k, " ~ ", v)

    # Generate a PDF for a project:
    generate_pdf(project_data, '299500.pdf')

