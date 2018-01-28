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
* Όλο το έργο είναι γραμμένο με [**Python 3**](https://www.python.org/) και συγκεκριμένα δοκιμασμένο σε **Python 3.5.3**.
* Χρησιμοποιείτε το [**Django 2.0**](https://www.djangoproject.com/).
* Επίσης για την δημιουργία του τελικού εγγράφου αναφοράς PDF, χρησιμοποιείται η [LaTeX](https://www.latex-project.org/).
* Επιπλέον αναγκαίες βιβλιοθήκες :
  * [requests 2.18.4](http://python-requests.org/)
  * [BeautifulSoup4 4.6.0](https://www.crummy.com/software/BeautifulSoup/)
  * [pyGoogleSearch 2.05](https://github.com/mdonnalley/pyGoogleSearch)

-----

### Οδηγίες ενσωμάτωσης και εγκατάστασης της εφαρμογής στον [Apache web server](https://httpd.apache.org/).
* **Εγκατάσταση των απαραίτητων πακέτων για ενσωμάτωση της εφαρμογής.** <br>
  1) Apache & mod_wsgi : <br>
`sudo apt-get install apache2 libapache2-mod-wsgi-py3`

  2) Python 3 virtual enviroment tools : <br>
`sudo apt-get install python3-venv`

  3) LaTeX : <br>
`sudo apt-get install texlive texlive-base texlive-full texlive-lang-greek`


* **Δημιουργία καταλόγου τοποθέτησης της εφαρμογής.**<br>
Επιλέγουμε απλώς ένα μέρος στο σύστημα αρχείων του χρήστη, ώστε να έχουμε την/τις εφαρμογή/ές μας. π.χ.:<br><br>
`mkdir -p webApps/ydsR` <br><br>
`cd webApps/ydsR` <br><br>

* **Μεταφοράς της εφαρμογής μας.**<br>
Μεταφέρουμε με έναν τρόπο την εφαρμογή μας στον κατάλογο που έχουμε αποφασίσει στον διακομιστή μας. Για λόγους ευκολίας, στο παράδειγμα μας κατεβάζουμε όλο το παρών αποθετήριο, το αποσυμπιέζουμε, κρατάμε τον κατάλογο με το Django project και έπειτα διαγράφουμε όσα είναι περιττά : <br><br>
`wget https://github.com/Tas-sos/yds-reports/archive/master.zip && unzip master.zip && mv yds-reports-master/report_app/yds/* . && rm -r master.zip yds-reports-master` <br><br>
Ακολουθώντας λοιπόν την παραπάνω διαδικασία, φτάσαμε λοιπόν σε αυτή την εικόνα της κατάστασης των αρχείων της εφαρμογής στο σύστημα μας :
```bash
webApps/
└── ydsR
    ├── db.sqlite3
    │
    ├── manage.py
    │
    ├── report
    │
    ├── report_api
    │
    ├── requirements.txt
    │
    ├── utilities
    │
    └── yds
        ├── __init__.py
        ├── __pycache__
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

* **Δημιουργία εικονικού περιβάλλοντος ( [*venv*](https://docs.python.org/3/tutorial/venv.html) )  για την εφαρμογή.**<br>
Για να μην υπάρχουν προβλήματα σύγκρουσης πακέτων της Python στο σύστημα μας, δημιουργούμε για την εφαρμογή μας το δικό της εικονικό περιβάλλον python, το οποίο θα χρησιμοποιεί ώστε να τρέχει εντός αυτού. Μέσα σε αυτό το εικονικό περιβάλλον - *και μόνο μέσα σε αυτό* - θα εγκαταστήσουμε έπειτα τα πακέτα που χρειάζεται η εφαρμογή μας για να εκτελεστεί. π.χ. :<br><br>
`python3 -m venv .venv_ydsR` <br><br>
Εμείς επιλέγουμε στο δικό μας παράδειγμα, να μεταβούμε στον κατάλογο όπου έχουμε αποφασίσει πως θα έχουμε την εφαρμογή μας και εντός αυτού να δημιουργήσουμε το εικονικό περιβάλλον για αυτή. Εφόσον το κάνουμε, πλέον στο παράδειγμα μας έχουμε την εξής κατανομή των αρχείων στο σύστημά μας.<br>
Προσέξτε πως πλέον υπάρχει και ο κατάλογος «***.venv_ydsR***», εντός του καταλόγου όπου φιλοξενείται όλη μας η εφαρμογή.
```bash
webApps/
└── ydsR
    ├── db.sqlite3
    │
    ├── manage.py
    │
    ├── report
    │
    ├── report_api
    │
    ├── requirements.txt
    │
    ├── utilities
    │
    ├── .venv_ydsR
    │   ├── bin
    │   ├── include
    │   ├── lib
    │   ├── lib64 -> lib
    │   ├── pip-selfcheck.json
    │   ├── pyvenv.cfg
    │   └── share
    │
    └── yds
```

* **Ενεργοποίηση του εικονικού περιβάλλοντος.** <br><br>
`source .venv_ydsR/bin/activate` <br><br>

* **Εγκατάσταση εντός του εικονικού περιβάλλοντος των απαραίτητων πακέτων της εφαρμογής μας.** <br>
Η εφαρμογή μας για να λειτουργήσει, χρειάζεται τα [απαραίτητα πακέτα/βιβλιοθήκες](https://github.com/Tas-sos/yds-reports#%CE%91%CF%80%CE%B1%CE%B9%CF%84%CE%AE%CF%83%CE%B5%CE%B9%CF%82) της Python που αναφέρονται παραπάνω. Η εγκατάσταση τους είναι πολύ απλή και την έχουμε κάνει ακόμη πιο απλή για εσάς. Το μόνο που χρειάζεται να κάνετε, είναι να εκτελέσετε την παρακάτω εντολή : <br><br>
`pip install -r requirements.txt` <br> <br>


* **Διαχείριση στατικών αρχείων.**<br>
Προς διευκόλυνση του διακομιστή ιστοσελίδων πρέπει να συγκεντρώσουμε όλα στατικά αρχεία σε ένα μέρος. Ευτυχώς για αυτό δεν χρειάζεται να κάνουμε τίποτα παραπάνω από το να τρέξουμε απλώς την παρακάτω απλή εντολή : <br><br>
`python manage.py collectstatic`<br><br>
Πλέον θα παρατηρήσετε πως έχετε αυτή την δομή στον κατάλογο όπου φιλοξενείται η εφαρμογή σας :
```bash
webApps/
└── ydsR
    ├── db.sqlite3
    │
    ├── manage.py
    │
    ├── report
    │
    ├── report_api
    │
    ├── requirements.txt
    │
    ├── static
    │   └── report
    │       ├── css
    │       ├── download
    │       ├── fonts
    │       ├── images
    │       └── js
    │
    ├── utilities
    │
    ├── .venv_ydsR
    │
    └── yds
```

* **Αποσύνδεση από το εικονικό περιβάλλον**<br>
Πλέων δεν χρειάζεται να ήμαστε συνδεδεμένοι στο εικονικό περιβάλλον, οπότε για να εξέλθουμε από αυτό εκτελούμε την παρακάτω εντολή : <br><br>
`deactivate` <br><br>


* **Παραχώρηση δικαιωμάτων.**<br>
Για να τρέχει απροβλημάτιστα η εφαρμογή θα πρέπει να εκχωρηθούν τα αρμόδια δικαιώματα στους καταλόγους της, κυρίως λόγο του γεγονότος πως παράγονται/δημιουργούνται αρχεία PDF.<br> Αρκεί να τρέξουμε την παρακάτω εντολή : <br><br>
`sudo chown www-data -R ~/webApps/ydsR/` <br><br>


* **Ρυθμίσεις παραμετροποίησης στον apache2 web server.** <br>
Ήρθε η ώρα να ρυθμίσουμε τον apache ώστε να μπορεί να σερβίρει την django εφαρμογή μας. <br>
Αντιγραφούμε λοιπόν το βασικό αρχείο ρυθμίσεων σε ένα δικό μας όπου θα αφορά *μονάχα* την εφαρμογή μας : <br> <br>
`cd /etc/apache2/sites-available/` <br><br>
`sudo cp 000-default.conf ydsR.conf`<br><br>
Επεξεργαζόμαστε το αρχείο «ydsR.conf» : <br><br>
`sudo vi ydsR.conf`<br><br>
ώστε να είναι ακριβώς έτσι :<br><br>

```
## Django configurations :
WSGIScriptAlias / /home/user/webApps/ydsR/yds/wsgi.py
WSGIPythonHome /home/user/webApps/ydsR/.venv_ydsR
WSGIPythonPath /home/user/webApps/ydsR/


<VirtualHost *:80>

	DocumentRoot /home/user/webApps/ydsR

	Alias /static/ /home/user/webApps/ydsR/static/

	<Directory /home/user/webApps/ydsR/static/>
		Require all granted
	</Directory>


	<Directory /home/user/webApps/ydsR/yds>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>


	ServerAdmin webmaster@localhost


	ErrorLog ${APACHE_LOG_DIR}/ydsr-error.log
	CustomLog ${APACHE_LOG_DIR}/ydsr-access.log combined

</VirtualHost>
```
> **Προσοχή!** Όπου `/home/user/`, «user» είναι το όνομα και αντίστοιχα ο προσωπικός κατάλογος του χρήστη στον οποιό έχουμε τοποθετήσει την εφαρμογή. Εσάς προφανώς το όνομα του χρήστει θα είναι διαφορετικό. Αλλάξτε λοιπόν απλά το «user» με το όνομα του δικού σας χρήστη.

Αποθηκεύουμε και κλείνουμε το αρχείο.<br>
Έπειτα ενεργοποιούμε το αρχείο ώστε να το λαμβάνει υπόψιν του ο Apache2 web server : <br><br>
`sudo a2ensite ydsR.conf `<br><br>
Επανεκκινούμε τον διακομιστή :<br><br>
`sudo /etc/init.d/apache2 start`<br><br>


-----

### Οδηγίες χρήσης.
Έχουν υλοποιηθεί δύο περιπτώσεις χρήσης :

* Η κλασική χρήση μέσω HTML σελίδων και περιήγησης ως μιας κλασικής Web ιστοσελίδας.
* Η χρήση ως API που επιστρέφει αποτελέσματα σε JSON format.


-----

### Αναφορές : <br>
Η επίσημη ιστοσελίδα του Django project, παρέχει πληροφορίες για την συνεργασία με τον [Apache web server](https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/) καθώς και για τον [nginx web server](https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/uwsgi/).<br>
* [How to use Django with Apache and mod_wsgi.](https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/modwsgi/) <br>
* [How to deploy with WSGI.](https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/)



<!-- Η εφαρμογή αποτελείται από ένα Django Application. -->
