import csv
from subprocess import check_output,call

#get the relative paths to all csv files
csv_files = str(check_output(['find','.','-name','*.csv']),'utf-8')
csv_files = csv_files.splitlines()

for csv_file in csv_files:
    out_lines = []
    r = csv.reader(open(csv_file))
    removed_lines = 0
    for line in r:
        #0:c_image#1:l_image#2:r_image#3:s_angle#4:throttle#5:brake#6:speed
        throttle = float(line[4])
        brake = float(line[5])
        speed = float(line[6])
        if (brake == 1) or (speed < 20) or (throttle != 1):
            #this sample should not be in the data, delete center image
            call(['rm',line[0]])
            removed_lines += 1
        else:
            #append this entry to the output list
            out_lines.append(line)
    print("removed ",removed_lines," lines from ",csv_file)
    w = csv.writer(open(csv_file,'w'))
    w.writerows(out_lines)

