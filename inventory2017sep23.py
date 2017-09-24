import os, re, xlsxwriter
''' 
This script is to get inventory of router interface that currenlty use or not.
- Need to get log from router using 'show interfaces'
- Put all log file in same folder.
- Run script and it will as about folder location for inventory analysys.
'''
source = raw_input("Please enter the directory of router 'show interfaces' log :")
os.chdir(source)
workbook = xlsxwriter.Workbook('inventory.xlsx')
for filenames in os.listdir(source):
    if filenames.endswith(".log") or filenames.endswith(".txt"):
        print filenames
        try:
            fullpath = os.path.join(source, filenames)
            fileread = open(fullpath, 'r').read()
        except:
            print "There is some error with opening file %s" % (filenames)
        sheetname = filenames.split('.')[0]
        worksheet = workbook.add_worksheet(sheetname)
        worksheet.write(0, 0, "Interface Name")
        worksheet.write(0, 1, "Upstream")
        worksheet.write(0, 2, "Down Stream")
        worksheet.write(0, 3, "Total Interface")
        worksheet.write(0, 4, "Used")
        worksheet.write(0, 5, "Not Used")
        et_up = 0
        et_down = 0
        xe_up = 0
        xe_down = 0
        ge_up = 0
        ge_down = 0
        e1_up = 0
        e1_down = 0
        row = 1
        col = 0
        interfaces = re.findall(r"Physical interface:.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n",fileread, re.MULTILINE)
        #print interfaces
        for interface in interfaces:
            if re.findall("Physical interface: [xge][et1]", interface):
                phyinterface = re.findall(r'Physical interface: (\S+)', interface)
                inputrate = re.findall(r'Input rate.* (\d+)', interface)
                outputrate = re.findall(r'Output rate.* (\d+)', interface)
                try:
                    if (phyinterface[0][:-1] and inputrate[0] and outputrate[0]):
                        worksheet.write(row, col, phyinterface[0][:-1])
                        worksheet.write(row, col + 1, inputrate[0] + " bps")
                        worksheet.write(row, col + 2, outputrate[0] + " bps")
                except: print ('there is some wrong format of \'show interfaces\' for: %s'%phyinterface[0])
                if 'ge' in phyinterface:
                    if int(inputrate[0]) != 0 or int(outputrate[0]) != 0:
                        ge_up += 1
                    else:
                        ge_down += 1
                elif 'xe' in phyinterface:
                    if int(inputrate[0]) != 0 or int(outputrate[0]) != 0:
                        xe_up += 1
                    else:
                        xe_down += 1
                elif 'et' in phyinterface:
                    if int(inputrate[0]) != 0 or int(outputrate[0]) != 0:
                        et_up += 1
                    else:
                        et_down += 1
                elif 'e1' in phyinterface:
                    if int(inputrate[0]) != 0 or int(outputrate[0]) != 0:
                        e1_up += 1
                    else:
                        e1_down += 1
                row +=1
                col = 0
        worksheet.write(1, 3, "GE interface")
        worksheet.write(1, 4, ge_up)
        worksheet.write(1, 5, ge_down)
        worksheet.write(2, 3, "XE interface")
        worksheet.write(2, 4, xe_up)
        worksheet.write(2, 5, xe_down)
        worksheet.write(3, 3, "ET interface")
        worksheet.write(3, 4, et_up)
        worksheet.write(3, 5, et_down)
        worksheet.write(4, 3, "E1 interface")
        worksheet.write(4, 4, e1_up)
        worksheet.write(4, 5, e1_down)
        print "xe up/down count: %s/%s, ge up down count: %s/%s et up/down count %s/%s " % (
        xe_up, xe_down, ge_up, ge_down, et_up, et_down)
    else:
        print "%s is not log files" % (filenames)
workbook.close()