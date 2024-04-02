from tkinter import *
from fpdf import FPDF

window = Tk()
window.title("Medicine Invoice Generator")

medicines = {
    "Medicine A": 10,
    "Medicine B": 20,
    "Medicine C": 15,
    "Medicine D": 25
}

invoiceItems = []


def addMedicine():
    selectedMedicine = medicineListbox.get(ANCHOR)  # Take the highlighted medicine
    quantity = int(quantityEntry.get())  # Take the medicine amount
    price = medicines[selectedMedicine]  # Take the medicine price
    itemTotal = price * quantity
    invoiceItems.append((selectedMedicine, quantity, itemTotal))
    totalAmountEntry.delete(0, END)  # Clear totalAmountEntry
    totalAmountEntry.insert(END, str(calculateTotal()))
    updateInvoiceText()


def calculateTotal():
    total = 0.0
    for item in invoiceItems:
        total = total + item[2]
    return total


def updateInvoiceText():
    invoiceText.delete(1.0, END)  # Erase everything
    for item in invoiceItems:  # Prepare invoice text
        invoiceText.insert(END, f"Medicine: {item[0]}, Quantity: {item[1]}, Total: {item[2]}\n")


def generateInvoice():
    customerName = customerEntry.get()
    pdf = FPDF()
    pdf.add_page()

    # Set up PDF formatting
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, text="Invoice", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, text=f"Customer: {customerName}",
             new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 10, text="", new_x="LMARGIN", new_y="NEXT")

    # Add invoice items to PDF
    for item in invoiceItems:
        medicineName, quantity, itemTotal = item  # Split the tuple to its components
        pdf.cell(
            0, 10, text=f"Medicine: {medicineName}, Quantity: {quantity}, Total: {itemTotal}", new_x="LMARGIN",
            new_y="NEXT", align="L")
    # Add total amount to PDF
    pdf.cell(0, 10, text="Total Amount: " +
                        str(calculateTotal()), new_x="LMARGIN", new_y="NEXT", align="L")
    # Save the PDF file
    pdf.output("Invoice.pdf")

medicineLabel = Label(window, text="Medicine:")
medicineLabel.pack()
medicineListbox = Listbox(window, selectmode=SINGLE, width=40)
for medicine in medicines:
    medicineListbox.insert(END, medicine)
medicineListbox.pack()

quantityLabel = Label(window, text="Quantity")
quantityLabel.pack()
quantityEntry = Entry(window)
quantityEntry.pack()

addButton = Button(window, text="Add Medicine", command=addMedicine)
addButton.pack()

totalAmountLabel = Label(window, text="Total Amount")
totalAmountLabel.pack()
totalAmountEntry = Entry(window)
totalAmountEntry.pack()

customerLabel = Label(window, text="Customer Name:")
customerLabel.pack()
customerEntry = Entry(window, width=40)
customerEntry.pack()

generateButton = Button(window, text="Generate Invoice", command=generateInvoice)
generateButton.pack()

invoiceText = Text(window, height=10, width=50)
invoiceText.pack()

window.mainloop()
