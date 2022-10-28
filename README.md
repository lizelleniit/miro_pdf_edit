***************
**** INTRO ****
***************

This utility breaks a pdf up into jpg files and places them on a Miro board in frames. One can then overlay content on these images in the Miro GUI and export back to PDF.

***************************
**** DEFAULT BEHAVIOUR ****
***************************

Details about the created frames and images are stored in a file called obj_data.json. When the script is run again later, this file is loaded and used to ensure that existing images are updated as opposed to uploading new images. Later I may create an option to upload new images. 

***************
**** USAGE ****
***************

Edit the settings in main.py and run it to send your PDF to a Miro board. You will need to delete the 'import config' statement*** as well as specify the following: 
* Your PDF file name 
* A Miro board ID board_id
* A Miro API key miro_authorisation 

*** You need to delete the 'import config' statement because that file does not exist in Github. I have hidden my own board_id and miro_authorisation in a hidden file for security reasons.

Unfortunately the export back to pdf has to be done manually because the Miro API does not allow for exports yet. But it can be quickly done from the Miro GUI in the following way:
* Drag a selection box around all the frames. 
* Click the Filter button on the floating toolbar.
* Pick the 'Frame' option.
* Click the three dots on the floating toolbar. 
* Click 'Export to PDF'

This will download a PDF scaled to a random page size. To scale up to A4 size, run the utility pdf_to_a4.py (currently you need to open the .py file to type in the correct file name...I'll sort out the ability to run it with parameters later). 