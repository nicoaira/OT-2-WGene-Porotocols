import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import configparser
import string
import subprocess
import os
from PIL import ImageTk, Image



class Keep(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.shared_data ={
            "rvo": tk.StringVar(),
            'num_racks': tk.StringVar(),
            'num_falcons': tk.StringVar(),
            'first_tip': tk.StringVar(),
            'ot_2_ip': tk.StringVar(),
            'last_tube': tk.StringVar(),
            'rack_completo_check' : tk.IntVar()
        }

        self.frames = {
            'StartPage': StartPage(self, self),
            '5x': Page5X(self, self),
            '40x': Page40X(self, self),
            'nfw': PageNFW(self, self),
            'pc': PagePC(self, self),

        }

        self.current_frame = None
        self.show_frame('StartPage')


    def show_frame(self, name):
        if self.current_frame:
            self.current_frame.forget()
        self.current_frame = self.frames[name]
        self.current_frame.pack()

        self.current_frame.update_widgets() # <-- update data in widgets


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label_rvo = tk.Label(self, text='Reactivo a alicuotar:')
        label_rvo.pack()

        rvo = self.controller.shared_data["rvo"]

        rb_rvo1 = tk.Radiobutton(
            master=self,
            text='Master Mix 5x',
            value='5x',
            variable=rvo)

        rb_rvo1.pack(padx=3, pady=2)

        rb_rvo2 = tk.Radiobutton(
            master=self,
            text='RT Mix 40x',
            value='40x',
            variable=rvo)

        rb_rvo2.pack(padx=3, pady=2)

        rb_rvo3 = tk.Radiobutton(
            master=self,
            text='Nuclease Free Water',
            value='nfw',
            variable=rvo)

        rb_rvo3.pack(padx=3, pady=2)

        rb_rvo4 = tk.Radiobutton(
            master=self,
            text='Positive Control',
            value='pc',
            variable=rvo)

        rb_rvo4.pack(padx=3, pady=2)


        button = tk.Button(self, text="Siguiente", command=self.next_page)
        button.pack()

    def update_widgets(self):
        rvo = self.controller.shared_data["rvo"].get()

    def next_page(self):
        rvo = self.controller.shared_data["rvo"].get()
        self.controller.show_frame(rvo)

class Page5X(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        def seleccion_num_falcons(event):

            num_falcon = int(menu_num_falcon.get())
            for i, v in enumerate(falcons):

                if i < num_falcon:
                    falcons[i].config(state='normal')
                    falcons[i].delete(0, tk.END)
                    falcons[i].insert(0, 44)
                else:
                    falcons[i].delete(0, 4)
                    falcons[i].config(state='disabled')

        ################## CANTIDAD DE RACKS A USAR ##################

        label_num_racks = tk.Label(self, text='Cantidad de racks a utilizar')
        label_num_racks.pack(padx=10)

        vlist = list(range(1, 10))
        menu_num_racks = ttk.Combobox(master=self, values=vlist, state='readonly', width=3)
        menu_num_racks.set(6)

        menu_num_racks.pack(padx=10, pady=10)




        ################## SETEO FALCONS ##################

        label_falcons = tk.Label(self, text='Falcons a utilizar')
        label_falcons.pack(padx=10)

        falcon_list = list(range(1, 7))
        menu_num_falcon = ttk.Combobox(master=self, values=falcon_list, state='readonly', width=3)
        menu_num_falcon.bind('<<ComboboxSelected>>', seleccion_num_falcons)
        menu_num_falcon.pack(padx=10, pady=10)

        label_falcons = tk.Label(self, text='Ingrese el volumen en cada Falcon (mL)')
        label_falcons.pack(padx=10, pady=10)

        sub_frame = tk.Frame(self)

        for i in range(3):

            for j in range(0, 4, 2):

                if j == 0:
                    row = 'A'
                elif j == 2:
                    row = 'B'

                falcon_label = tk.Label(sub_frame, text=row + str(i + 1))
                falcon_label.grid(row=j, column=i, padx=10, pady=3)

        falcons = []

        for i in range(3):

            for j in range(1, 5, 2):
                volfalcon = tk.Entry(sub_frame, width=4, state='disabled')
                volfalcon.insert(0, '44')
                falcons.append(volfalcon)
                volfalcon.grid(row=j, column=i, padx=10)

        sub_frame.pack()

        ################## SELECCION DEL ULTIMO TUBO ##################

        sub_frame2 = tk.Frame(self)


        def disable_enable_button():
            if boton_ult_tubo["state"] == "normal":
                boton_ult_tubo["state"] = "disabled"
            else:
                boton_ult_tubo["state"] = "normal"

        def popup_select_tube():

            last_tube = self.controller.shared_data["last_tube"]

            def guardar_seleccion_tubo():
                entry_ult_tubo.configure(state='normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, last_tube.get())
                entry_ult_tubo.configure(state='readonly')
                popup.destroy()

            popup = tk.Toplevel(self)
            popup.wm_title("Seleccion del ultimo tubo")

            label_tips = tk.Label(popup, text='Seleccione el ultimo tubo disponible:')
            label_tips.grid(row=1, column=1, columnspan=12, padx=10, pady=10)

            for i in range(8):
                label_tips = tk.Label(popup, text=str(i + 1))
                label_tips.grid(row=2, column=2 + i, padx=10, pady=10)

            for j in range(5):
                label_tips = tk.Label(popup, text=string.ascii_uppercase[j])
                label_tips.grid(row=3 + j, column=1, padx=10, pady=10)

            tips_list = []
            for i in range(8):
                for j in range(5):
                    tip = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=last_tube)

                    tips_list.append(tip)

                    tip.grid(row=3 + j, column=2 + i, padx=10, pady=10)

            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tubo)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()



        checkb_ult_tubo = tk.Checkbutton(sub_frame2,
                                         text="Ultimo rack completo",
                                         variable=self.controller.shared_data['rack_completo_check'],
                                         height=1,
                                         width=15,
                                         command=disable_enable_button,
                                         onvalue=1, offvalue=0)

        self.controller.shared_data['rack_completo_check'].set(1)


        checkb_ult_tubo.grid(row=1, column=1, columnspan=2, padx=3, pady=3)

        label_ult_tubo2 = tk.Label(sub_frame2, text='Ultimo tubo:')
        label_ult_tubo2.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        entry_ult_tubo = tk.Entry(sub_frame2, width=4)
        entry_ult_tubo.insert(0, 'E8')
        entry_ult_tubo.configure(state='readonly')
        entry_ult_tubo.grid(row=3, column=1, padx=3, pady=3)

        boton_ult_tubo = tk.Button(sub_frame2, text="Seleccionar", state='disable', command=popup_select_tube)
        boton_ult_tubo.grid(row=3, column=2, columnspan=1, padx=10, pady=3)

        sub_frame2.pack()


    def guardar(self):
        self.controller.shared_data["num_racks"] = menu_num_racks.get()
        self.controller.shared_data["num_falcons"] = menu_num_racks.get()


    def update_widgets(self):
        rack_completo_check = self.controller.shared_data['rack_completo_check'].get()

class Page40X(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = tk.Label(self, text="") # <-- create empty label
        self.label.pack()


    def update_widgets(self):
        rvo = self.controller.shared_data["rvo"].get()
        self.label["text"] = rvo

class PageNFW(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = tk.Label(self, text="") # <-- create empty label
        self.label.pack()


    def update_widgets(self):
        rvo = self.controller.shared_data["rvo"].get()
        self.label["text"] = rvo

class PagePC(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = tk.Label(self, text="") # <-- create empty label
        self.label.pack()


    def update_widgets(self):
        rvo = self.controller.shared_data["rvo"].get()
        self.label["text"] = rvo

if __name__ == "__main__":
    keep = Keep()
    keep.mainloop()