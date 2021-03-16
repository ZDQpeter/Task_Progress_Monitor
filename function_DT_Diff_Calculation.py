from datetime import date

def function_DT_Diff_Calculation(DT_Commenced, DT_Completed):
    # DT Format: YYYY-MM-DD hh:mm:ss

    diff = 0
    DT_Commenced_YYYY = DT_Commenced.split(' ')[0].split('-')[0]
    DT_Commenced_MM = DT_Commenced.split(' ')[0].split('-')[1]
    DT_Commenced_DD = DT_Commenced.split(' ')[0].split('-')[2]
    DT_Commenced_hh = DT_Commenced.split(' ')[1].split(':')[0]
    DT_Commenced_mm = DT_Commenced.split(' ')[1].split(':')[1]

    # print(DT_Commenced, DT_Completed)

    DT_Completed_YYYY = DT_Completed.split(' ')[0].split('-')[0]
    DT_Completed_MM = DT_Completed.split(' ')[0].split('-')[1]
    DT_Completed_DD = DT_Completed.split(' ')[0].split('-')[2]
    DT_Completed_hh = DT_Completed.split(' ')[1].split(':')[0]
    DT_Completed_mm = DT_Completed.split(' ')[1].split(':')[1]

    DT_Commenced_val = date(int(DT_Commenced_YYYY), int(DT_Commenced_MM), int(DT_Commenced_DD))
    DT_Completed_val = date(int(DT_Completed_YYYY), int(DT_Completed_MM), int(DT_Completed_DD))
    diff = DT_Completed_val - DT_Commenced_val
    diff_days = diff.days

    Time_Commenced_val = int(DT_Commenced_hh) + int(DT_Commenced_mm) / 60
    Time_Completed_val = int(DT_Completed_hh) + int(DT_Completed_mm) / 60

    # in unit of hours
    diff = diff_days * 24 - Time_Commenced_val + Time_Completed_val

    return diff