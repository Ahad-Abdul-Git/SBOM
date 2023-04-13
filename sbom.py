import sys
import os
from pathlib import Path
import re
import csv
import json

#Main program function
def main(args):
    
    #Checks if there is only 2 arguments, if not, gives appropriate feedback to user and closes program
    if len(args) < 2:
        sys.exit('Exited program due to too few arguments given in the command line.  Try "py sbom.py [directorypath]".')
    elif len(args) > 2:
        sys.exit('Exited program due to too many arguments given in the command line. Try "py sbom.py [directorypath]".')

    #Turns the path given by the user into a Path object
    p = Path(args[1])

    #Checks if this directory exists, if not, gives appropriate feedback to user and closes program
    if not p.is_dir():
        sys.exit("The directory path given is not a valid one. Try using the absolute path if the problem is consistent.")

    #Hold the amount of repos visited
    amount = 0

    #Regex to find name and version in requirements.txt files
    req_string = re.compile("(.*)==(.*)")
    #Regex to find names and version in package-lock.json files
    lock_string = re.compile("\"(.*?)\": {[\n\s]+\"version\": \"(.*?)[\"]")

    #Hold all the data for the SBOM outprint
    sbom_data = []

    #Visits every new path in the provided path
    for dir in p.iterdir():

        #Checks if the path is a new folder/directory
        if(dir.is_dir()):

            #Iterates through the files in that directory
            for subpath in dir.iterdir():
                
                #Checks if the filename is requirements.txt
                if str(subpath).endswith("\\requirements.txt"):

                    #Uses a regex pattern to find all instances of names and versions
                    results = req_string.findall(subpath.read_text())

                    #For every touple of dependency name and version, add type and absolute path
                    for result in results:
                        row = [result[0], result[1], "pip", os.path.abspath(subpath)]
                        #Appends it to the SBOM data
                        sbom_data.append(row)    

                    #Increments amount of repos visited
                    amount += 1       

                #Checks if the filename is package.json
                elif str(subpath).endswith("\\package.json"):

                    #Opens the JSON file in read mode and brings out the data
                    with open(subpath, 'r') as f:
                        json_bulk = json.load(f)

                    #Container for dependencies and devDependencies
                    json_objects = {}

                    #Makes sure dependencies/devDependencies actually exists, then adds them to the container if they do
                    if("dependencies" in json_bulk):
                        json_objects.update(json_bulk["dependencies"])

                    if("devDependencies" in json_bulk):
                        json_objects.update(json_bulk["devDependencies"])

                    #Iterates through all the dependencies gathered in the container
                    for object in json_objects.items():
                        
                        #For every touple of dependency name and version, add type and absolute path
                        row = [object[0], object[1], "npm", os.path.abspath(subpath)]

                        #Appends it to the SBOM data
                        sbom_data.append(row)
                    
                    #Increments amount of repos visited
                    amount += 1
                    f.close()

                #Checks if the filename is package-lock.json
                elif str(subpath).endswith("\\package-lock.json"):

                    #Uses a regex pattern to find all instances of names and versions
                    results = lock_string.findall(subpath.read_text())

                    #For every touple of dependency name and version, add type and absolute path
                    for result in results:
                        row = [result[0], result[1], "npm", os.path.abspath(subpath)]
                        #Appends it to the SBOM data
                        sbom_data.append(row)    

                    #Increments amount of repos visited
                    amount += 1     


    #If there was no data found, the system will notify the user then exit the program.
    if not sbom_data:
        sys.exit("No data was found for the SBOM in this directory. Check if the path leads to the correct directory.")

    #Informs user of the amount of repos found
    print(f"Found {amount} repositories in '{p}'")

    #Sends data to be written to CSV and JSON files
    writeToCSV(p, sbom_data)
    writeToJSON(p, sbom_data)    

#Writes to CSV file
def writeToCSV(path, data):

    #Make sure to write to the user provided path
    write_path = os.path.join(path, "sbom.csv")

    #Opens a file to write to
    with open(write_path, "w", newline="") as f:

        #Creates an writer for CSV files
        csv_handler = csv.writer(f, delimiter=" ")

        #Writes down the colum names for the file
        csv_handler.writerow(["Name", "Version", "Type", "Abs_path"])

        #Iterates through the rows in the data and writes them to file
        for row in data:
            csv_handler.writerow([row[0], row[1], row[2], row[3]])
    
    #Closes file
    f.close()

    #Notifies user that CSV file has been finished at the provided path
    print(f"Saved SBOM in CSV format to {write_path}")
    
#Writes to JSON file
def writeToJSON(path, data):

    #Make sure to write to the user provided path
    write_path = os.path.join(path, "sbom.json")

    #Opens a file to write to
    with open(write_path, 'w') as f:
        #Dumps data to JSON file, in bulks of 4 variables per bulk
        f.write(json.dumps(data, indent=4))
        
    #Closes file
    f.close()

    #Notifies user that CSV file has been finished at the provided path
    print(f"Saved SBOM in JSON format to {write_path}")

#Runs the main program function with the command line arguments
if __name__ == "__main__":
    main(sys.argv)