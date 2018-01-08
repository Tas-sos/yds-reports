## Δημιουργία εγγράφων αναφοράς ενός δημόσιου έργου.
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![django2.0](https://img.shields.io/badge/Django-2.0-green.svg)](https://docs.djangoproject.com/en/2.0/releases/)
[![python3.5.3](https://img.shields.io/badge/Python-3.5.3-blue.svg)](https://www.python.org/downloads/release/python-353/)
[![coverage-80%](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/Tas-sos/yds-reports)

> Η παρούσα εφαρμογή προτάθηκε στα πλαίσια του [YDS Hackathon in Athens](https://yourdatastories.eu/features/hackathons/yds-hackathon-athens/).

<p align="center">
<a href="http://platform.yourdatastories.eu/"><img src="https://yourdatastories.eu/wp-content/uploads/2016/01/YDS_Logo_SiteKopie.png" alt="YourDataStories"></a>
<br/> <br/>
<a href="https://www.diavgeia.gov.gr/"><img src="https://www.diavgeia.gov.gr/img/diavgeia_all_logo.png" alt="Diavgeia"></a>
<br/>
</p>

Ο κύριος σκοπός της εφαρμογής είναι να παρέχει στον τελικό χρήστη ένα εύχρηστο περιβάλλον από το οποίο θα μπορεί να αναζητεί δημόσια έργα και επιλέγοντας κάποιο, να του εμφανίζεται ένα έγγραφο αναφοράς PDF, με τις βασικές πληροφορίες του έργου.

Η εφαρμογή βασίζεται στα εύχρηστα προσφερόμενα API του [YourDataStories.eu](platform.yourdatastories.eu/) και τα δεδομένα που αντλούν από την [Διαύγεια](https://www.diavgeia.gov.gr/).

-----

### Απαιτήσεις.
* Όλο το έργο είναι γραμμένο με **Python 3** και συγκεκριμένα δοκιμασμένο σε **Python 3.5.3**.
* Χρησιμοποιείτε το **Django 2.0**.
* Επιπλέον αναγκαίες βιβλιοθήκες :
  * [requests 2.18.4](http://python-requests.org/)
  * [BeautifulSoup4 4.6.0](https://www.crummy.com/software/BeautifulSoup/)
  * [pyGoogleSearch 2.05](https://github.com/mdonnalley/pyGoogleSearch)

Όλο το έργο το τρέχαμε σε ένα απομονωμένο εικονικό περιβάλλον ( [*venv*](https://docs.python.org/3/tutorial/venv.html) ).


### Οδηγίες εγκατάστασης.
* Για δοκιμές :
  * Δημιουργία εικονικού περιβάλλοντος :
```bash
python3 -m venv a_tutorial-env_directory
```
  * Εφόσον ενεργοποιήσετε το εικονικό περιβάλλον, τότε εγκαθιστάτε τα [απαραίτητα πακέτα](https://github.com/Tas-sos/yds-reports#%CE%91%CF%80%CE%B1%CE%B9%CF%84%CE%AE%CF%83%CE%B5%CE%B9%CF%82) με την χρήση του εργαλείου pip. π.χ. για την εγκατάσταση της [τελευταίας έκδοσης του Django](https://www.djangoproject.com/download/) :
  ```bash
  pip install Django==2.0.0
  ```

* Εγκατάσταση σε ένα διακομιστή ιστού παραγωγής : <br>
Η επίσημη ιστοσελίδα του Django project, παρέχει πληροφορίες για την συνεργασία με τον [Apache web server](https://docs.djangoproject.com/el/2.0/howto/deployment/wsgi/) καθώς και για τον [nginx web server](https://docs.djangoproject.com/el/2.0/howto/deployment/wsgi/uwsgi/).

### Οδηγίες χρήσης.
Έχουν υλοποιηθεί δύο περιπτώσεις χρήσης :

* Η κλασική χρήση μέσω HTML σελίδων και περιήγησης ως μιας κλασικής Web ιστοσελίδας.
* Η χρήση ως API που επιστρέφει αποτελέσματα σε JSON format.



<!-- Η εφαρμογή αποτελείται από ένα Django Application. -->

