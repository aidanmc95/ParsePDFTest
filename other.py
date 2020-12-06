import csv
import datetime
import glob
import os
from pdfminer.high_level import extract_text
import re
import sys

"""Deal with arguments"""
path = './Results'
dirs = os.listdir( path )

"""Deal with arguments"""
pdf_dir = './Results'    # within this file, pdfs named <req_id>.pdf

if not os.path.exists(pdf_dir):
    sys.stderr.write("No directory {}\n".format(pdf_dir))
    exit(1)

result_re = re.compile(r'Result\s+(?P<match>[a-zA-Z ]+)\n')
name_re = re.compile(r'(?!Facility )Name:\s+(?P<match>[a-zA-Z ]+)\s+')
dob_re = re.compile(r'DOB:\s+(?P<match>[\.0-9]+)\s+')
mrn_re = re.compile(r'Medical Record Number:\s+(?P<match>[A-Z]{4}[0-9]{6})\s+')
collected_re = re.compile(r'Date Collected:\s+(?P<match>[\.0-9]+)\s+')
received_re = re.compile(r'Date Received:\s+(?P<match>[\.0-9]+)\s+')
reported_re = re.compile(r'Report Date:\s+(?P<match>[\.0-9]+)\s+')
req_re = re.compile(r'Sample ID:\s+(?P<match>(20A[^0-9A-Za-z][0-9]{5}))\s+')


def format_report_date(date_text):
    output_text = 'NA'
    try:
        date = datetime.datetime.strptime(date_text, "%m.%d.%Y")
        output_text = datetime.datetime.strftime(date, "%m/%d/%Y")
    except:
        pass
    return output_text


def match_pdf_text(text, regex, as_date=False):
    match = regex.search(text)
    output = 'NA'
    if match is not None:
        match_text = match.group('match')
        if as_date:
            output = format_report_date(match_text)
        else:
            output = match_text
    return output


def get_data_from_pdf(pdf_fp):
    pdf_text = extract_text(pdf_fp)
    split_version = list(filter(lambda a: (a != '' and a != ' '), pdf_text.split("\n")))
    print("Name: {}, Req ID: {}, Date Collected: {}, DOB: {}, Result: {}".format(split_version[7], split_version[13], split_version[14], split_version[21], split_version[33]))

    name = match_pdf_text(pdf_text, name_re)
    result = match_pdf_text(pdf_text, result_re)
    #mrn = match_pdf_text(pdf_text, mrn_re)
    req_id = match_pdf_text(pdf_text, req_re)

    dob = match_pdf_text(pdf_text, dob_re, True)
    # collected = match_pdf_text(pdf_text, collected_re, True)
    # received = match_pdf_text(pdf_text, received_re, True)
    # reported = match_pdf_text(pdf_text, reported_re, True)
    
    # sys.stdout.write("{}\t{}\n".format(
    #     pdf_fp,
    #     ",".join([
    #         name, dob, result, mrn, collected, received, reported, req_id
    #     ])
    # ))
    sys.stdout.write("{}\t{}\n".format(
        pdf_fp,
        ",".join([
            result, req_id
        ])
    ))
    return {
        'name': name,
        'dob': dob,
        'result': result,
        #'mrn': mrn,
        #'collected': collected,
        #'received': received,
        #'reported': reported,
        'req_id': req_id,
    }

for file in dirs:
    file_path = 'Results/' + file
    if (not os.path.isdir(file_path) and file.split(".")[-1] == "pdf"):
        this_dict = get_data_from_pdf(file_path)
        print(this_dict)

sys.stdout.write("Done\n")
