from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from utilities.data_set import regions, municipality
from utilities.project import get_projects_by_municipality, get_project_data, search, generate_pdf, pdf_name

from os.path import dirname, abspath, join, getctime
from os import listdir, remove
from datetime import datetime, timedelta
import time
import threading



def index(request):
    """
    View που καλείται όταν ο χρήστης επισκεφτεί την αρχική σελίδα και θα πρέπει να επιλέξει μια περιφερειακή ενότητα.

    Δίνεται στη σελίδα :
    - Το λεξικό με όλες τις περιφερειακές ενότητες.
    - Την πρώτη περιφερειακή ενότητα ( στο λεξικό - για λόγους υλοποίησης στο action της φόρμας της σελίδας - ).

    :param request: Το αίτημα του χρήστη.
    :return: Την σελίδα «report/index.html» με τις παραπάνω πληροφορίες.
    """

    return render(request, 'report/index.html', {'regions': regions,
                                                 'first_region': list(regions.keys())[0]})




def about(request):
    """
    View που καλείται όταν ο χρήστης επισκεφτεί την σελίδα "Πληροφορίες".

    Απλώς επιστρέφει ένα στατικό HTML αρχείο.

    :param request: Το αίτημα του χρήστη.
    :return: Την σελίδα «report/about.html».
    """

    return render(request, 'report/about.html')




def selected_region(request, a_region):
    """
    View που καλείται όταν ο χρήστης έχει επιλέξει μια περιφερειακή ενότητα και θα πρέπει να επιλέξει ένα νομό.

    Δίνεται στην σελίδα  :
        - Η επιλεγμένη περιφερειακή ενότητα.
        - Το λεξικό με όλους τους νομούς της περιφερειακής ενότητας που επιλέχθηκε.
        - Τον πρώτο νομό ( στο λεξικό - για λόγους υλοποίησης στο action της φόρμας της σελίδας - ).

    :param request: Το αίτημα του χρήστη.
    :param a_region: Μια περιφερειακή ενότητα.
    :return: Την σελίδα με τις παραπάνω πληροφορίες.
    """

    try:
        if regions[a_region]:

            context = {'selected_region': a_region,
                       'first_municipality': list(municipality[a_region].keys())[0],
                       'municipalities': municipality[a_region]}

            return render(request, 'report/region.html', context)

    except KeyError:  # Αν δε βρει δηλαδή την περιφέρεια αυτή
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




def selected_municipality(request, a_region, a_municipality):
    """
    View που καλείται όταν ο χρήστης έχει επιλέξει μια περιφερειακή ενότητα και νομό, και θα πρέπει να επιλέξει ένα έργο.

    Σε αυτή την σελίδα εμφανίζονται τα έργα που υπάρχουν για τον συγκεκριμένο νομό που έχει επιλεχθεί.
    Ο χρήστης μπορεί να επιλέξει κάποιο από αυτά τα έργα και να κατεβάσει μια PDF αναφορά για αυτό.

    Δίνεται στην σελίδα  :
        - Η επιλεγμένη περιφερειακή ενότητα.
        - Τον επιλεγμένο νομό της περιφερειακής ενότητας.
        - Όλα τα έργα του νομού.

    :param request: Το αίτημα του χρήστη.
    :param a_region: Μια περιφερειακή ενότητα.
    :param a_municipality: Ένας νομός της παραπάνω περιφερειακής ενότητας.
    :return: Την σελίδα με τις παραπάνω πληροφορίες.
    """

    try:
        if regions[a_region]:  # Αν υπάρχει η περιφέρεια μέσα στις περιφέρειες
            try:
                if municipality[a_region][a_municipality]:  # Αν υπάρχει ο νομός μέσα στη συγκεκριμένη περιφέρεια!

                    projects = get_projects_by_municipality(a_municipality)

                    # Διόρθωση του project url ώστε να παίρνω μονάχα το id του.
                    for name, url in projects.items():
                        projects[name] = url.split('/')[5]

                    context = {'selected_region': a_region,
                               'selected_municipality': a_municipality,
                               'projects': projects,
                               'total_number_of_projects': len(projects)}

                    return render(request, 'report/municipality.html', context)
            except KeyError:
                raise Http404("The municipality \"{0}\" was not found it!".format(a_municipality))
    except KeyError:
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




def create_pdf(request, project_url_id):
    """
    Δημιουργία του εγγράφου αναφοράς.

    Η παρούσα συνάρτηση είναι υπεύθυνη ώστε να προσπαθήσει να δημιουργήσει ένα PDF έγγραφο αναφοράς για το έργο που θα
    της ζητηθεί και έπειτα να το επιστρέψει ένα μήνυμα επιτυχής παραγωγής του ή όχι.
    Αυτή η συνάρτηση καλείται μέσω AJAX.

    :param request: Το αίτημα του χρήστη.
    :param project_url_id: Το id του έργου ( όπως είναι στο «linkedeconomy.org» αλλά μονάχα το id του ).
    :return: Είτε το έγγραφο αναφοράς σε μορφή PDF με τα στοιχεία του έργου που δόθηκε ως παράμετρος, είτε "status=504"
             το οποίο σημαίνει πως για κάποιο λόγο δεν ήταν επιτυχής η παραγωγή του PDF.
    """

    url = "http://linkedeconomy.org/resource/PublicWork/" + str(project_url_id)
    file_name = str(project_url_id) + ".pdf"

    # To define the "STATIC_ROOT" path. ( Look at the "yds/settings.py" file. )
    base_dir = dirname( dirname(abspath(__file__)) )
    static_root = join(base_dir, "static/report/download/")

    # Downloading data from this project :
    project_data = get_project_data(url)

    # Search for related articles for this project :
    try:
        related_articles = search(project_data['title'])
    except:
        related_articles = {'Δεν ήταν δυνατή η εύρεση σχετικών δημοσιεύσεων.': '#'}


    # Delete olf PDFs:
    threading.Thread(target=delete_PDFs, args=(static_root,), kwargs={}, daemon=True).start()


    # Generating the report PDF for this project :
    try:
        generate_pdf(project_data, related_articles, pdf_name(static_root, url))
    except ValueError as log:
        print("Compiler error from LaTeX, for project : {0}".format(url))
        print('-------------------------------------------------------------------------------------------------------')
        print('LaTex Log |')
        print('-----------')
        print(log)
        print('-------------------------------------------------------------------------------------------------------')

        return HttpResponse(status=504)

    # Create success response :
    file_system = FileSystemStorage(static_root)
    with file_system.open(file_name) as pdf:

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'

        return response




def pdf_error(request, a_region, a_municipality, project_url_id):
    """
    Εμφάνιση μηνύματος σφάλματος για την παραγωγή ενός PDF.

    Όταν καλείται αυτή η συνάρτηση, τότε σημαίνει πως η παραγωγή ενός PDF δεν ήταν επιτυχής και αυτό το view αναλαμβάνει
    μονάχα να εμφανίσει μια σελίδα σφάλματα προς ενημέρωση του χρήστη.

    :param request: Το αίτημα του χρήστη.
    :param a_region: Σε ποια περιφερειακή ενότητα ανήκει το έργο που δεν ήταν εφικτή η παραγωγή του PDF.
    :param a_municipality: Σε ποιο νομό της παραπάνω περιφερειακής ενότητας ανήκει το έργο.
    :param project_url_id: Για ποιο έργο δεν ήταν εφικτή η παραγωγή του PDF.
    :return: Την σελίδα «report/pdf.html» με τις παραπάνω πληροφορίες.
    """

    context = {'region': a_region,
               'municipality': a_municipality,
               'project_id': project_url_id}

    return render(request, 'report/pdf.html', context)




def delete_PDFs( folder_path ):
    """
    Μέθοδος που αναλαμβάνει να διαγράψει όλα τα PDFs που πλέον θεωρούνται παλιά.

    Είναι μια πάρα πολύ σημαντική μέθοδος η οποία αναλαμβάνει να διαγράψει τα παλιά PDFs.
    Χωρίς αυτή ο αποθηκευτικός χώρος του διακομιστή κάποια στιγμή θα γέμιζε πλήρως και ο λόγος θα ήταν τα PDF.

    Αυτή η μέθοδος τρέχει παράλληλα κάθε φορά που εκτελείται η μέθοδος παραγωγής ενός νέου εγγράφου PDF.

    :param folder_path: Ο κατάλογος που αποθηκεύονται τα PDFs.
    :return: Θα πρέπει να έχουν διαγραφεί τα έργα που είναι παραπάνω από μια ώρα δημιουργημένα.
    """

    # Find PDF files.
    files = [ f for f in listdir(folder_path) ]

    # The time from an hour ago
    one_hour_before = datetime.now() + timedelta(hours=-1)

    # Delete older files
    for pdf in files:
        if datetime.strptime(time.ctime(getctime( folder_path + pdf )), "%a %b %d %H:%M:%S %Y") < one_hour_before:
            remove(folder_path + pdf)


