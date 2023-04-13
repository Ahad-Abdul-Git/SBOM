# SBOM - Command line tool

Simple command line tool which gathers dependencies from the repos in a given path and saves them to a CSV and JSON file respectively.

## Usage instructions:

You can run this program by opening a terminal and navigating to the directory it has been put in.

To run the file, write "py sbom.py [directorypath]" in the terminal to run it.
Instead of writing "py" you can also write "python".
The directory path should be to the folder which contains the code repositories.

## Assumptions/notes:

I will let the testfiles/folders used during development stay, in case of interest or perspective.

I assumed for this task that the files will not contain any writing errors, and that they all follow the same format of writing.

Since there was no example for the package-lock.json, i found an example online and based my solution for the reading and processing of the data of that example.
Example was found here:
https://chromium.googlesource.com/external/github.com/grpc/grpc/+/HEAD/examples/node/package-lock.json

## Issues / Bugs

Currently, there is no known bug or issue with the program.

But if the files being read are not formatted correctly, the program might not work as intended.

## Ideas for other features

It might have been a useful feature if the user was able to chose to sort the data by any of the columns before they were written out. 

Another possibility could be to make it a bit more interactive than just running the file. Like not terminating but instead letting the user try again, giving options to chose what type of columns they would like, if they should be sorted, etc.
All this provided in a menu type fashion which you can navigate back and forth in.


*Code provided by Ahad Abdul.*