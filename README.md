




To use this software, after performing a pip install, you must perform two steps:

from python import x_download
from python import z_begin

These will both download files and also create new ones.  As an example of this codes functionality we repunctuate the LASLA database of the Satyricon into a punctuated text with macrons, accents and elision.

The z_begin method takes roughly 20 minutes to complete.  This software merges several Latin databases into one.  These databases are:

1. COLLATINUS

found here:

https://github.com/biblissima/collatinus/tree/Daemon

And on the web here:

https://outils.biblissima.fr/en/collatinus-web/



2. LASLA or OPERA LATINA

found here:

http://cipl93.philo.ulg.ac.be/operalatina/



3. PEDECERTO

found here:

https://www.pedecerto.eu/public/

Only about 75% of this database is currently being used.



4. OXFORD LATIN DICTIONARY

Due to copyright restrictions only a list of words found in the Oxford Latin Dictionary is available.  We also use the vowel quantity and the known spelling variants of these words from the Oxford Latin Dictionary.  No definitions or examples of word usage is available. 

5. The Packhard Humanities Institute Corpus or PHI 

found here:

https://latin.packhum.org/


This project is not yet complete.  Because it is important to see how we get from the separate databases to the new database, the z_begin module will loop through the entire code from the beginning to the end.  In this way, if a mistake has been made, it can be tracked down and more of its kind can be spotted.  This code has several ambitions but certainly one of the most important ambitions is to reconstruct the LASLA database into punctuated text complete with macrons, elision and accent marks.  So far this has been done for Petronius' Satyricon.  Because each text has its quirks these texts mostly have to be examined on an individual basis but with each text the job of restoring them will become easier. 

Our main ambition with the Collatinus database is to restore the vowel length of the words.  The Collatinus database contains the syllable length but not the vowel length.  One major error that I have not yet corrected is that although dictionary authors agree roughly 97% of the time for those syllables which are long or short by nature, and 80% of the time they agree on the vowel quantity for syllables which are long by position, I made the unfortunate decision to not always get the vowel length from the same authors for the perfect stem than I did for the main stem.  So for example, suppose all five authors listed the vowel length for the present stem of "figo".  I would then use the vowel length for the author most in agreement with the Pedecerto database, call him A.  But suppose only two authors listed the vowel length for the perfect stem of "figo" which is "fixo".  Suppose this author was B but B disagrees with A regarding the vowel length of the present stem.  I have not yet corrected this mistake because I'm going to change how I get the vowel length anyway.  In the future I plan to get the vowel length from the Pedecerto database firstly, Oxford Latin Dictionary secondly.

Another major problem we are working on is the third declension.  The third declension turns out to differ widely in practice then as listed in the Collatinus database.  This problem has mostly been solved but I still have not fully integrated all of the changes to the third declension into the new database.  This work is done in the o_memorize module. 

The m_stems module was meant to divide words into their constituent morphemes.  It turns out that the Oxford Latin Dictionary has already done a remarkable job with this.  I have managed to separate a lot of words into their constituent morphemes but much more work remains to be done. 

In the j_lasla module we normalize the LASLA database and in the j_lasla2 we merge the database with the Collatinus database.  Presently roughly 90% of the lemmas in LASLA have been matched to lemmas in Collatinus.  

The v_reading module contains a few classes that are not all that related but it does contain the key class where we put all of our analysis together and produce a text complete with vowel macronization, accent marks and elision.  One of the main problems we encounter when punctuating the LASLA database with a text from PHI is that quite often sentences will be in a different order.  We have figured out a way to fix this problem but have not yet updated the code accordingly.  




