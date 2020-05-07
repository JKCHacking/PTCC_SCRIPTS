from collections import namedtuple


class TimesheetCalculatorTestData:
    Work = namedtuple('Work', ['projectName', 'taskName', 'date', 'timeIn', 'timeOut', 'totalHours'])
    Employee = namedtuple('Employee', ['employeeName', 'work'])
    all_employee_list = [Employee(employeeName='JED ALISON ALIMANZA', work=[
        Work(projectName='Apple Dadeland', taskName='CS02 SHOP CALCS R0.1', date='04/29/20', timeIn='01:00:00 PM',
             timeOut='02:00:00 PM', totalHours=1.0),
        Work(projectName='Apple Dadeland', taskName='CS03 SHOP CALCS R0', date='29-April-2020', timeIn='02:00:00 PM',
             timeOut='07:00:00 PM', totalHours=5.0),
        Work(projectName='Apple Dadeland', taskName='CS03 SHOP CALCS R0', date='04/29/20', timeIn='08:00:00 PM',
             timeOut='12:00 AM', totalHours=4.0),
        Work(projectName='Atlantis Project', taskName='CS02 THERM CALCS', date='27-April-2020', timeIn='11:00 AM',
             timeOut='1:00 PM', totalHours=1.0),
        Work(projectName='Atlantis Project', taskName='CS02 THERM CALCS', date='04/27/20', timeIn='02:00:00 PM',
             timeOut='08:00:00 PM', totalHours=6.0),
        Work(projectName='Atlantis Project', taskName='CS02 THERM CALCS', date='04/28/20', timeIn='02:00:00 PM',
             timeOut='08:00:00 PM', totalHours=6.0),
        Work(projectName='Atlantis Project', taskName='CS02 THERM CALCS', date='04/29/20', timeIn='09:00:00 AM',
             timeOut='12:00:00 PM', totalHours=3.0)]), Employee(employeeName='NATHAN CANTOS', work=[
        Work(projectName='250 SOUTH STREET', taskName='F02 Brackets Check', date='04/28/20', timeIn='11:00:00 PM',
             timeOut='11:30:00 PM', totalHours=0.5),
        Work(projectName='45-18 Court Square', taskName='EWS-02-Comments Review', date='04/28/20', timeIn='10:30:00 PM',
             timeOut='11:00:00 PM', totalHours=0.5),
        Work(projectName='45-18 Court Square', taskName='EWS-02-Comments Review', date='04/30/20', timeIn='02:00:00 PM',
             timeOut='04:00:00 PM', totalHours=2.0),
        Work(projectName='ATLANTIS BUILDING', taskName='QAQC-CS01 CALCS', date='04/27/20', timeIn='07:00:00 PM',
             timeOut='12:00:00 AM', totalHours=5.0),
        Work(projectName='ATLANTIS BUILDING', taskName='QAQC-CS01 CALCS', date='04/28/20', timeIn='12:00:00 AM',
             timeOut='03:00:00 AM', totalHours=2.0),
        Work(projectName='ATLANTIS BUILDING', taskName='QAQC-CS01 CALCS', date='28 April 2020', timeIn='02:00:00 PM',
             timeOut='04:00:00 PM', totalHours=2.0),
        Work(projectName='Fashion Institute of Technology', taskName='TAKE-OFF', date='28 April 2020',
             timeIn='04:00:00 PM', timeOut='06:00:00 PM', totalHours=2.0),
        Work(projectName='Fashion Institute of Technology', taskName='TAKE-OFF', date='28 April 2020',
             timeIn='09:00:00 PM', timeOut='10:30:00 PM', totalHours=1.5)])]
