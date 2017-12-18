from django.shortcuts import render
from django.http import Http404
from .utilities.data_set import regions, municipality
from .utilities.project import get_projects_by_municipality


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
            if municipality[a_region][a_municipality]:  # Αν υπάρχει ο νομός μέσα στη συγκεκριμένη περιφέρεια!

                projects = get_projects_by_municipality(a_municipality)


                context = {'selected_region': a_region,
                           'selected_municipality': a_municipality,
                           'projects': projects}
                return render(request, 'report/municipality.html', context)
    except KeyError:
        raise Http404("The municipality \"{0}\" was not found it!".format(a_region))

