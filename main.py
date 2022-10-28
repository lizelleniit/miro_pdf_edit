import pdf_to_images

import send_to_miro

###########################
###### Configuration ######
###########################

# either delete this or create your own config.py file 
import config 

# Set file to send to Miro as images
file = 'Mathematical_Thinking.pdf'

# Set board ID (replace 'config.board_id' with your own details)
board_id = config.board_id

# Set Miro API key (replace 'config.miro_authorisation' with your own details)
miro_authorisation = config.miro_authorisation

# Set base for file names of generated images
base_name = 'page'

# Image resolution. 300 is more or less decent. Too high a resolution results in an error from Miro. 
dpi = 300

# Image and frame size
size = [1000,1414]

# Spacing between successive frames
space = 300

# Where on the board we would like the first page of the report to be. 
starting_pos = [0,2000] 



# Todo: Make a setting to leave existing work on the board and make a fresh copy of the report somewhere else

pdf_to_images.pdf2images(file,dpi=dpi)


send_to_miro.send_to_miro(board_id,miro_authorisation,starting_pos, size, space, base_name)