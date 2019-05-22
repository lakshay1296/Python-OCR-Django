# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from .models import FileName
from .source import utils as UT
import os
import re
import sys

# Set default encoding to 'UTF-8'
reload(sys)
sys.setdefaultencoding('utf-8')

''' GLOBAL REGEX PATTERNS: '''
# Regex for detecting if a single file is selected or a directory.
singleFile = r'[/\\](.*)[/\\].(?:(png))'
# For checking a valid directory.
validDirec = r'[A-Za-z]:[/\\](.*)'

# Main Home Page
def index(request):
    file_name = FileName.objects.all()
    context = {'file_name': file_name}
    return render(request, "index/index.html", context)

# Experimental
def details(request, album_id):
    return HttpResponse('<h1> The entered Id is: ' + album_id + '</h1>')

# PNG_OCR Page
def home(request):
    file_name = FileName.objects.all()
    context = {'file_name': file_name}
    return render(request, "home/home.html", context)

# Getting file path for processing the PNG
def ocr_file_path(request):

    # Getting Value of file path
    file_path = request.POST.get('fname')
    print (str(file_path))

    # Starting of OCR Code.
    # Pattern for checking if a file path is is being uploaded or folder path.
    #matchObj = re.search(singleFile, file_path, re.I|re.M)

    if str(file_path).endswith(".png"):
        # Single Files
        process = path_exception_handling(file_path)
        output = process[0]
        emptyField = process[1]
        alert = "Fully Executed"

    elif (str(file_path).endswith("\\")) or (str(file_path).endswith("/")):
        # Creating a TXT folder in the parent location as the images.
        folder_path = str(os.path.abspath(os.path.join(file_path, os.pardir))) + "\\TXT"
        print "Folder Path:" + folder_path
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            print "Folder Already Exists."

        # # Multiple Files
        # for root, dir, files in os.walk(file_path):
        #     for single_image in files:
        #         image_path = os.path.join(root, single_image)
        # process = multi_path_exception_handling(file_path, image_path, folder_path, single_image)
        process = multi_path_exception_handling(file_path, folder_path)
        output = process[0]
        emptyField = process[1]
        print output
        alert = "Fully Executed"

    else:
        output = "Not Valid Path"
        emptyField = "Not Valid Path"
        alert = "Not Executed"

    print (alert)

    context = {'file_path': file_path,
               'output' : output,
               'alert' : alert,
               'error' : emptyField}

    return render(request, "home/home.html", context)

# PDF_to_Image Home Screen
def pdf_home(request):
    file_name = FileName.objects.all()
    context = {'file_name': file_name}
    return render(request, "pdf_home/pdf_home.html", context)

# Getting file path for processing the PDF
def pdf_file_path(request):

    # Getting Value of file path
    file_path = request.POST.get('fname')
    print (file_path)

    if str(file_path).endswith(".pdf"):
        # For conversion of single file
        process = pdf_exception_handling(file_path)
        output = process[0]
        emptyField = process[1]

    else:
        # For multiple PDF files
        for root, dir, files in os.walk(file_path):
            for single_pdf in files:
                if single_pdf.endswith(".pdf"):
                    single_pdf_path = file_path + "\\" + single_pdf
                    process = pdf_exception_handling(single_pdf_path)
                    output = process[0]
                    emptyField = process[1]

    alert = "Fully Executed"
    print (alert)

    context = {'file_path': file_path,
               'output' : output,
               'alert' : alert,
               'error' : emptyField}

    return render(request, "pdf_home/pdf_home.html", context)

# Handles exception occurred in single_file_path
def path_exception_handling(file_path):
    try:
        output = UT.single_file_tesseract(file_path)
        emptyField = "Fully Executed"
    except Exception as e:

        # Check if path is empty or directory is invalid.
        pathObj = re.search(validDirec, file_path, re.I | re.M)
        if file_path == "":
            emptyField = "Enter Path!"
            output = "Enter Path"

        elif not pathObj:
            emptyField = "Not Valid Path"
            output = "Not Valid Path"

        else:
            emptyField = "Some Error"
            output = e

    return output, emptyField

# Handles exception occurred in multi_file_path
# def multi_path_exception_handling(file_path, image_path, folder_path, single_image):
def multi_path_exception_handling(file_path, folder_path):
    try:
        # output = UT.multi_file_tesseract(image_path, folder_path, single_image)
        output = UT.multi_file_tesseract(file_path, folder_path)
        emptyField = "Fully Executed"
    except Exception as e:

        # Check if path is empty or directory is invalid.
        pathObj = re.search(validDirec, file_path, re.I | re.M)
        if file_path == "":
            emptyField = "Enter Path!"
            output = "Enter Path"

        elif not pathObj:
            emptyField = "Not Valid Path"
            output = "Not Valid Path"

        else:
            emptyField = "Some Error"
            output = e

    return output, emptyField

def pdf_exception_handling(file_path):
    try:
        output = UT.pdf_to_image(file_path)
        emptyField = "Fully Executed"
    except Exception as e:

        # Check if path is empty or directory is invalid.
        pathObj = re.search(validDirec, file_path, re.I | re.M)
        if file_path == "":
            emptyField = "Enter Path!"
            output = "Enter Path"

        elif not pathObj:
            emptyField = "Not Valid Path"
            output = "Not Valid Path"

        else:
            emptyField = "Some Error"
            output = e

    return output, emptyField