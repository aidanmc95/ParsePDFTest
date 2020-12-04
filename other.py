#!/usr/bin/env python

"""
Use this script to scrape results and demographics from all DiaCarta PDFs in a directory
"""

import sys
import os
import shutil

from pdfminer.high_level import extract_text 

"""Deal with arguments"""
path = './Results'
dirs = os.listdir( path )

for file in dirs:
    file_path = 'Results/' + file
    if not os.path.isdir(file_path):
        pdfFileObj = open(file_path, 'rb')
        pdf_text = extract_text(pdfFileObj)
        print(pdf_text)



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

    #name = match_pdf_text(pdf_text, name_re)
    result = match_pdf_text(pdf_text, result_re)
    #mrn = match_pdf_text(pdf_text, mrn_re)
    req_id = match_pdf_text(pdf_text, req_re)

    # dob = match_pdf_text(pdf_text, dob_re, True)
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
        #'name': name,
        #'dob': dob,
        'result': result,
        #'mrn': mrn,
        #'collected': collected,
        #'received': received,
        #'reported': reported,
        'req_id': req_id,
    }

reqs = []
with open(reqs_fp, 'r') as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        reqs.append(row['req_id'])
    f.close()

output_lines = []
for req in reqs:
    pdf_fp = os.path.join(pdf_dir, "{}.pdf".format(req))
    if os.path.exists(pdf_fp):
        this_dict = get_data_from_pdf(pdf_fp)
        this_dict['file'] = pdf_fp
        output_lines.append(this_dict)
    else:
        sys.stderr.write("No file: {}\n".format(pdf_fp))


with open(output_fp, 'w') as f:
    writer = csv.DictWriter(
        f,
        delimiter="\t",
        fieldnames=output_lines[0].keys()
    )
    writer.writeheader()
    for line in output_lines:
        writer.writerow(line)
    f.close()

sys.stdout.write("Done\n")
