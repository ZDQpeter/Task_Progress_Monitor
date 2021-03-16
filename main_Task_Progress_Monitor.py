import datetime
import tkinter as tk
from tkinter import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from function_DT_Diff_Calculation \
    import function_DT_Diff_Calculation
from function_Save_Data_Matrix_into_CSV \
    import function_Save_Data_Matrix_into_CSV

# ==================================================================================
# self-defined function below!

def refresh():

    global data, data_header, id_list, task_list, dt_start_list, dt_end_list, duration_hrs_list, var_select, checkbutton_select_list

    data_df = pd.read_csv('./Input/database.csv', header=None)
    data = np.matrix(data_df)[1:, :]
    data_header = np.matrix(data_df)[0, :]

    id_list = np.array(data[:, 0]).squeeze()
    task_list = np.array(data[:, 1]).squeeze()
    dt_start_list = np.array(data[:, 2]).squeeze()
    dt_end_list = np.array(data[:, 3]).squeeze()
    duration_hrs_list = np.array(data[:, 4]).squeeze()

    data_str = ''
    if (np.alen(id_list) > 1):
        for i in range (0, np.alen(id_list)):
            data_str = data_str + str(id_list[i]) + ': ' + str(task_list[i]) + '\n'
    elif (np.alen(id_list) == 1):
        data_str = data_str + str(id_list) + ': ' + str(task_list)
    else:
        data_str = 'No data.'

    data_label = tk.Label(master, text='Select Task(s) to Show/Delete:', justify='left')
    data_label.place(x=10, y=30)

    data_textbox = tk.Text(master, height=10, width=85, font=("Helvetica", 10))
    data_textbox.insert(tk.END, data_str)
    data_textbox.place(x=10, y=50)


    var_select = []
    checkbutton_select_list = []
    if (np.alen(id_list) > 1):
        for i in range(0, np.alen(id_list)):
            var = IntVar()
            checkbutton_select = Checkbutton(master, text='Task ' + str(id_list[i]), variable=var)
            checkbutton_select.place(x=650, y=45 + i*18)
            var_select = np.append(var_select, var)
            checkbutton_select_list = np.append(checkbutton_select_list, checkbutton_select)
    elif (np.alen(id_list) == 1):
        var = IntVar()
        checkbutton_select = Checkbutton(master, text='Task ' + str(id_list), variable=var)
        checkbutton_select.place(x=650, y=45)
        var_select = np.append(var_select, var)
        checkbutton_select_list = np.append(checkbutton_select_list, checkbutton_select)
    else:
        print('No data.')


    print('Refresh successfully.')

    return



def show():

    idx = []
    for i in range (0, np.alen(var_select)):
        if (int(var_select[i].get()) == 1):
            idx = np.append(idx, i)

    # generate figure plot
    plt.figure()
    color_set = ['red', 'green']
    for i in range (0, np.alen(idx)):
        idx_val = int(idx[i])

        id = int(id_list[idx_val])
        task = str(task_list[idx_val])
        duration_hrs = float(duration_hrs_list[idx_val])
        dt_start = str(dt_start_list[idx_val])
        dt_now = str(datetime.datetime.now()).split('.')[0]
        complete_hrs = function_DT_Diff_Calculation(dt_start, dt_now)
        if (complete_hrs < 0):
            complete_hrs = 0
        completeness = round(complete_hrs / duration_hrs, 3)


        plt.barh(2 * i - 1, duration_hrs, color=color_set[0])
        plt.barh(2 * i - 1, complete_hrs, color=color_set[1])
        plt.text(1, 2 * i - 1 + 0.5, 'Task ' + str(id) + ': [Completed ' + str(round((completeness * 100), 3)) + '%]')
        plt.xlabel('Task Progress')
        plt.xticks([])
        plt.yticks([])
        plt.ylim(-2, 2 * np.alen(idx) - 0.5)
        plt.title('Task Progress Monitor')


    plt.show()
    print('Show successfully.')

    return



def create():

    global data, data_header
    m = np.alen(id_list)
    id_val = m
    task_val = str(e_task.get())
    dt_start_val = str(e_dt_start.get())
    dt_end_val = str(e_dt_end.get())
    duration_hrs = function_DT_Diff_Calculation(dt_start_val, dt_end_val)

    row = np.matrix([id_val, task_val, dt_start_val, dt_end_val, duration_hrs])
    data = np.vstack((data, row))
    data_result = np.vstack((data_header, data))
    function_Save_Data_Matrix_into_CSV(data_result, './Input/database.csv')


    # clear labels for next refresh update
    if (np.alen(checkbutton_select_list) >= 1):
        for i in range(0, np.alen(checkbutton_select_list)):
            checkbutton_select = checkbutton_select_list[i]
            checkbutton_select.destroy()
    else:
        print('No data.')



    print('Create successfully.')

    return



def delete():

    global data, data_header

    idx = []
    for i in range(0, np.alen(var_select)):
        if (int(var_select[i].get()) == 1):
            idx = np.append(idx, i)

    offset = 0
    for i in range (0, np.alen(idx)):
        idx_val = int(idx[i]) - offset

        data_p1 = data[0:idx_val, :]
        data_p2 = data[(idx_val+1):, :]

        data = np.vstack((data_p1, data_p2))
        offset = offset + 1

    (m, n) = np.shape(data)
    for i in range (0, m):
        data[i, 0] = i
    data_result = np.vstack((data_header, data))
    function_Save_Data_Matrix_into_CSV(data_result, './Input/database.csv')


    # clear labels for next refresh update
    if (np.alen(checkbutton_select_list) >= 1):
        for i in range (0, np.alen(checkbutton_select_list)):
            checkbutton_select = checkbutton_select_list[i]
            checkbutton_select.destroy()
    else:
        print('No data.')

    print('Delete successfully.')

    return




# self-defined function above!

# ==================================================================================


# GUI Layout
master = tk.Tk()
master.title('Task Progress Monitor')
master.geometry("800x400")



# Buttons:
b_refresh = tk.Button(master, text='Refresh', command=refresh)
b_refresh.grid(row=2, column=0)

b_show = tk.Button(master, text='Show', command=show)
b_show.grid(row=2, column=1)

b_create = tk.Button(master, text='Create', command=create)
b_create.place(x=430, y=315)

b_delete = tk.Button(master, text='Delete (1 Selected Only)', command=delete)
b_delete.place(x=650, y=315)




# Textbox:
l_task = tk.Label(master, text='Task Description')
l_task.place(x=10, y=300)
e_task = tk.Entry(master)
e_task.delete(0, tk.END)
e_task.insert(0, 'Input new task here')
e_task.place(x=10, y=320)



l_dt_start = tk.Label(master, text='Datetime Start')
l_dt_start.place(x=150, y=300)
e_dt_start = tk.Entry(master)
e_dt_start.delete(0, tk.END)
e_dt_start.insert(0, 'yyyy-mm-dd hh:mm-ss')
e_dt_start.place(x=150, y=320)


l_dt_end = tk.Label(master, text='Datetime End')
l_dt_end.place(x=290, y=300)
e_dt_end = tk.Entry(master)
e_dt_end.delete(0, tk.END)
e_dt_end.insert(0, 'yyyy-mm-dd hh:mm-ss')
e_dt_end.place(x=290, y=320)





master.mainloop()
















# # Selling Price label and entry:
# l_SalePrice = tk.Label(master, text='Sale Price = ', bg='yellow')
# l_SalePrice.grid(row=0, column=0)
# e_SalePrice = tk.Entry(master, bg='yellow')
# e_SalePrice.delete(0, tk.END)
# e_SalePrice.insert(0, "1000000")
# e_SalePrice.grid(row=0, column=1)
#
#
# # Holding Period label and entry:
# l_HoldPeriod = tk.Label(master, text='Hold Period (Years) = ', bg='cyan')
# l_HoldPeriod.grid(row=1, column=0)
# e_HoldPeriod = tk.Entry(master, bg='cyan')
# e_HoldPeriod.delete(0, tk.END)
# e_HoldPeriod.insert(0, "1")
# e_HoldPeriod.grid(row=1, column=1)
#



# # Textbox output
# tb_output = tk.Text(master)
# tb_output.place(x=5, y=80, height=100, width=380)






















