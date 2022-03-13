# FileOrganizer

Il notebook contiene:
- uno script Python che itera in ordine alfabetico sui file della cartella files e, a seconda del tipo (audio, documento, immagine), li sposta nella relativa sottocartella di riferimento.
- uno script Python che itera i files presenti nella sottocartella images e costruisce una tabella riassuntiva (prodotta con la libreria tabulate) che riporta varie info.

Il programma addfile.py (eseguibile da cmd) sposta un singolo file (che si trova nella cartella files) nella sottocartella di competenza, aggiornando il file recap.csv
L'interfaccia dell'eseguibile ha come unico argomento (obbligatorio) il nome del file da spostare (comprensivo di formato, es: 'trump.jpeg'). 
