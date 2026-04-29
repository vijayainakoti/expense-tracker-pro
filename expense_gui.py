import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER,
    category TEXT,
    date TEXT
)
""")
conn.commit()

current_records = []

# ---------------- FUNCTIONS ---------------- #

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    amount_entry.focus_set()


def add_expense():
    try:
        amount = int(amount_entry.get())
        category = category_entry.get().strip()
        date = date_entry.get().strip()

        if not category or not date:
            return messagebox.showwarning("Warning", "Fill all fields")

        cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                       (amount, category, date))
        conn.commit()

        clear_entries()
        view_expenses()

    except:
        messagebox.showerror("Error", "Invalid input")


def view_expenses():
    global current_records
    listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    rows = cursor.fetchall()
    current_records = rows

    if not rows:
        listbox.insert(tk.END, "No expenses found")
        return

    for i, e in enumerate(rows):
        listbox.insert(tk.END, f"₹{e[1]} | {e[2]} | {e[3]}")


def delete_expense():
    sel = listbox.curselection()
    if not sel:
        return

    idx = sel[0]
    cursor.execute("DELETE FROM expenses WHERE id=?", (current_records[idx][0],))
    conn.commit()
    view_expenses()


def update_expense():
    sel = listbox.curselection()
    if not sel:
        return

    idx = sel[0]
    rid = current_records[idx][0]

    if amount_entry.get():
        cursor.execute("UPDATE expenses SET amount=? WHERE id=?", (amount_entry.get(), rid))
    if category_entry.get():
        cursor.execute("UPDATE expenses SET category=? WHERE id=?", (category_entry.get(), rid))
    if date_entry.get():
        cursor.execute("UPDATE expenses SET date=? WHERE id=?", (date_entry.get(), rid))

    conn.commit()
    view_expenses()


def on_select(event):
    sel = listbox.curselection()
    if not sel:
        return

    d = current_records[sel[0]]

    clear_entries()
    amount_entry.insert(0, d[1])
    category_entry.insert(0, d[2])
    date_entry.insert(0, d[3])


def total_expense():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    messagebox.showinfo("Total", f"₹{total}")


def category_summary():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    msg = "\n".join([f"{c}: ₹{a}" for c, a in data])
    messagebox.showinfo("Summary", msg or "No data")


def show_bar():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    if not data:
        return

    plt.figure()
    plt.bar([x[0] for x in data], [x[1] for x in data])
    plt.title("Expenses Bar Chart")
    plt.show()


def show_pie():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    if not data:
        return

    plt.figure()
    plt.pie([x[1] for x in data], labels=[x[0] for x in data], autopct="%1.1f%%")
    plt.title("Expenses Pie Chart")
    plt.show()


def export_csv():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Amount", "Category", "Date"])
        writer.writerows(rows)

    messagebox.showinfo("Export", "CSV saved!")


# ---------------- UI (UPGRADED UX) ---------------- #

root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("600x750")
root.config(bg="#f4f6f9")

# ===== HEADER ===== #
header = tk.Frame(root, bg="#2c3e50", pady=10)
header.pack(fill="x")

tk.Label(header, text="💰 Expense Tracker Pro",
         font=("Arial", 18, "bold"), fg="white", bg="#2c3e50").pack()

# ===== INPUT CARD ===== #
card = tk.Frame(root, bg="white", padx=10, pady=10)
card.pack(pady=10, padx=10, fill="x")

tk.Label(card, text="Amount").grid(row=0, column=0, sticky="w")
amount_entry = tk.Entry(card, width=25)
amount_entry.grid(row=0, column=1, pady=5)

tk.Label(card, text="Category").grid(row=1, column=0, sticky="w")
category_entry = tk.Entry(card, width=25)
category_entry.grid(row=1, column=1, pady=5)

tk.Label(card, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
date_entry = tk.Entry(card, width=25)
date_entry.grid(row=2, column=1, pady=5)

# ===== BUTTONS ===== #
btn_frame = tk.Frame(root, bg="#f4f6f9")
btn_frame.pack(pady=5)

def btn(text, color, cmd, r, c):
    tk.Button(btn_frame, text=text, bg=color, fg="white",
              width=12, command=cmd).grid(row=r, column=c, padx=5, pady=5)

btn("Add", "#27ae60", add_expense, 0, 0)
btn("Update", "#f39c12", update_expense, 0, 1)
btn("Delete", "#e74c3c", delete_expense, 0, 2)

btn("Total", "#8e44ad", total_expense, 1, 0)
btn("Summary", "#34495e", category_summary, 1, 1)
btn("Export", "#16a085", export_csv, 1, 2)

btn("Bar Chart", "#2980b9", show_bar, 2, 0)
btn("Pie Chart", "#8e44ad", show_pie, 2, 1)

# ===== LISTBOX CARD ===== #
list_frame = tk.Frame(root, bg="white")
list_frame.pack(pady=10, padx=10, fill="both", expand=True)

scroll = tk.Scrollbar(list_frame)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, font=("Arial", 11), yscrollcommand=scroll.set)
listbox.pack(fill="both", expand=True)
scroll.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", on_select)

view_expenses()
root.mainloop()