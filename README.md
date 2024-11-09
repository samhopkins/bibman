# bibman
This is a simple bibfile manager integrating google scholar for searching and DBLP for retrieving bibtex information.

Interaction with DBLP is handled by import_dblp, a nice command-line utility available here: https://github.com/scholrly/dblp-python

Requirements:
must install import_dblp -- follow installation instructions in link above

Behavior:
Run
    bibman "your search query here"

This will search google scholar and let you select a paper title.
This paper title is passed on to import_dblp, which checks if the bib file in your current directory already contains this paper.
If so, the bibkey is copied to your clipboard.
If not, the bibtex for this paper is fetched from DBLP and added to your bibfile, and then the bib key is copied to your clipboard.


### TODO
the interactive chooser isn't very robust.
if it can't fit its output in the current terminal it tends to fail with an error.
should make this more robust.

also, if the bib is already available, we don't always get the citation key copied.
should make this more robust



### Things which didn't work

Don't try to get bibtex from google scholar. Scholar is very picky about bots.
The python 'scholarly' package consistently gets blocked by google.
