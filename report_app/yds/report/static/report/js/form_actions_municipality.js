$(document).ready(
    function ()
    {

        /**
         * Κάθε φορά που πατάει και επιλέγει μια επιλογή από το drop-down μενού των δήμων, αλλάζω και το που θα
         * υποβάλει την σελίδα. ;) Αλλάζω το action της φόρμας.
         * Αυτό το κάνω για μια ομαλοποιημένη δομή της σελίδας, είτε απλώς χρησιμοποιώντας την κάποιος σαν API , είτε
         * επιλέγοντας τις επιλογές μέσω browser.
         *
         * Προσοχή : Εξαιτίας αυτούς, απαιτώ για τον χρήστη που θα συνδεθεί μέσω web browser να τρέχει JavaScript!
         *
         */

        $("#selected_municipality").click(
            function ()
            {
                $('#municipality_form').attr('action', $("#selected_municipality").val() + '/' );

            });

    }
);
