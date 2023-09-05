### run each script listed below in that order

# run dbf_extract.py - pulls all the data out of the original BRAHMS tables
# go through extracted files and remove any not needed
# set up fields in dbdiagram.io, then download the sql file to create the database
# run extract_fields.py - creates the mysql database and then extracts the desired fields from the csvs created above
# check FK values all match up in OpenRefine (manual step), and export results to a new folder
# run load_data.py to upload the data from OpenRefine into the database. 
# run extract_data.py to extract the data again as a single file for cleaning in OpenRefine
# the file above only includes the current identification for each specimen. Historical identifications still need to be extracted
# Run the extract for historical identifications, using extract_data.py again but with different params
