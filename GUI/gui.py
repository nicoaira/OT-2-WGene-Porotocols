import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()


frame1 = tk.Frame()
frame2 = tk.Frame()
frame3 = tk.Frame()
sub_frame3 = tk.Frame(master = frame3)

################## SELECCION DE REACTIVO ##################

label_rvo = tk.Label(master = frame1, text = 'Reactivo a alicuotar:')
label_rvo.pack()

rb_rvo1 = tk.Radiobutton(
	master = frame1,
	text = 'Master Mix 5x',
	value = 1)

rb_rvo1.pack(padx = 3, pady= 2)

rb_rvo2 = tk.Radiobutton(
	master = frame1,
	text = 'RT Mix 40x',
	value = 2)

rb_rvo2.pack(padx = 3, pady= 2)


################## CANTIDAD DE RACKS A USAR ##################


label_num_racks = tk.Label(frame2, text='Cantidad de racks a utilizar')
label_num_racks.pack(padx = 10)


vlist = list(range(1,10))
menu_num_racks = ttk.Combobox(master = frame2, values = vlist)
menu_num_racks.set(9)

menu_num_racks.pack(padx = 10, pady = 10)


################## SETEO FALCONS ##################


label_falcons = tk.Label(frame3, text='Falcons a utilizar')
label_falcons.pack(padx = 10)


falcon_list = list(range(1,7))
menu_num_falcon = ttk.Combobox(master = frame3, values = falcon_list)
menu_num_falcon.set(6)


menu_num_falcon.pack(padx = 10, pady = 10)

# falcons = [volfalcon1, volfalcon2, volfalcon3, volfalcon4, volfalcon5, volfalcon6]


label_falcons = tk.Label(frame3, text='Ingrese el volumen en cada Falcon (mL)')
label_falcons.pack(padx = 10, pady=10)

for i in range(3):

	for j in range(0, 4, 2):


		if j == 0:
			row = 'A'
		elif j == 2:
			row = 'B'

		falcon_label = tk.Label(sub_frame3, text = row + str(i))
		falcon_label.grid(row = j, column = i, padx = 10, pady = 3)




falcons = []

for i in range(3):

	for j in range(1 ,5 ,2):

		volfalcon = tk.Entry(sub_frame3, width = 3)
		volfalcon.insert(0,'44')
		falcons.append(volfalcon)
		volfalcon.grid(row = j, column = i, padx = 10)

sub_frame3.pack()


################## EMPAQUETADO DE LOS FRAMES ##################


frame1.grid(row = 1, column = 1, padx = 10, pady = 10)
frame2.grid(row = 2, column = 1, padx = 10, pady = 10)
frame3.grid(row = 3, column = 1, padx = 10, pady = 10)

root.mainloop()
