import tkinter as tk
from tkinter import ttk, messagebox
import random


#org_data can be done differently, but nice to show hierarchical structure

def build_org_data():
    """
    Builds a nested dictionary structure representing
    the original 'CEO -> Marketing_VP / Production_VP -> ...' hierarchy.
    Each node has:
        - 'name': str
        - 'salary': int
        - 'subordinates': list of child dictionaries
    This replaces explicit Boss/Employee classes with built-in types.
    """
    # For consistent random output
    random.seed(2)

    def make_employee(name, base, spread, count=1):
        """
        Creates 'count' employees with random salaries.
        """
        return [
            {
                "name": f"{name}_{i}",
                "salary": int(base + random.random() * spread),
                "subordinates": []
            }
            for i in range(count)
        ]

    org_data = {
        "name": "CEO",
        "salary": 200000,
        "subordinates": [
            {
                "name": "Marketing_VP",
                "salary": 100000,
                "subordinates": [
                    {
                        "name": "Sales_Mgr",
                        "salary": 50000,
                        "subordinates": make_employee("Sales", 30000, 10000, 6)
                    },
                    {
                        "name": "Advt_Mgr",
                        "salary": 50000,
                        "subordinates": [
                            {
                                "name": "Secy",
                                "salary": 20000,
                                "subordinates": []
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Production_VP",
                "salary": 100000,
                "subordinates": [
                    {
                        "name": "Prod_Mgr",
                        "salary": 40000,
                        "subordinates": make_employee("Manuf", 25000, 5000, 4)
                    },
                    {
                        "name": "Ship_Mgr",
                        "salary": 35000,
                        "subordinates": make_employee("Ship_Clrk", 20000, 5000, 4)
                    }
                ]
            }
        ]
    }
    return org_data

def get_total_salary(emp_data):
    """
    Recursively computes the sum of 'salary'
    for emp_data and all its subordinates.
    """
    total = emp_data["salary"]
    for sub in emp_data["subordinates"]:
        total += get_total_salary(sub)
    return total

def find_employee(emp_data, name):
    """
    Recursively locates the dictionary node
    matching 'name'. Returns None if not found.
    """
    if emp_data["name"] == name:
        return emp_data
    for sub in emp_data["subordinates"]:
        found = find_employee(sub, name)
        if found is not None:
            return found
    return None

def get_report_chain(org_data, emp_data, chain=None):
    """
    Builds a chain from emp_data up to the CEO.
    Since we do not store 'parent' references,
    we do a search for the manager referencing 'emp_data'.
    """
    if chain is None:
        chain = []

    chain.append(emp_data["name"])
    if emp_data["name"] == "CEO":
        return chain

    boss = find_boss_of(org_data, emp_data)
    if boss is None:
        # If no boss is found, we are at top
        return chain
    else:
        return get_report_chain(org_data, boss, chain)

def find_boss_of(root_data, child_data):
    """
    Finds the immediate 'boss' node in root_data whose
    'subordinates' list references child_data. Returns None if not found.
    """
    for sub in root_data["subordinates"]:
        if sub is child_data:
            return root_data
        boss = find_boss_of(sub, child_data)
        if boss:
            return boss
    return None

def build_treeview(treeview, parent_id, emp_data):
    """
    Recursively inserts employees into the Treeview.
    'parent_id' is the ID of the parent node in the Treeview.
    """
    # Insert current node
    current_node_id = treeview.insert(parent_id, "end", text=emp_data["name"])

    # Recursively process subordinates
    for sub in emp_data["subordinates"]:
        build_treeview(treeview, current_node_id, sub)

class ReportButton(ttk.Button):
    """
    Button to show the "report chain" for the selected item in the Treeview.
    """
    def __init__(self, master, org_data, **kwargs):
        super().__init__(master, text="Chain", command=self.on_click, **kwargs)
        self.org_data = org_data

    def on_click(self):
        # Identify selected item
        selected = self.master.tree.focus()
        if not selected:
            messagebox.showinfo("Report chain", "No employee selected.")
            return
        name = self.master.tree.item(selected)["text"]

        emp_node = find_employee(self.org_data, name)
        if emp_node:
            chain_list = get_report_chain(self.org_data, emp_node)
            # We'll show the chain bottom-up or top-down as needed
            chain_str = "\n".join(reversed(chain_list))
            messagebox.showinfo("Report chain", chain_str)
        else:
            messagebox.showinfo("Report chain", f"No boss found for {name}.")

class SalaryButton(ttk.Button):
    """
    Button to compute and display total salaries under the selected employee.
    """
    def __init__(self, master, org_data, entry, **kwargs):
        super().__init__(master, text="Salaries", command=self.on_click, **kwargs)
        self.org_data = org_data
        self.entry = entry

    def on_click(self):
        selected = self.master.tree.focus()
        if not selected:
            messagebox.showinfo("Salaries", "No employee selected.")
            return
        name = self.master.tree.item(selected)["text"]
        emp_node = find_employee(self.org_data, name)
        if emp_node:
            total = get_total_salary(emp_node)
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{total:,}")
        else:
            self.entry.delete(0, "end")
            self.entry.insert(0, "0")

class Builder:
    """
    Replaces explicit Boss/Employee classes with
    a dictionary-based approach for the Composite structure.
    The UI logic remains similar to Cooper's code.
    """

    def __init__(self, root):
        self.root = root
        self.root.geometry("300x330")
        self.root.title("Employee Tree (Dictionary-based)")
        self.org_data = build_org_data()

    def build(self):
        """
        Builds the UI with a Treeview, a SalaryButton, an Entry, and a ReportButton.
        Then populates the treeview from the dictionary-based structure.
        """
        # Main frame
        self.frame = ttk.Frame(self.root, padding=5)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        self.tree = ttk.Treeview(self.frame, columns=[], show="tree")
        self.tree.column("#0", width=170, stretch=False)  # Name column
        self.tree.pack(pady=5)

        # Populate the Treeview from org_data
        root_id = self.tree.insert("", "end", text=self.org_data["name"])
        for sub in self.org_data["subordinates"]:
            build_treeview(self.tree, root_id, sub)
        self.tree.item(root_id, open=True)


        # Entry for salaries
        self.entry = ttk.Entry(self.frame, width=18)
        self.entry.pack(pady=2)

        # Buttons
        self.sal_button = SalaryButton(self.frame, self.org_data, self.entry)
        self.sal_button.pack(side=tk.LEFT, padx=5)

        self.chain_button = ReportButton(self.frame, self.org_data)
        self.chain_button.pack(side=tk.LEFT, padx=5)

def main():
    root = tk.Tk()
    builder = Builder(root)
    builder.build()
    root.mainloop()

if __name__ == "__main__":
    main()
