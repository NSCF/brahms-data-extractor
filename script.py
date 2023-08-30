### run each script listed below in that order

# run dbf_extract.py - pulls all the data out of the original BRAHMS tables
# go through extracted files and set up fields in dbdiagram.io, then download the sql file to create the database
# run extract_fields.py - creates the mysql database and then extracts the desired fields from the csvs created above
# check FK values all match up in OpenRefine (manual step), and export results to a new folder
# run load_data.py to upload the data from OpenRefine into the database. 
# join everything up in the database...
# 
