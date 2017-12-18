"""
Δεδομένα τα οποία χρησιμοποιούνται στα ίδια τα έργα για κατηγοριοποίηση ( ως πληροφορία ) ή για αναζήτηση στα API calls.

Το έγγραφο δημιουργήθηκε ώστε να λειτουργεί ως αρχείο δεδομένων στο οποίο υπάρχουν με διαφορετικούς τρόπους δομημένα,
τα παρακάτω δεδομένα:
    - όλες οι περιφερειακές ενότητες της Ελλάδος,
    - όλοι οι δήμοι τις Ελλάδος που ανήκουν σε κάποια περιφερειακή ενότητα.

[1] Στο λεξικό "short_regions", κάποιος μπορεί να αναζητήσει την περιφερειακή ενότητα με βάση τη συντομογραφία της.
[2] Στο λεξικό "reverse_short_regions", κάποιος μπορεί να βρει από το όνομα της περιφερειακής ενότητας ( ολογράφως ) την συντομογραφία του.
[3] Στο λεξικό "regions", κάποιος μπορεί να αναζητήσει με το αγγλικό όνομα της περιφερειακής ενότητας και να βρει το αντίστοιχο ελληνικό.
[4] Στο λεξικό "municipality", κάποιος μπορεί να αναζητήσει το όνομα της περιφερειακής ενότητας και να πάρει όλους τους δήμους της.

References :
https://github.com/YourDataStories/components-visualisation/blob/master/demo/js/components/dashboard/region-selector-gr.js#L63
"""

__author__      = 'Tas-sos'
__maintainer__  = 'Tas-sos'
__email__       = 'tas-sos@g-lts.info'
__copyright__   = 'GNU General Public License v3.0'
__version__     = '1'




short_regions = {
    'GR.MT': 'Anatoliki Makedonia kai Thraki',
    'GR.AT': 'Attiki',
    'GR.AN': 'Voreio Aigaio',
    'GR.GW': 'Dytiki Ellada',
    'GR.MW': 'Dytiki Makedonia',
    'GR.EP': 'Ipeiros',
    'GR.TS': 'Thessalia',
    'GR.II': 'Ionioi Nisoi',
    'GR.MC': 'Kentriki Makedonia',
    'GR.CR': 'Kriti',
    'GR.AS': 'Notio Aigaio',
    'GR.PP': 'Peloponnisos',
    'GR.GC': 'Sterea Ellada',
    'GR.MA': 'Ayion Oros',
}




reverse_short_regions = {
    'Anatoliki Makedonia kai Thraki':	'GR.MT',
    'Attiki':	                        'GR.AT',
    'Voreio Aigaio':	                'GR.AN',
    'Dytiki Ellada':	                'GR.GW',
    'Dytiki Makedonia':	                'GR.MW',
    'Ipeiros':	                        'GR.EP',
    'Thessalia':	                    'GR.TS',
    'Ionioi Nisoi':	                    'GR.II',
    'Kentriki Makedonia':	            'GR.MC',
    'Kriti':	                        'GR.CR',
    'Notio Aigaio':	                    'GR.AS',
    'Peloponnisos':	                    'GR.PP',
    'Sterea Ellada':	                'GR.GC',
    'Ayion Oros':	                    'GR.MA',
}




regions = {
    'Anatoliki Makedonia kai Thraki': 'Ανατολική Μακεδονία & Θράκη',
    'Attiki'                        : 'Αττική',
    'Voreio Aigaio'					: 'Βόρειο Αιγαίο',
    'Dytiki Ellada'					: 'Δυτική Ελλάδα',
    'Dytiki Makedonia'				: 'Δυτική Μακεδονία',
    'Ipeiros'						: 'Ήπειρος',
    'Thessalia'						: 'Θεσσαλία',
    'Ionioi Nisoi'					: 'Ιόνιοι Νήσοι',
    'Kentriki Makedonia'			: 'Κεντρική Μακεδονία',
    'Kriti'							: 'Κρήτη',
    'Notio Aigaio'					: 'Νότιο Αιγαίο',
    'Peloponnisos'					: 'Πελοπόννησος',
    'Sterea Ellada'					: 'Στερεά Ελλάδα',
    'Ayion Oros'					: 'Άγιο Όρος'
}




municipality = {
    'Anatoliki Makedonia kai Thraki': {
        'N. DRAMAS': 'Ν. Δράμας',
        'N. EVROU': 'Ν. Έβρου',
        'N. KAVALAS': 'Ν. Καβάλας',
        'N. XANTHIS': 'Ν. Ξάνθης',
        'N. RODOPIS': 'Ν. Ροδόπης'
    },
    'Attiki': {
        'N. PIREOS KE NISON': 'Ν. Πειραιώς και Νήσων',
        'N. ANATOLIKIS ATTIKIS': 'Ν. Ανατολικής Αττικής',
        'N. DYTIKIS ATTIKIS': 'Ν. Δυτικής Αττικής',
        'N. ATHINON': 'Ν. Αθηνών'
    },
    'Voreio Aigaio': {
        'N. CHIOU': 'Ν. Χίου',
        'N. SAMOU': 'Ν. Σάμου',
        'N. LESVOU': 'Ν. Λέσβου'
    },
    'Dytiki Ellada': {
        'N. ACHAIAS': 'Ν. Αχαΐας',
        'N. ETOLOAKARNANIAS': 'Ν. Αιτωλοακαρνανίας',
        'N. ILIAS': 'Ν. Ηλείας'
    },
    'Dytiki Makedonia': {
        'N. FLORINAS': 'Ν. Φλώρινας',
        'N. GREVENON': 'Ν. Γρεβενών',
        'N. KASTORIAS': 'Ν. Καστοριάς',
        'N. KOZANIS': 'Ν. Κοζάνης'
    },
    'Ipeiros': {
        'N. ARTAS': 'Ν. Άρτας',
        'N. IOANNINON': 'Ν. Ιωαννίνων',
        'N. PREVEZAS': 'Ν. Πρέβεζας',
        'N. THESPROTIAS': 'Ν. Θεσπρωτίας'
    },
    'Thessalia': {
        'N. MAGNISIAS': ' Ν. Μαγνησίας',
        'N. KARDITSAS': ' Ν. Καρδίτσας',
        'N. LARISAS': ' Ν. Λάρισας',
        'N. TRIKALON': ' Ν. Τρικάλων'
    },
    'Ionioi Nisoi': {
        'N. KERKYRAS': 'Ν. Κέρκυρας',
        'N. KEFALLONIAS': 'Ν. Κεφαλληνίας',
        'N. LEFKADAS': 'Ν. Λευκάδας',
        'N. ZAKYNTHOU': 'Ν. Ζακύνθου'
    },
    'Kentriki Makedonia': {
        'N. IMATHIAS': 'Ν. Ημαθίας',
        'N. THESSALONIKIS': 'Ν. Θεσσαλονίκης',
        'N. KILKIS': 'Ν. Κιλκίς',
        'N. PELLAS': 'Ν. Πέλλας',
        'N. PIERIAS': 'Ν. Πιερίας',
        'N. SERRON': 'Ν. Σερρών ',
        'N. CHALKIDIKIS': 'Ν. Χαλκιδικής'
    },
    'Kriti': {
        'N. CHANION': 'Ν. Χανίων',
        'N. IRAKLIOU': 'Ν. Ηρακλείου',
        'N. LASITHIOU': 'Ν. Λασιθίου',
        'N. RETHYMNOU': 'Ν. Ρεθύμνης'
    },
    'Notio Aigaio': {
        'N. KYKLADON': 'Ν. Κυκλάδων',
        'N. DODEKANISON': 'Ν. Δωδεκανήσου'
    },
    'Peloponnisos': {
        'N. ARKADIAS': 'Ν. Αρκαδίας',
        'N. ARGOLIDAS': 'Ν. Αργολίδας',
        'N. KORINTHOU': 'Ν. Κορινθίας',
        'N. LAKONIAS': 'Ν. Λακωνίας',
        'N. MESSINIAS': 'Ν. Μεσσηνίας'
    },
    'Sterea Ellada': {
        'N. VIOTIAS': 'Ν. Βοιωτίας',
        'N. EVVIAS': 'Ν. Εύβοιας',
        'N. EVRYTANIAS': 'Ν. Ευρυτανίας',
        'N. FOKIDAS': 'Ν. Φωκίδας',
        'N. FTHIOTIDAS': 'Ν. Φθιώτιδας'
    },
    'Ayion Oros': {
        'AGIO OROS': 'Άγιο Όρος'
    }
}



