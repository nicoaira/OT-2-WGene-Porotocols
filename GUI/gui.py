import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import configparser
import string
import subprocess




###############################################

root = tk.Tk()
root.title('Protocolo - WGene SARS-CoV-2 RT Detection')

################## VARIABLES ##################


rvo = tk.StringVar()
OT2_IP = "169.254.77.218"


################## DEFINICION DE FUNCIONES ##################

def seleccion_num_falcons(event):

	num_falcon = int(menu_num_falcon.get())
	for i, v in enumerate(falcons):

		if i < num_falcon:
			falcons[i].config(state = 'normal')
			falcons[i].delete(0,4)
			falcons[i].insert(0, 44)
		else:
			falcons[i].delete(0,4)
			falcons[i].config(state = 'disabled')


def saludar():
	print('holas')

def guardar():

	config = configparser.ConfigParser()

	config['REACTIVO'] = {'Reactivo' : rvo.get()}
	config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
	config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}

	falcons_dict = {}
	a = 0
	for i in range(3):
		for j in string.ascii_uppercase[:2]:
			falcons_dict[j+str(i+1)] = falcons[a].get()
			a += 1

	# config['VOL_FALCONS'] = {str(index+1):v.get() for (index, v) in enumerate(falcons)}
	config['VOL_FALCONS'] = falcons_dict

	with open('config.ini', 'w') as configfile:
		config.write(configfile)

	#### Carga en OT-2

	upload_script = ["scp",
					 "-i",
					 "ot2_ssh_key",
					 "../config.ini",
					 "root@169.254.77.218:/data/user_storage"]

	upload = subprocess.run(upload_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	upload.wait(10)


################## INICIALIZACION DE FRAMES ##################


frame1 = tk.Frame()
frame2 = tk.Frame()
frame3 = tk.Frame(relief  = tk.GROOVE, borderwidth=3, pady=20)
sub_frame3 = tk.Frame(master = frame3)
frame4 = tk.Frame()


################## SELECCION DE REACTIVO ##################

label_rvo = tk.Label(frame1, text = 'Reactivo a alicuotar:')
label_rvo.pack()

rb_rvo1 = tk.Radiobutton(
	master = frame1,
	text = 'Master Mix 5x',
	value = '5x',
	variable = rvo)

rb_rvo1.pack(padx = 3, pady= 2)

rb_rvo2 = tk.Radiobutton(
	master = frame1,
	text = 'RT Mix 40x',
	value = '40x',
	variable = rvo)

rb_rvo2.pack(padx = 3, pady= 2)


################## CANTIDAD DE RACKS A USAR ##################


label_num_racks = tk.Label(frame2, text='Cantidad de racks a utilizar')
label_num_racks.pack(padx = 10)


vlist = list(range(1,10))
menu_num_racks = ttk.Combobox(master = frame2, values = vlist, state ='readonly', width=3)
menu_num_racks.set(6)

menu_num_racks.pack(padx = 10, pady = 10)


################## SETEO FALCONS ##################


label_falcons = tk.Label(frame3, text='Falcons a utilizar')
label_falcons.pack(padx = 10)



falcon_list = list(range(1,7))
menu_num_falcon = ttk.Combobox(master = frame3, values = falcon_list, state = 'readonly', width =3 )
menu_num_falcon.bind('<<ComboboxSelected>>', seleccion_num_falcons)
menu_num_falcon.pack(padx = 10, pady = 10)



label_falcons = tk.Label(frame3, text='Ingrese el volumen en cada Falcon (mL)')
label_falcons.pack(padx = 10, pady=10)

for i in range(3):

	for j in range(0, 4, 2):


		if j == 0:
			row = 'A'
		elif j == 2:
			row = 'B'

		falcon_label = tk.Label(sub_frame3, text = row + str(i+1))
		falcon_label.grid(row = j, column = i, padx = 10, pady = 3)



falcons = []


for i in range(3):

	for j in range(1 ,5 ,2):


		volfalcon = tk.Entry(sub_frame3, width = 4, state = 'disabled')
		volfalcon.insert(0,'44')
		falcons.append(volfalcon)
		volfalcon.grid(row = j, column = i, padx = 10)



sub_frame3.pack()


################## EMPAQUETADO DE LOS FRAMES ##################


frame1.grid(row = 1, column = 1, padx = 10, pady = 10)
frame2.grid(row = 2, column = 1, padx = 10, pady = 10)
frame3.grid(row = 3, column = 1, padx = 10, pady = 10)
frame4.grid(row = 4, column = 1, padx = 10, pady = 10)


################## GUARANDO LA CONFIGURACION ##################




boton_guardar = tk.Button(frame4, text ="Guardar", command = guardar)
boton_guardar.pack()


root.resizable(False, False)
root.mainloop()
