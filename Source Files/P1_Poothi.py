import os
import time
import PySimpleGUI as sg
import psutil
import matplotlib.pyplot as plt
import numpy as np

sg.theme('Dark Blue')  # please make your creations colorful

layout = [[sg.Text('Upload your Algorithm 1')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Text('Upload your Algorithm 2')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK('Compare'), sg.Cancel()]]

window = sg.Window('Algorithms Comparison', layout)


def runProgram(program):
    os.system('python ' + program)
    Data = getData(program)
    return Data


def runPrograms(program1, program2):
    os.system('python ' + program1 + " && python " + program2)
    Data = getData(program1+" And "+program2)
    return Data


def getData(program):
    Data = []
    pid = os.getpid()
    py = psutil.Process(pid)
    CPU_Time = psutil.cpu_times_percent(interval=1, percpu=False)
    CPU_Time_User = psutil.cpu_times_percent(interval=1, percpu=False).user
    mem_usage = py.memory_percent()
    mem_info = py.memory_info()
    hdd = psutil.disk_usage('/')
    rss = mem_info[0] / 2. ** 30
    vms = mem_info[1] / 2. ** 30
    pf = mem_info[2]

    Data.append(CPU_Time_User)
    Data.append(mem_usage)
    Data.append(hdd)
    Data.append(rss)
    Data.append(vms)
    Data.append(pf)
    Data.append(psutil.cpu_times_percent(interval=1, percpu=False).system)
    print("\n______________________________________________" + program + "______________________________________________\n")
    print("System Level Information:")
    print("CPU User Usage: ", CPU_Time, "\n")  # 1
    print("Memory Usage: ", mem_usage, " \n")  # 2
    print("Hard Drive Usage: \n \tTotal: ", hdd.total / (2 ** 30), " GB, Used: ", hdd.used / (2 ** 30), " GB Free: ", hdd.free / (2 ** 30)," GB \n")  # 3
    print("RSS (Resident set size): ", rss, " GB \n")  # 4
    print("VMS (Virtual memory size): ", vms, " GB \n")  # 5
    print("No. of Page faults: ", pf, "\n\n")  # 6
    return Data


def userInformation(start,end,return_='false'):
    if(return_ == 'false'):
        print("User-Level Information: \n")
        print("Execution time :",(end - start),end=" Seconds\n\n\n")
    elif(return_== 'true'):
        return float(end - start)


def drawGraph(title, label, p1, p2, p1_2):
    objects = ('Program 1', 'Program 2', 'Program  1 & 2')
    y_pos = np.arange(len(objects))
    performance = [p1,p2,p1_2]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(label)
    plt.title(title)
    for i,v in enumerate(performance):
        plt.text(i, v, str(v))
    plt.show()


while True:
    event, programs = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    print('Filename 1: ', programs[0])
    print('Filename 2: ', programs[1], "\n")
    user_info = []
    start_time = time.time()
    program1 = runProgram(programs[0])
    end_time = time.time()
    userInformation(start_time, end_time)
    user_info.append(end_time - start_time)
    start_time = time.time()
    program2 = runProgram(programs[1])
    end_time = time.time()
    userInformation(start_time, end_time)
    user_info.append(end_time - start_time)
    start_time = time.time()
    program1_2 = runPrograms(programs[0], programs[1])
    end_time = time.time()
    userInformation(start_time, end_time)
    user_info.append(end_time - start_time)

    drawGraph("User level Information", "Execution time (in sec)", user_info[0], user_info[1], user_info[2])
    drawGraph("CPU User Usage", "Usage (in %)", program1[0], program2[0], program1_2[0])
    drawGraph("CPU System Usage", "Usage (in %)", program1[6], program2[6], program1_2[6])
    drawGraph("Memory Usage", "Usage (in GB)", program1[1], program2[1], program1_2[1])
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Used', 'Free'
    size1 = [program1[2][1]/2**30, program1[2][2]/2**30]
    size2 = [program2[2][1]/2**30, program2[2][2]/2**30]
    size1_2 = [program1_2[2][1]/2**30, program1_2[2][2]/2**30]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax= plt.subplots(1, 3)
    ax[0].pie(size1, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[0].set_title('Program 1')
    ax[1].pie(size2, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax[1].axis('equal')
    ax[1].set_title('Program 2')
    ax[2].pie(size1_2, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax[2].axis('equal')
    ax[2].set_title('Program 1 & 2')
    plt.suptitle("Hard Disk Usage")
    plt.show()
    drawGraph("RSS (Resident Set Size)", "Size (in GB)", program1[3], program2[3], program1_2[3])
    drawGraph("VMS (Virtual Memory Size)", "Size (in GB)", program1[4], program2[4], program1_2[4])
    drawGraph("Page Faults", "No. of page faults", program1[5], program2[5], program1_2[5])
window.close()
