from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, Http404
from django.core.files.storage import FileSystemStorage

from utilities.data_set import regions, municipality
from utilities.project import get_projects_by_municipality, get_project_data, search, generate_pdf, pdf_name



def all_regions(request):
    """
    Επιστροφή όλων των περιφερειών.

    Όταν κάποιος αιτηθεί το εξής ερώτημα : "/api" τότε εκτελείται αυτό το view που σκοπό έχει να εμφανίσει όλες τις
    διαθέσιμες περιφερειακές ενότητες.
    :param request: Το URL request.
    :return: Επιστρέφει σε JSON μορφή όλες τις περιφερειακές ενότητες της Ελλάδος.
    """

    return JsonResponse(regions,
                        json_dumps_params=dict(sort_keys=True, indent=4, ensure_ascii=False),
                        safe=False)




def all_municipalities(request, a_region):
    """
    Επιστροφή όλων των νομών μιας περιφερειακής ενότητας.

    Όταν κάποιος αιτηθεί το εξής ερώτημα : "/api/Attiki/" τότε εκτελείται αυτό το view που σκοπό έχει να επιστρέψει
    όλους τους δήμους της εκάστοτε περιφερειακής ενότητας.
    :param request: Το URL request.
    :param a_region: Ποια περιφερειακή ενότητα έχει δοθεί ως παράμετρος.
    :return: Επιστρέφει σε JSON μορφή όλους τους νομούς της περιφερειακής ενότητας που δίνεται ως παράμετρος.
    """

    try:
        if regions[a_region]:

            return JsonResponse(municipality[a_region],
                                json_dumps_params=dict(sort_keys=True, indent=4, ensure_ascii=False),
                                safe=False)
    except KeyError:
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




def all_projects(request, a_region, a_municipality):
    """
    Επιστροφή όλων των έργων ενός νομού.

    Όταν κάποιος αιτηθεί το εξής ερώτημα : "/api/Attiki/N. ANATOLIKIS ATTIKIS" τότε εκτελείται αυτό το view που σκοπό
    έχει να επιστρέψει όλα τα δημόσια έργα του εκάστοτε νομού.
    :param request: Το URL request.
    :param a_region: Ποια περιφερειακή ενότητα έχει δοθεί ως παράμετρος.
    :param a_municipality: Ποιος νομός έχει δοθεί ως παράμετρος.
    :return: Επιστρέφει σε JSON μορφή όλα τα δημόσια έργα του νομού που έχει δοθεί ως παράμετρος.
    """

    try:
        if regions[a_region]:  # Αν υπάρχει η περιφέρεια μέσα στις περιφέρειες
            try:
                if municipality[a_region][a_municipality]:  # Αν υπάρχει ο νομός μέσα στη συγκεκριμένη περιφέρεια!

                    projects = get_projects_by_municipality(a_municipality)

                    return JsonResponse(projects,
                                        json_dumps_params=dict(sort_keys=True, indent=4, ensure_ascii=False),
                                        safe=False)
            except KeyError:
                raise Http404("The municipality \"{0}\" was not found it!".format(a_municipality))
    except KeyError:
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




def redirect_to_download_pdf(request, a_region, a_municipality, a_project):
    """
    Αναπροσαρμογή του requested URL και ανακατεύθυνση του στο σωστό view.

    Όταν κάποιος αιτηθεί το εξής ερώτημα :
    "/api/Attiki/N. ANATOLIKIS ATTIKIS/http://linkedeconomy.org/resource/PublicWork/525244"
    
    τότε εκτελείται αυτό το view που έχει ως σκοπό απλώς να διορθώσει το URL ώστε να το κάνει :
    "/api/Attiki/N. ANATOLIKIS ATTIKIS/525244"
    
    και έτσι να απευθυνθεί στο αρμόδιο view.
    :param request: Το URL request.
    :param a_region: Ποια περιφερειακή ενότητα έχει δοθεί ως παράμετρος.
    :param a_municipality: Ποιος νομός έχει δοθεί ως παράμετρος.
    :param a_project: Ένα δημόσιο έργο της μορφής "http://linkedeconomy.org/resource/PublicWork/448352".
    :return: Αναπροσαρμόζει το requested URL ώστε να περιέχει μονάχα το id του έργου και το ανακατευθύνει στο σωστό view.
    """

    if not str(a_project).startswith("http://linkedeconomy.org/resource/PublicWork/"):
        raise Http404("You haven't set a \"linkedeconomy.org\" link, for example : \"http://linkedeconomy.org/resource/PublicWork/443856/\".")

    return redirect('report_api:download_pdf', a_region=a_region,
                                               a_municipality=a_municipality,
                                               a_project=int(a_project.split('/')[5]) )




def download_pdf(request, a_region, a_municipality, a_project):
    """
    Δημιουργία εγγράφου αναφοράς σε μορφή PDF.

    Όταν κάποιος αιτηθεί το εξής ερώτημα : "/api/Attiki/N. ANATOLIKIS ATTIKIS/525244" τότε εκτελείται αυτό το view και
    σκοπό έχει να παράξει ένα έγγραφο αναφοράς σε μορφή PDF για αυτό το έργο και έπειτα να το δώσει για κατέβασμα στον
    χρήστη.
    :param request: Το URL request.
    :param a_region: Ποια περιφερειακή ενότητα έχει δοθεί ως παράμετρος.
    :param a_municipality: Ποιος νομός έχει δοθεί ως παράμετρος.
    :param a_project: Ένα δημόσιο έργο της μορφής "448352".
    :return: Δημιουργεί ένα έγγραφο αναφοράς σε PDF στον διακομιστή και το σερβίρει και στον client σε περίπτωση που
    θέλει να το κατεβάσει.
    """

    a_project = "http://linkedeconomy.org/resource/PublicWork/" + str(a_project)

    try:
        if regions[a_region]:  # Αν υπάρχει η περιφέρεια μέσα στις περιφέρειες
            try:
                if municipality[a_region][a_municipality]:  # Αν υπάρχει ο νομός μέσα στη συγκεκριμένη περιφέρεια!

                    projects = get_projects_by_municipality(a_municipality)

                    for name, link in projects.items():
                        if a_project == link:

                            file_name = a_project.split("/")[5] + ".pdf"

                            # Downloading data from this project :
                            project_data = get_project_data(a_project)

                            # Search for related articles for this project :
                            related_articles = search(project_data['title'])

                            # Generating the report PDF for this project:
                            try:
                                generate_pdf(project_data, related_articles,
                                             pdf_name("report/static/report/download/", a_project))
                            except ValueError as log:
                                print("Compiler error from LaTeX, for project : {0}".format(a_project))
                                print('-------------------------------------------------------------------------------------------------------')
                                print('LaTex Log |')
                                print('-----------')
                                print(log)
                                print('-------------------------------------------------------------------------------------------------------')

                                return render(request, 'report/pdf.html', {'project_url': a_project})

                            file_system = FileSystemStorage('report/static/report/download/')
                            with file_system.open(file_name) as pdf:

                                # Create the HttpResponse object with the appropriate PDF headers.
                                response = HttpResponse(pdf, content_type='application/pdf')
                                response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'

                                return response

                    raise Http404("The project \"{0}\" was not found it!".format(a_project))

            except KeyError:
                raise Http404("The municipality \"{0}\" was not found it!".format(a_municipality))
    except KeyError:
        raise Http404("The region \"{0}\" was not found it!".format(a_region))




