#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A LaTeX template for generating dynamically PDF files.

This file contains the LaTeX code for producing the PDF document.
It just replaces the dynamic fields from the project data and related articles.
"""


from os import path


__author__      = 'Tas-sos'
__maintainer__  = 'Tas-sos'
__email__       = 'tas-sos@g-lts.info'
__copyright__   = 'CopyLeft'
__licence__     = 'GNU General Public License v3.0'
__version__     = '1'
__url__         = 'https://github.com/Tas-sos/yds-reports'




def set_latex(project_data, articles):
    """
    Το LaTeX template στο οποίο προστίθενται τα δεδομένα του εκάστοτε έργου.

    Η συνάρτηση αυτή απλώς δημιουργεί τον LaTeX κώδικα για τα εκάστοτε δεδομένα του έργου.
    Προσθέτει στον ήδη υπάρχον LaTeX κώδικα - template τα δεδομένα του έργου.

    TODO: Πρόβλεψη για χαρακτήρες διαφυγής :
    Ίσος υπάρξει πρόβλημα με κάποιο τυχόν περίεργο χαρακτήρα διαφυγής που μπορεί τυχόν να υπάρξει και
    η LaTeX να τα παίξει.

    TODO: Πρόβλεψη για ελληνικούς και αγγλικούς χαρακτήρες στα δυναμικά κείμενα.
    Συμβαίνει κυρίως στις αναζητήσεις των σχετικών άρθρων στη Google πως πολύ τίτλοι εμπεριέχουν και αγγλικούς χαρακτήρες
    με αποτέλεσμα η LaTeX να τους μετατρέπει σε ελληνικούς και να μην βγαίνει εύκολα νόημα. Το ίδιος όμως μπορεί να
    συμβεί και σε οποιοδήποτε από τα επιμέρους δυναμικά κείμενα των δεδομένων του έργου. Θα πρέπει ίσος να ερευνηθεί αν
    γίνεται να υποστηριχθεί μέσω της LaTeΧ η δυναμική αναγνώριση των ελληνικών και αγγλικών χαρακτήρων ώστε να
    αποτυπώνονται σωστά στο τελικό έγγραφο.

    ΠΡΟΣΟΧΗ! : Αν υπάρχουν κενά μεταξύ των φακέλων ίσος υπάρχει πρόβλημα στο compile της LaTeX κυρίως λόγο των
    εικόνων που υπάρχουν και προστίθενται στο έγγραφο.

    :param project_data: Τα δεδομένα του εκάστοτε έργου εντός λεξικού.
    :param articles: Τα σχετικά με το έργο άρθρα, που βρέθηκαν στο διαδίκτυο.
    :return: Τον πλήρες LaTeX κώδικα εμπλουτισμένο με τα δεδομένα του εκάστοτε έργου.
    """


    images_path = path.dirname(__file__) + "/images/"

    LaTeX_special_characters = [ ('&', '\&'),
                                 ('\n\n', '\\\\~\\\\'),         # Two new lines.
                                 ('\n', '\\newline '),          # New line character.
                                 ("_", "\\textunderscore"),     # Underscore.
                                 ('%', '\\%'),                  # Percent symbol.
                                 ('.0', '')			# For amounts (because they are converted from float to string).
                                 ]

    # Convert to string :
    project_data['budget']                  = str(project_data['budget'])
    project_data['spending']                = str(project_data['spending'])
    project_data['completion_of_payments']  = str(project_data['completion_of_payments'])
    project_data['completion_of_contracts'] = str(project_data['completion_of_contracts'])


    # Avoid special characters :
    for k, v in LaTeX_special_characters:
        project_data['title']                   = project_data['title'].replace(k, v)
        project_data['region']                  = project_data['region'].replace(k, v)
        project_data['buyer_name']              = project_data['buyer_name'].replace(k, v)
        project_data['budget']                  = project_data['budget'].replace(k, v)
        project_data['spending']                = project_data['spending'].replace(k, v)
        project_data['completion_of_payments']  = project_data['completion_of_payments'].replace(k, v)
        project_data['completion_of_contracts'] = project_data['completion_of_contracts'].replace(k, v)
        project_data['description']             = project_data['description'].replace(k, v)


    latex = r"""\documentclass[12pt,a4paper]{report}
    \usepackage[a4paper, total={7in, 9in}]{geometry}
    \usepackage{graphicx}
    \usepackage[utf8x]{inputenc}
    \usepackage[greek,english]{babel}
    \usepackage{xcolor}
    
    \definecolor{myCyan}{RGB}{0,140, 193}
    \definecolor{myRed}{RGB}{175, 0, 0}
    
    \usepackage{hyperref}
    \hypersetup{
        colorlinks=true,
        linkcolor=blue,
        filecolor=magenta,
        urlcolor=myCyan,
    }
    
    \graphicspath{{""" + images_path + r"""}}
    \newcommand{\changeurlcolor}[1]{\hypersetup{urlcolor=#1}}
    \newcommand{\en}{\selectlanguage{english}}
    \newcommand{\gr}{\selectlanguage{greek}}
    
    \begin{document}
    
    \begin{titlepage}
    \centering
    
    \begin{figure}[!htb]
    \begin{minipage}{0.48\textwidth}
    \centering
    \href{https://diavgeia.gov.gr/}{\includegraphics[width=.8\linewidth]{diavgeia-logo}}
    \end{minipage}\hfill
    \begin {minipage}{0.48\textwidth}
    \centering
    \href{http://platform.yourdatastories.eu/}{\includegraphics[width=.6\linewidth]{yds-logo}}
    \end{minipage}
    \end{figure}
    
    {\scshape\LARGE \href{""" + project_data['id_URL'] + r"""}{\gr{""" + project_data['title'] + r"""}} \par}
    \vspace{0.7cm}
    
    {\Large \gr Περιφερειακή ενότητα : \textbf{""" + project_data['region'] + r"""}}
    \vspace{0.5cm}
    
    {\Large\bfseries \gr Αγοραστής : \par}
    {\Large \changeurlcolor{myRed}\href{""" + project_data['buyer_id_URL'] + r"""}{\gr """ + project_data['buyer_name'] + r"""}}\\
    \footnotesize{\gr Α.Φ.Μ. : """ + project_data['bayer_VAT'] + r"""}
    \vspace{0.5cm}
    
    {\large \gr Προϋπολογισμός έργου : \textbf{""" + project_data['budget'] + r""" \euro} \par}
    {\large \gr Συνολική δαπάνη : \textbf{""" + project_data['spending'] + r""" \euro} \par}
    \vspace{0.2cm}

    {\large \gr Ημερομηνία έναρξης : """ + project_data['start_date'][:10] + r""" \par}
    {\large \gr Ημερομηνία λήξης : """ + project_data['end_date'][:10] + r""" \par}
    \vspace{0.4cm}
    
    {\Large {\gr Ολοκλήρωση πληρωμών έργου : \textbf{""" + project_data['completion_of_payments'] + r"""\%}} \par}
    {\Large {\gr Ολοκλήρωση συμβάσεων έργου : \textbf{""" + project_data['completion_of_contracts'] + r"""\%}} \par}
    \vspace{0.4cm}
    
    
    {\Large\itshape {\gr Περιγραφή :}\par}
    \raggedright
    {\normalsize {\gr """ + project_data['description'] + r"""}\par}\vspace{0.5cm}
    
    \end{titlepage}

    \section*{\gr Σχετικές δημοσιεύσεις στο διαδίκτυο\let\thefootnote\relax\footnote{Οι δημοσιεύσεις προέρχονται έπειτα από αναζήτηση στην μηχανή αναζήτησης {\en \changeurlcolor{myRed}\href{https://www.google.com/}{Google}.}}. :}
    \begin{itemize}"""
    for article_title, article_link in articles.items():
        latex += """\item \changeurlcolor{blue}\href{""" + article_link + """}{\gr """
        for k, v in LaTeX_special_characters:
            article_title = article_title.replace(k, v)
        latex += article_title + """}"""
    latex += r"""\end{itemize}
    
    \centering
    \vfill
    \scriptsize{generated by\par
    \textsc{yourdatastories.eu}}
    
    {\footnotesize \today\par}
    
    \end{document}"""

    return latex




