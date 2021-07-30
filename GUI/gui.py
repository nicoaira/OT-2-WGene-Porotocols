import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import configparser
import string
import subprocess
import os


################## CONFIGURACION IP OT-2 ##################




###############################################

root = tk.Tk()
root.title('Protocolo - WGene SARS-CoV-2 RT Detection')
root.iconbitmap("wl-icono.ico")



################## VARIABLES ##################


rvo = tk.StringVar()
first_tip = tk.StringVar()
OT2_IP = tk.StringVar()

try:
	config = configparser.ConfigParser()
	config.read('../config.ini')
	OT2_IP.set(config.get('OT-2-IP', 'ip'))

except:
	OT2_IP.set('')



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

def popup_select_tip():
	first_tip = tk.StringVar()


	def guardar_seleccion_tip():
		entry_primer_tip.configure(state='normal')
		entry_primer_tip.delete(0, tk.END)
		entry_primer_tip.insert(0, first_tip.get())
		entry_primer_tip.configure(state='readonly')
		popup.destroy()



	popup = tk.Toplevel(root)
	popup.wm_title("Seleccion del primer tip")

	label_tips = tk.Label(popup, text = 'Seleccione el primer tip disponible:')
	label_tips.grid(row = 1, column = 1, columnspan = 12, padx = 10, pady = 10)

	for i in range(12):
		label_tips = tk.Label(popup, text = str(i+1))
		label_tips.grid(row = 2, column = 2 + i, padx = 10, pady = 10)

	for j in range(8):
		label_tips = tk.Label(popup, text = string.ascii_uppercase[j])
		label_tips.grid(row = 3 + j, column = 1, padx = 10, pady = 10)


	tips_list = []
	for i in range(12):
		for j in range(8):

			tip = tk.Radiobutton(
				master = popup,
				value = string.ascii_uppercase[j]+str(i+1),
				variable = first_tip)

			tips_list.append(tip)

			tip.grid(row = 3 + j, column = 2 + i, padx = 10, pady = 10)



	B1 = ttk.Button(popup, text="Guardar seleccion", command = guardar_seleccion_tip)
	B1.grid(row = 11, column = 1, columnspan = 12, padx = 10, pady = 10)

	popup.resizable(False, False)
	popup.mainloop()

def popup_advertencia(msg):

	popup_advertencia = tk.Toplevel(root)
	popup_advertencia.wm_title("Error!")
	label = ttk.Label(popup_advertencia, text=msg)
	label.pack(side="top", fill="x", pady=10)

	B2 = ttk.Button(popup_advertencia, text="Cerrar", command=popup_advertencia.destroy)
	B2.pack()

	popup_advertencia.resizable(False, False)
	popup_advertencia.mainloop()



def guardar():

	config = configparser.ConfigParser()

	config['REACTIVO'] = {'Reactivo' : rvo.get()}
	config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
	config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}
	config['FIRST_TIP'] = {'tip': entry_primer_tip.get()}
	config['OT-2-IP'] = {'ip': OT2_IP.get()}


	falcons_dict = {}
	a = 0
	for i in range(3):
		for j in string.ascii_uppercase[:2]:
			if falcons[a].get() != "":
				falcons_dict[j+str(i+1)] = falcons[a].get()
			else:
				falcons_dict[j + str(i + 1)] = "0"
			a += 1

	config['VOL_FALCONS'] = falcons_dict

	with open('../config.ini', 'w') as configfile:
		config.write(configfile)

	#### Carga en OT-2

	upload_script = ["scp",
					 "-i",
					 "ot2_ssh_key",
					 "../config.ini",
					 "root@" + OT2_IP.get() + ":/data/user_storage"]

	try:
		p = subprocess.check_call(upload_script)
	except:
		popup_advertencia("No se pudo guardar la configuracion!")

	else:
		popup_advertencia("Configuracion guardada exitosamente!")


def opciones_avanzadas():

	def guardar_config_avanzada():
		OT2_IP.set(entry_IP.get())

		try:
			config = configparser.ConfigParser()
			config.read("../config.ini")
			config.set("OT-2-IP", "ip", OT2_IP.get())

			with open('../config.ini', 'w') as configfile:
				config.write(configfile)

		except:
			pass

		finally:
			popup_oa.destroy()


	popup_oa = tk.Toplevel(root)
	popup_oa.wm_title("Opciones Avanzadas")
	label_IP = ttk.Label(popup_oa, text='IP OT-2:')
	entry_IP = tk.Entry(popup_oa, width = 16)
	entry_IP.insert(0, OT2_IP.get())
	label_IP.grid(row = 1, column = 1, padx = 10, pady = 10)
	entry_IP.grid(row = 1, column = 2, padx = 10, pady = 10)

	B3 = ttk.Button(popup_oa, text="Guardar", command=guardar_config_avanzada)
	B3.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 10)

	popup_oa.resizable(False, False)
	popup_oa.mainloop()




################## INICIALIZACION DE FRAMES ##################


frame1 = tk.Frame()
frame2 = tk.Frame()
frame3 = tk.Frame(relief  = tk.GROOVE, borderwidth=3, pady=20)
sub_frame3 = tk.Frame(master = frame3)
frame4 = tk.Frame()
frame5 = tk.Frame()
frame6 = tk.Frame()


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


rb_rvo3 = tk.Radiobutton(
	master = frame1,
	text = 'Nuclease Free Water',
	value = 'nfw',
	variable = rvo)

rb_rvo3.pack(padx = 3, pady= 2)

rb_rvo4 = tk.Radiobutton(
	master = frame1,
	text = 'Positive Control',
	value = 'pc',
	variable = rvo)

rb_rvo4.pack(padx = 3, pady= 2)

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

################## SELECCION DEL PRIMER TIP ##################


label_tips = tk.Label(frame4, text = 'Primer tip disponible:')
label_tips.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 3)


entry_primer_tip = tk.Entry(frame4, width = 4)
entry_primer_tip.insert(0,'A1')
entry_primer_tip.configure(state='readonly')
entry_primer_tip.grid(row = 2, column = 1, padx = 10, pady = 3)

boton_select_tip = tk.Button(frame4, text ="Seleccionar", command = popup_select_tip)
boton_select_tip.grid(row = 2, column = 2, padx = 10, pady = 3)


################## BOTON GUARDAR ##################

boton_guardar = tk.Button(frame5, text ="Guardar", command = guardar)
boton_guardar.pack()

################## BOTON OPCIONES AVANZADAS ##################

boton_oa = tk.Button(frame6, text ="Opciones Avanzadas", command = opciones_avanzadas)
boton_oa.pack()


################## EMPAQUETADO DE LOS FRAMES ##################


frame1.grid(row = 1, column = 1, padx = 10, pady = 10)
frame2.grid(row = 2, column = 1, padx = 10, pady = 10)
frame3.grid(row = 3, column = 1, padx = 10, pady = 10)
frame4.grid(row = 4, column = 1, padx = 10, pady = 10)
frame5.grid(row = 5, column = 1, padx = 10, pady = 10)
frame6.grid(row = 1, column = 2, padx = 10, pady = 10)



root.resizable(False, False)
root.mainloop()
