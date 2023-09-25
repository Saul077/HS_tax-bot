def hs_code(hs_code):
    "Does all the required processes to get the final tax amount"
    #Importing required modules
    import requests
    from bs4 import BeautifulSoup
    import tabula
    import csv as CV
    import pandas as pd
    import camelot		

    #Declaring variables
    headings = []
    pref_duty_index = []
    gen_index = 0
    hs_list = []
    hs_row = []
    hs_desc = ""
    chapter = hs_code[0:2]
    if chapter[0] == '0':
        chapter = chapter[1]        
    pref_duty = ""
    gen_duty =""
    tax = ""
    row_found = False
    fixed_chg = ""

    #Getting the hs code value that corresponds with the Srilankan hs code characters
    if len(hs_code) != 8:
        while len(hs_code) != 8:
            hs_code +="0"
    if hs_code[-4:] == "0000":
        hs_code = hs_code[0:4]
    elif hs_code[-3:] == "000":
        hs_code = hs_code[0:4] + "." + hs_code[4:6]
    else:
        hs_code = hs_code[0:4] + "." + hs_code[4:6] + "." + hs_code[6:]

    print(hs_code)

    #Downloading the PDF File of the relevant chapter
    # Import tariff website url
    url = "https://www.customs.gov.lk/customs-tariff/import-tariff/"

    # Request URL and get response
    response = requests.get(url)

    # parse text obtained
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all hyperlinks present on webpage
    links = soup.find_all('a')

    # From all links check for the relevant pdf file
    for link in links:
        if ('.pdf' in link.get('href', [])) and (chapter in link.get('href', [])):
            print("Downloading file...")

            response = requests.get(link.get('href'))

            # Write content in pdf file
            pdf = open(chapter + ".pdf", "wb")
            pdf.write(response.content)
            pdf.close()
            print("File Downloaded")

    # convert all tables of a PDF file into a single CSV file
    print("Converting...")
    tabula.convert_into(chapter + ".pdf", "output.csv", output_format="csv", pages="all")
    file = chapter+".pdf"
    print(file)
    hs_tabs = camelot.read_pdf(file)
    hs_tabs.export("output.csv", f="csv", compress=False)
    print("Conversion Done!")

    # Finding the row corresponding with the hs code
    while row_found == False:
        print("not found")
        #Getting the taxes relevant to the hs code from the csv file
        # Open file
        file = "output.csv"
        print(file)
        with open(file) as f:
            # Create reader object by passing the file
            # object to reader method
            reader_obj = CV.reader(f)
            for row in reader_obj:
                #Get headings int a list
                if headings == []:
                    if "Preferential Duty" in row:
                        headings = row
                        temp_index = headings.index("Preferential Duty")
                        headings[temp_index] = "AP"
                        headings[temp_index+1] = "AD"
                        headings[temp_index+2] = "BN"
                        headings[temp_index+3] = "GT"
                        headings[temp_index+4] = "IN"
                        headings[temp_index+5] = "PK"
                        headings[temp_index+6] = "SA"
                        headings[temp_index+7] = "SF"
                        headings[temp_index+8] = "SD"
                        headings[temp_index+9] = "SG"
                        gen_index = temp_index+10
                        pref_duty_index = [temp_index,temp_index+1,temp_index+2,temp_index+3,temp_index+4,temp_index+5,temp_index+6,temp_index+7,temp_index+8,temp_index+9]
                        temp_index = headings.index("HS Code")
                        temp_index2 = headings.index("Description")

                #continue if headings list is blank
                if headings == []:
                    continue
                
                #Getting the rows for the sub categorized hs code
                if row[temp_index]== hs_code:
                    print("bb")
                    hs_row = row
                    hs_desc = row[temp_index2]
                    hs_list.append(row)
                    #data found variable
                    row_found = True
                elif hs_code in row[temp_index]:
                    print("hh")
                    row_found = True
                    hs_list.append(row)

            #Repeating the loop if data not found by tracing back to the superior category
            if row_found == False:
                print(".")
                print(len(hs_code))
                print(hs_code)
                if len(hs_code) == 10:
                    hs_code = hs_code[0:7]
                    print(hs_code)
                    continue
                elif len(hs_code) == 7:
                    hs_code = hs_code[0:4]
                    print(hs_code)
        print(hs_list)
        print(headings)


        #Removing line breaks
        for i in hs_list:
            j = 0
            while j<=(len(i)-1):
                i[j] =i[j].replace('\n',' ')
                if i[j] == '':
                    i[j] = '-'
                j+=1

        hs_desc = hs_desc.replace('\n',' ')

        if len(hs_list) == 1:
            hs_row = hs_list[0]
            hs_desc = hs_list[0][temp_index2]

        print(hs_row)

        #Calculating total tax if exact data found
        if hs_row != [] and len(hs_list) == 1:
            for i in hs_row:
                j = i.replace('\n',' ')
                if hs_row.index(i) in pref_duty_index and i!="Free":
                    pref_duty +="\n"+j+" ("+headings[hs_row.index(i)]+")"
                    hs_row[hs_row.index(i)] = "-"
                    
                elif hs_row.index(i) == gen_index and i!="Free":
                    gen_duty = j
                    hs_row[hs_row.index(i)] = "-"
                    
                elif i[-1:] == "%" and "Rs." not in i:
                    tax+="\n"+i+" ("+headings[hs_row.index(i)]+")"
                    
                elif "Rs." in i:
                    fixed_chg += " \n+ "+j+" ("+headings[hs_row.index(i)]+")"
                    
            print(str(tax)+"%"+fixed_chg+"\n\Preferential Duties(By Country)"+pref_duty+"\n\General Duty\n"+gen_duty)
            if pref_duty != "" and gen_duty != "":
                tax = ""+str(tax)+"%"+fixed_chg+"\n\nPREFERENTIAL DUTY (BY COUNTRY)"+pref_duty+"\n\nGENERAL DUTY\n"+gen_duty

            else:
                tax = ""+str(tax)+"%"+fixed_chg+""

        #Writing relevant data to a csv file followed by html if exact data not found
        else:
            # name of csv file
            filename = "HS.csv"

            # writing to csv file
            with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = CV.writer(csvfile)
            
                # writing the fields
                csvwriter.writerow(headings)
            
                # writing the data rows
                csvwriter.writerows(hs_list)

  
            # SAVE CSV TO HTML USING PANDAS
            csv = 'HS.csv'
            html_file = 'HS.html'
  
            df = pd.read_csv(csv, sep=',')
            df.to_html(html_file)

    return tax, hs_desc
                    


