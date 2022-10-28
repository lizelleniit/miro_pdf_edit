import pdf_to_images
import config
import send_to_miro

###########################
###### Configuration ######
###########################

# Set file to send to Miro as images
file = 'Mathematical Thinking sample pages.pdf'

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

#pdf_to_images.pdf2images(file,dpi=dpi)


send_to_miro.send_to_miro(starting_pos, size, space, base_name)