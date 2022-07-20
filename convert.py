# from pdf2image import convert_from_path

# pages = convert_from_path('exemple.pdf',500)

# for page in pages:
    
#     page.save("out.jpg",'JPEG')
    
import os
from pdf2image import convert_from_path

def pdf_to_png(inputPath,fname):
    
    current_directory = os.getcwd()
    os.chdir(r'C:\Users\mpete\OneDrive\Bureau\Projets HESTIM\2eme annee\Innovation_Créativité\test\uploads')
    images = convert_from_path(inputPath, 500,first_page = 1, last_page = 1, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    images[0].save(fname, 'PNG')
    os.chdir(current_directory)    
