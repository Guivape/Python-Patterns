import tkinter as tk
from tkinter import Listbox, Entry, END
from functools import singledispatch

# ----------------------------
# Replaces 'accept()' visitor logic with singledispatch functions
# for dynamic dispatch on Employee vs. Boss.
# ----------------------------

class Employee:
    def __init__(self, name, salary, vacdays, sickdays):
        self.name = name
        self.salary = salary
        self.vacDays = vacdays
        self.sickDays = sickdays

    def getName(self): 
        return self.name

    def getVacDays(self): 
        return self.vacDays

    def getSalary(self):
        return self.salary

class Boss(Employee):
    def __init__(self, name, salary, vacdays, sickdays):
        super().__init__(name, salary, vacdays, sickdays)
        self.bonusdays = 0

    def setBonusdays(self, bd):
        self.bonusdays = bd

    def getBonusdays(self):
        return self.bonusdays


# Singledispatch function for "VacationVisitor" (normal vac days)
@singledispatch
def vacation_days(emp):
    # Fallback for normal Employee
    return emp.getVacDays()

@vacation_days.register
def _(emp: Boss):
    # Boss also uses normal vac days (like the old VacationVisitor)
    # not counting bonus days here
    return emp.getVacDays()


# Singledispatch function for "BVacationVisitor" (vac + bonus)
@singledispatch
def bvacation_days(emp):
    return emp.getVacDays()

@bvacation_days.register
def _(emp: Boss):
    # For Boss, sum vac + bonus
    return emp.getVacDays() + emp.getBonusdays()


class Mediator:
    """
    Manages interactions for the UI:
    - Listbox selection
    - 'Visit' button click
    - Displays normal and boss vacation totals
    """
    def __init__(self):
        self.employees = []
        self.listbox = None
        self.totalField = None
        self.btotalField = None

    def setEmployees(self, emp_list):
        self.employees = emp_list

    def setFields(self, total, btotal):
        self.totalField = total
        self.btotalField = btotal

    def setList(self, lb):
        self.listbox = lb

    def clearFields(self):
        self.totalField.delete(0, END)
        self.btotalField.delete(0, END)

    def clickList(self, evt):
        idx = self.listbox.curselection()
        if not idx:
            return
        i = idx[0]
        emp = self.employees[i]

        self.clearFields()
        # Show normal vac
        self.totalField.insert(0, str(emp.getVacDays()))
        # If it's a Boss, also show bonus
        if isinstance(emp, Boss):
            self.btotalField.insert(0, str(emp.getBonusdays()))

    def vclick(self):
        # Equivalent of "VacationVisitor" and "BVacationVisitor"
        self.clearFields()
        total = sum(vacation_days(e) for e in self.employees)
        btotal = sum(bvacation_days(e) for e in self.employees)
        self.totalField.insert(0, str(total))
        self.btotalField.insert(0, str(btotal))


class DButton(tk.Button):
    """
    Minimal derived button that calls mediator action on click.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, command=self.comd, **kwargs)
    def comd(self):
        pass

class VisitButton(DButton):
    def __init__(self, master, med, **kwargs):
        super().__init__(master, text="Visit", **kwargs)
        self.med = med
    def comd(self):
        self.med.vclick()


class Builder:
    def build(self):
        root = tk.Tk()
        root.geometry("350x200")
        root.title("Visitor with singledispatch Demo")

        self.listbox = Listbox(root, width=25, height=8)
        self.listbox.grid(row=0, column=0, rowspan=5)

        self.vac = Entry(root, width=20)
        self.vac.grid(row=0, column=1, padx=10, sticky="nw")

        self.bonus = Entry(root, width=20)
        self.bonus.grid(row=1, column=1, padx=10, sticky="nw")

        self.med = Mediator()
        self.med.setList(self.listbox)
        self.med.setFields(self.vac, self.bonus)
        self.listbox.bind('<<ListboxSelect>>', self.med.clickList)

        vbutton = VisitButton(root, self.med)
        vbutton.grid(row=2, column=1)

        self.loadList()
        root.mainloop()

    def loadList(self):
        # Example employees
        employees = [
            Employee("Susan Bear", 55000, 12, 1),
            Employee("Adam Gehr", 150000, 9, 0),
            Employee("Fred Harris", 50000, 15, 2),
            Employee("David Oakley", 57000, 12, 2),
            Employee("Larry Thomas", 100000, 20, 6),
        ]
        b1 = Boss("Leslie Susi", 175000, 16, 4)
        b1.setBonusdays(12)
        b2 = Boss("Laurence Byerly", 35000, 17, 6)
        b2.setBonusdays(17)
        employees.extend([b1, b2])

        self.med.setEmployees(employees)
        for e in employees:
            self.listbox.insert(END, e.getName())

def main():
    Builder().build()

if __name__ == "__main__":
    main()
