import os
import csv
import requests
import platform
import statistics
import bs4
import re

def download_txt(url, save_path='./downloaded'):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def html_thead_to_list(table_head):
    l = []
    rows = table_head.find_all('tr')
    for tr in rows:
        lr = []
        cols = tr.find_all('th')
        for c in cols:
            c = c.getText().strip()
            lr.append(c)
        l.append(lr)
    return l

def get_zip_code(str):
    return 'uknown'

def get_sell_date(s):
    s = re.match('([\d-]*)', s, 0)
    s = s.group()
    return s

def html_tbody_to_list(table_body):
    l = []
    rows = table_body.find_all('tr')
    for tr in rows:
        lr = []
        cols = tr.find_all('td')
        for i,c in enumerate(cols):
            c = c.getText().strip()
            if (i == 0):
                zipcode = get_zip_code(c)
                lr.append(c)
                lr.append(zipcode)
            elif(i == 2):

                sell_date = get_sell_date(c)
                sell_type = c.replace(sell_date,'')

                lr.append(sell_date)
                lr.append(sell_type)

            else:
                lr.append(c)
        l.append(lr)
    return l

def html_file_to_csv(html_file):
    base_url = 'http://138.197.184.35/boliga/'
    url = base_url + html_file;
    r = requests.get(url)
    example_html = r.content.decode('utf-8')
    
    rows = html_to_csv_list(example_html)
    )
    
    csv_file = get_csv_filename_from_html(html_file)
    print(csv_file)
    generate_csv(rows, csv_file)

def get_csv_filename_from_html(z):
    z = re.match('[\d-]*', z, 0)
    z = z.group()
    z = z + '.csv'
    return z

def file_to_html(txt_path):
    with open( txt_path ) as f:
        example_html = f.read()
    return example_html

def html_to_csv_list(example_html):

        data = []

        soup = bs4.BeautifulSoup(example_html, 'html5lib')
        table = soup.find('table')
        #if(table.get('id') == 'searchresult'):
            #table_head = table.find('thead')
            #b_list = html_thead_to_list(table_head)
        table_body = table.find('tbody')
        a_list = html_tbody_to_list(table_body)
            #b_list.extend(a_list)
            #print(b_list)
        data = a_list
        return data


def generate_csv(rows, csv_output_path):

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None
    with open(csv_output_path, 'a', newline=newline, encoding='utf-8') as f:
        output_writer = csv.writer(f)
        for row in rows:
            #if(if file exist the skipp the first row)
            output_writer.writerow(row)

def get_zipcsv_from_list(scraped_list):
    row = ['address','zip_code','price','sell_date','sell_type','price_per_sq_m','no_rooms','housing_type','size_in_sq_m','year_of_construction',
           'price_change_in_pct']

    for z in scraped_list:
        csv_file_name = get_csv_filename_from_html(z)
        csv_path = os.path.join(os.getcwd(), csv_file_name)
        if platform.system() == 'Windows':
            newline=''
        else:
            newline=None
        with open(csv_path, 'w', newline=newline, encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(row)

def get_zipcodes(html_txt):
        #response = requests.get(url)
        #r = requests.get('http://138.197.184.35/boliga/')
        #my_html = r.content.decode('utf-8')
        soup = bs4.BeautifulSoup(html_txt, 'html5lib')
        table = soup.find('table')
        

        table_body = table.find('tbody')

        l = []
        rows = table_body.find_all('tr')
        rows.pop(0)
        rows.pop(1)
        rows.pop(2)
        for tr in rows:
            table_data = tr.find_all('td')

            for data in table_data:
                last_td = data.find_all('a')
                for a in last_td:
                    c = a.getText().strip()
                    
                    l.append(c)

        return l

def loop_and_scrape(url_list):
    for l in url_list:
        html_file_to_csv(l)

def run():
    file_url = 'http://138.197.184.35/boliga' 
    txt_file_name = os.path.basename(file_url)
    txt_path = os.path.join('./', txt_file_name)
    txt_path = txt_path + '.html'
    download_txt(file_url, txt_path)
    html_txt = file_to_html(txt_path)
    
    ##index_url = 'http://138.197.184.35/boliga'
    ##scraped_list= ['4500_130.html','1050-1549_1.html','1050-1549_36.html']
    ##get_zipcsv_from_list(scraped_list)
    
    url_list= get_zipcodes(html_txt)
    #print(url_list)

    #url_list = ['1050-1549_1.html','1050-1549_3.html','1050-1549_4.html','1050-1549_5.html','1050-1549_6.html','1050-1549_7.html','1050-1549_8.html',
    #      '1050-1549_9.html','1050-1549_10.html','1050-1549_11.html','1050-1549_12.html','1050-1549_13.html','1050-1549_14.html',
    #      '1050-1549_15.html']
    get_zipcsv_from_list(url_list)
    loop_and_scrape(url_list)
    print('done')
    #
    
    #file_url = 'http://138.197.184.35/boliga/1050-1549_1.html'
    #txt_file_name = os.path.basename(file_url)
    #txt_path = os.path.join('./', txt_file_name)
    #download_txt(file_url, txt_path)
    #csv_file_name = 'something.csv'
    #csv_path = os.path.join(os.getcwd(), csv_file_name)
    #scrape_housing_data(txt_path)
    #file_to_csv(txt_path, csv_path)



if __name__ == '__main__':
    run()
