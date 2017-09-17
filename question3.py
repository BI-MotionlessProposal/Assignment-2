import os
import sys
import csv
import platform

## This files prints the (CSV)file name and number of sales (lines - 1) in a given folder
# The output is a CSV file with 'zipcode_file','number_of_sales'
# The last line of the CSV output is a total of  sales#


def get_sales_per_zipcode(path = "data"):
    dirs = os.listdir(path)
    total = 0
    #file_url = 'http://138.197.184.35/boliga' 
    #dirs = os.path.basename(dirs) 
    result = [['zipcode_file','number_of_sales']]
    for csv_file in dirs:
        rl = []

        #print (csv_file)

        csv_path = os.path.join('./'+path, csv_file)
        num_lines = sum(1 for line in open(csv_path))
        rl.append(csv_file)
        rl.append(num_lines-1)
        total += num_lines-1
        
        result.append(rl)
    result.append(['total sales',total])    
    return result


def generate_csv(rows, csv_output_path):

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    with open(csv_output_path, 'w', newline=newline, encoding='utf-8') as f:
        output_writer = csv.writer(f)
        for row in rows:
            output_writer.writerow(row)

def run():
    #Put the name of the output file here
    output_file_name = os.path.basename('result_3_a')
    output_path = os.path.join('./', output_file_name)
    #Put the name of the output file here
    rows = get_sales_per_zipcode('data')
    generate_csv(rows, output_path)
    print('done')



if __name__ == '__main__':
    run()

