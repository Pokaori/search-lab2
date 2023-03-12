
python main.py create-document --name "Self-Portrait at the Age of Twenty Eight" --release-date '1500-12-31' --genres Self-portrait --genres Portrait --cost 1500 --text-path "text_documents/Self-Portrait at the Age of Twenty Eight/"python main.py create-document --name "The Last Judgment" --release-date '1482-12-31' --genres 'Christian art' --cost 2000 --text-path "text_documents/The Last Judgment/"
python main.py create-document --name "The Last Judgment" --release-date '1482-12-31' --genres 'Christian art' --cost 2000 --text-path "text_documents/The Last Judgment/"
python main.py create-document --name "Las Meninas" --release-date '1656-12-31' --genres 'Portrait' --genres 'Genre art' --genres 'History painting' --cost 1200
python main.py add-query release-date-range should 1500-12-31 1600-12-31
python main.py add-query fuzzy should name Portrait