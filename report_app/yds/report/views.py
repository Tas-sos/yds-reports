from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from utilities.data_set import regions, municipality
from utilities.project import get_projects_by_municipality, get_project_data, search, generate_pdf, pdf_name


def index(request):
    """
    View που καλείται όταν ο χρήστης επισκεφτεί την αρχική σελίδα και θα πρέπει να επιλέξει μια περιφερειακή ενότητα.

    Δίνεται στη σελίδα το λεξικό με όλες τις περιφερειακές ενότητες καθώς και την πρώτη
    ( στο λεξικό - για λόγους υλοποίησης στο action της φόρμας της σελίδας - ) περιφερειακή ενότητα.

    :param request: Το αίτημα του χρήστη.
    :return: Την σελίδα «report/index.html» με τις παραπάνω πληροφορίες.
    """

    return render(request, 'report/index.html', {'regions': regions,
                                                 'first_region': list(regions.keys())[0]})




def selected_region(request, a_region):
    """
    View που καλείται όταν ο χρήστης έχει επιλέξει μια περιφερειακή ενότητα και θα πρέπει να επιλέξει ένα νομό.

    Δίνεται στην σελίδα  :
        - Η επιλεγμένη περιφερειακή ενότητα.
        - Το λεξικό με όλους τους νομούς της περιφερειακής ενότητας που επιλέχθηκε.
        - Τον πρώτο νομό ( στο λεξικό - για λόγους υλοποίησης στο action της φόρμας της σελίδας - )

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
    View που καλείται όταν ο χρήστης έχει επιλέξει μια περιφερειακή ενότητα και νομό και θα πρέπει να επιλέξει ένα έργο.

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

                    context = {'selected_region': a_region,
                               'selected_municipality': a_municipality,
                               'projects': projects}

                    return render(request, 'report/municipality.html', context)
            except KeyError:
                raise Http404("The municipality \"{0}\" was not found it!".format(a_municipality))
    except KeyError:
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




def create_pdf(request, a_region, a_municipality, project_url_id):

    url = "http://linkedeconomy.org/resource/PublicWork/" + str(project_url_id)
    file_name = str(project_url_id) + ".pdf"

    # Downloading data from this project :
    project_data = get_project_data(url)

    # Search for related articles for this project :
    related_articles = search(project_data['title'])

    # Generating the report PDF for this project:
    try:
        generate_pdf(project_data, related_articles, pdf_name("report/static/report/download/", url))
    except ValueError as log:
        print("Compiler error from LaTeX, for project : {0}".format(url))
        print('-------------------------------------------------------------------------------------------------------')
        print('LaTex Log |')
        print('-----------')
        print(log)
        print('-------------------------------------------------------------------------------------------------------')

        return render(request, 'report/pdf.html', {'project_url': url})

    file_system = FileSystemStorage('report/static/report/download/')
    with file_system.open(file_name) as pdf:

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'

        return response






