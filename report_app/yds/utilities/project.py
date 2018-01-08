#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Υλοποίηση βοηθητικών συναρτήσεων για την διαχείριση των API calls και των δεδομένων που επιστρέφουν.

Με την υλοποίηση των παρακάτω συναρτήσεων γίνεται μια προσπάθεια εξομάλυνσης και απλούστευσης του τρόπου με τον οποίο
θα γίνουν τα API calls στο yourdatastories. Εφόσον γίνουν τα API calls αναλύονται τα επιστρεφόμενα δεδομένα
( JSON format ) ώστε οι συναρτήσεις να επιστρέψουν εν τέλει μονάχα την καθαρή και απαραίτητη πληροφορία.

Οι κλήσεις των συναρτήσεων είναι όσο το δυνατόν πιο απλές, που σημαίνει πως αναμένουν μονάχα τα εντελώς απαραίτητα ώστε
να δημιουργήσουν δυναμικά στην συνέχεια τα API calls και όχι να δίνεται κατευθείαν σε αυτές το URL API call.
Έτσι τις περισσότερες φορές αρκεί να δώσεις π.χ. μονάχα τον νομό όπου θέλεις να βρεις όλα τα έργα του και η
συνάρτηση θα σου τα επιστρέψει. Ο χρήστης λοιπόν δεν χρειάζεται να ξέρει ποιο API call χρειάζεται να καλεστεί, για να
πάρει τις πληροφορίες που θέλει, αρκεί να ξέρει μονάχα τι θέλει. :)
"""


import json
from urllib.request import urlopen
from urllib.parse import quote
from datetime import datetime

from .data_set import reverse_short_regions
from .latex.tex import latex2pdf
from .latex.tex_template import set_latex
from .google.search import search


__author__      = 'Tas-sos'
__maintainer__  = 'Tas-sos'
__email__       = 'tas-sos@g-lts.info'
__copyright__   = 'CopyLeft'
__licence__     = 'GNU General Public License v3.0'
__version__     = '1'
__url__         = 'https://github.com/Tas-sos/yds-reports'




def get_json(url):
    """
    Συνάρτηση όπου φορτώνει σε κατάλληλη μορφή το επιστρεφόμενο JSON από ένα URL call.

    Η συνάρτηση αυτή έχει ως σκοπό να χρησιμοποιείται σε HTTP αιτήματα τα οποία επιστρέφουν τα δεδομένα σε JSON μορφή.
    Η λειτουργία της είναι πολύ εύκολη αλλά και πολύ σημαντική ώστε να έχουμε έναν ποιοτικό και αναγνώσιμο κώδικα.
    Απλώς εκτελεί το URL HTTP call request που της δύνεται και φορτώνει την επιστρεφόμενη JSON απάντηση στη σωστή δομή
    δεδομένων ( dictionary ) ώστε τα δεδομένων να είναι εύκολα διαχειρίσιμα.

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
    Επειδή δεν λαμβάνει μόνο τα έργα, αλλά και πολλές επιμέρους πληροφορίες για αυτά, φροντίζει να τις διαχωρίσει από τα
    δεδομένα και να κρατήσει, μονάχα τα id των έργων της περιφερειακής ενότητας.

    Αυτή η συνάρτηση :
    1. Λαμβάνει την περιφερειακή ενότητα για την οποία ζητούνται να βρεθούν *όλα* τα έργα,
    2. Εκτελεί το κατάλληλο URL API call και λαμβάνει την απάντηση του (που είναι σε JSON μορφή).
    3. Διαχωρίζει τα δεδομένα του JSON
    4. Τέλος κρατάει όλα τα id των έργων όπως είναι στο «linkedeconomy.org», δηλαδή τέτοιου είδους:
       http://linkedeconomy.org/resource/PublicWork/371514.

    Εκτελείτε ένα τέτοιου είδους API call :
    http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject AND Duration:[1997 TO 2018] AND hasRelatedFeature.hasGeometry.Address.region_code:GR.AT&rows=250&start=0

    Προσοχή! Το URL πρέπει να είναι encoded! Όχι έτσι όπως το έχω, αλλά έτσι όπως τα κάνουν οι browsers ( για τους ειδικούς χαρακτήρες )

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
    Επειδή δεν λαμβάνει μόνο τα έργα, αλλά και πολλές επιμέρους πληροφορίες για αυτά, φροντίζει να τις διαχωρίσει από τα
    δεδομένα και να κρατήσει, μονάχα τα id των έργων της περιφερειακής ενότητας.

    Αυτή η συνάρτηση :
    1. Λαμβάνει τον νομό για τον οποίο ζητούνται να βρεθούν *όλα* τα έργα.
    2. Εκτελεί το κατάλληλο URL API call και λαμβάνει την απάντηση του (που είναι σε JSON μορφή).
    3. Διαχωρίζει τα δεδομένα του JSON
    4. Τέλος κρατάει όλα τα id των έργων όπως είναι στο «linkedeconomy.org», δηλαδή τέτοιου είδους:
       http://linkedeconomy.org/resource/PublicWork/371514.

    Εκτελείτε ένα τέτοιου είδους API call :
    http://platform.yourdatastories.eu/api/json-ld/component/search.tcl?lang=el&q=type:PublicProject AND Duration:[1997 TO 2018] AND hasRelatedFeature.hasGeometry.Address.region_unit.en:"N. PIREOS KE NISON"&rows=250&start=0

    Προσοχή! Το URL πρέπει να είναι encoded! Όχι έτσι όπως το έχω, αλλά έτσι όπως τα κάνουν οι browsers ( για τους ειδικούς χαρακτήρες )

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
        - id				: Το "linkedeconomy.org" URL προς το έργο.
        - title				: Ο τίτλος του έργου.
        - description			: Η περιγραφή του έργου.
        - region			: Η περιφερειακή ενότητα του έργου.
        - municipality			: Ο δήμος του έργου.
        - completion_of_payments	: Το ποσοστό ολοκλήρωσης των πληρωμών.
        - completion_of_contracts	: Το ποσοστό ολοκλήρωσης των συμβάσεων.
        - buyer_name			: Το όνομα του αγοραστή του έργου.
        - buyer_id_URL			: Το "linkedeconomy.org" URL του αγοραστή.
        - bayer_VAT			: Το Α.Φ.Μ. του αγοραστή.
        - start_date			: Πότε άρχισε το έργο.
        - end_date			: Πότε τελείωσε το έργο.
        - budget			: Ο προϋπολογισμός του έργου.
        - spending			: Η συνολική δαπάνη του έργου.
        - document_URL			: TODO : ????
        - coordinates			: Η συντεταγμένες του έργου.

    :param a_project_url_id: Το URL id ενός συγκεκριμένου έργου προς το «linkedeconomy.org» π.χ. :
    http://linkedeconomy.org/resource/PublicWork/216004

    :param view: Προαιρετική παράμετρος ελέγχου εκτύπωσης στην κονσόλα ή όχι των στοιχείων του έργου.

    :return: Επιστρέφει ένα λεξικό το οποίο εμπεριέχει τα στοιχεία του έργου που αναγράφονται παραπάνω.
    Όμως αν κατά την κλήση της, τεθεί ρητά τιμή "True" στην προαιρετική παράμετρο "view", τότε επιπλέον θα εμφανίσει τα
    δεδομένα του έργου και στην κονσόλα.
    """

    call_url = "http://platform.yourdatastories.eu/api/json-ld/model/describe.tcl?context=0&id=" + a_project_url_id

    project = get_json(call_url)

    data = {
        "id_URL":                   project['data']['id'] ,
        "title":                    project['data']['title']['el'] ,
        "description":              project['data']['description']['el'] ,
        "region":                   project['data']['hasRegion']['name'] ,
        "municipality":             project['data']['hasOperationalCode']['prefLabel']['el'] ,
        "completion_of_payments":   project['data']['completionOfPayments'],
        "completion_of_contracts":  project['data']['completionOfContracts'],
        "buyer_name":               project['data']['buyer']['name']['el'],
        "buyer_id_URL":             project['data']['buyer']['id'],
        "start_date":               project['data']['startDate'],
        "end_date":                 project['data']['endDate'],
        "budget":                   project['data']['hasBudgetAggregate']['aggregatedAmount'],
        "spending":                 project['data']['hasSpendingAggregate']['aggregatedAmount'],
        "document_URL":             project['data']['documentUrl'],
         }

    # Επειδή μερικά δεδομένα, μερικές φορές δεν υπάρχουν σε όλα τα έργα.

    try:
        data['bayer_VAT'] = project['data']['buyer']['vatID']
    except KeyError:
        data['bayer_VAT'] = '-'

    try:
        data['coordinates'] = project['data']['hasRelatedFeature']['hasGeometry']['asWKT']
    except (KeyError, TypeError):  # TODO: Να το ελέγξω το "TypeError" ( μου έβγαζε "list indices must be integers or slices, not str" )
        data['coordinates'] = '-'


    if view:
        for k, v in data.items():
            print("{0} \t: {1}".format(k, v))

    return data




def pdf_save(pdf_source, target_file):
    """
    Αποθήκευση του PDF αναφοράς.

    Η συνάρτηση όπου έχει ένα πολύ απλό σκοπό :
    Αναλαμβάνει να πάρει όλον τον κώδικα LaTeX και να τον γράψει απλώς σε ένα (δυαδικό - PDF) αρχείο.

    :param pdf_source: Ο κώδικας LaTex.
    :param target_file: Η διαδρομή (που) και όνομα του αρχείου PDF που θα δημιουργήσει.
    :return: Δημιουργία ενός αρχείου PDF.
    """

    file = open(target_file, 'wb')
    file.write(pdf_source)
    file.close()




def generate_pdf(project_data, articles, file_name):
    """
    Δημιουργία του PDF αναφοράς.

    Η συνάρτηση αυτή αναλαμβάνει να δημιουργήσει το PDF report document με τα στοιχεία του έργου που τις δύνονται.

    :param project_data: Τα δεδομένα που έχουν συλλεχθεί.
    :param file_name: Το όνομα του PDF αρχείου.
    :param articles: Τα σχετικά με αυτό το έργο άρθρα, που βρέθηκαν στο διαδίκτυο.
    :return: Ένα έγγραφο PDF με συγκεκριμένα δεδομένα του έργου.
    """

    document = set_latex(project_data, articles)
    pdf = latex2pdf(document)
    pdf_save(pdf, file_name)




def pdf_name(a_target_path, a_project_id):
    """
    Ορισμός διαδρομής και ονόματος αποθήκευσης του PDF αρχείου.

    Η συνάρτηση αυτή αναλαμβάνει να δημιουργήσει με ένα καθορισμένο τρόπο/πρότυπο το όνομα με το οποίο θα αποθηκευτεί
    το προς δημιουργία PDF report document. Επίσης θέτει και την διαδρομή στην οποία θα αποθηκευτεί το αρχείο.

    TODO: Ίσος χρειαστεί στο μέλλον η συνάρτηση αυτή να εξελιχθεί ώστε να προσαρμοστεί στις απαιτήσεις του web server.

    :param a_target_path: Η διαδρομή όπου θα αποθηκευτεί το PDF αρχείο.
    :param a_project_id: Το URL id του έργου από το «linkedeconomy.org»
    :return: String με το όνομα το οποίο θα αποθηκευτεί το προς δημιουργία PDF report.
    """

    return a_target_path + a_project_id.split('/')[5] + '.pdf'




if __name__ == '__main__':

    # Get list of projects:
    # projects = get_projects_by_region("Ipeiros")
    # projects = get_projects_by_municipality("N. IOANNINON")

    # for k, v in projects.items():
    #     print(k, " ~ ", v, end="\n\n")

    # TODO: Βελτιστοποίηση επιδόσεων :
    # Λόγο του ότι οι αναζητήσεις των πληροφοριών και η συλλογή των δεδομένων τους ( είτε για το δημόσιο έργο, είτε για
    # για σχετικές με αυτό δημοσιεύσεις στο διαδίκτυο ) απαιτούν ένα σημαντικό χρονικό διάστημα, θα πρέπει να ερευνηθεί
    # ο τρόπος με τον οποίο αυτό μπορεί να βελτιωθεί. Μία απλή και γρήγορη σκέψη, είναι να δημιουργούνται δύο
    # διαφορετικά νήματα διεργασιών όπου το καθένα να αναλαμβάνει την δική του αναζήτηση και συλλογή των δεδομένων και
    # μόλις ολοκληρωθούν και τα δύο, τότε να προχωράει το πρόγραμμα στην δημιουργία του PDF report document.
    # Αλλά : Για την αναζήτηση, χρειάζεται το όνομα του έργου!!
    # Προς το παρών παίρνει περίπου 3-4" ώστε να συλλεχθούν όλα τα δεδομένα και να παραχθεί το τελικό έγγραφο αναφοράς.

    # Get data of a project:
    project_url = "http://linkedeconomy.org/resource/PublicWork/299500"  # 299500  # 216004
    project_data = get_project_data(project_url)
    # for k, v in project_data.items():
    #     print(k, " ~ ", v)

    # Search for related articles for this project :
    related_articles = search( project_data['title'] )

    # Generate a PDF for a project:
    generate_pdf(project_data, related_articles, pdf_name("/home/tas-sos/workspace/python/YDS_simply_functionality/", project_url))


