# LXX Project

To generate `lxx.db`, simply run:

    python3 main.py

---

This python script transforms plain text lxx files retreived from <http://ccat.sas.upenn.edu> into a sqlite3 database. See [here](http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/) for the files.

The resulting database (`lxx.db`) stores book, verse, and word number attributes as well as root and morphological data in the format:

id|book name|ch|v|w|word|root|morphology
---|---|---|---|---|---|---|---
183022|Exod|1|1|1|ταῦτα|οὗτος|RD NPN
183023|Exod|1|1|2|τὰ|ὁ|RA NPN
183024|Exod|1|1|3|ὀνόματα|ὄνομα|N3M NPN
183025|Exod|1|1|4|τῶν|ὁ|RA GPM
183026|Exod|1|1|5|υἱῶν|υἱός|N2 GPM
183027|Exod|1|1|6|Ισραηλ|Ἰσραήλ|N GSM
183028|Exod|1|1|7|τῶν|ὁ|RA GPM
183029|Exod|1|1|8|εἰσπεπορευμένων|πορεύομαι εἰς|VX XPPGPM
183030|Exod|1|1|9|εἰς|εἰς|P
183031|Exod|1|1|10|Αἴγυπτον|Αἴγυπτος|N2 ASF
