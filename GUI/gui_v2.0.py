import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
import configparser
import string
import subprocess
from PIL import ImageTk, Image



class Keep(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('')
        self.title('Protocolo - WGene SARS-CoV-2 RT Detection')
        self.resizable(False, False)
        self.iconbitmap("wl-icono.ico") # solo en windows


        self.shared_data ={
            "rvo": tk.StringVar(),
            'num_racks': tk.StringVar(),
            'num_falcons': tk.StringVar(),
            'first_tip': tk.StringVar(),
            'ot_2_ip': tk.StringVar(),
            'last_tube': tk.StringVar(),
            'rack_completo_check' : tk.IntVar(), 
            'vel_asp_p300' : tk.StringVar(),
            'vel_disp_p300' : tk.StringVar(),
            'vel_asp_p1000' : tk.StringVar(),
            'vel_disp_p1000' : tk.StringVar(),
            'vel_mov_ot' : tk.StringVar(),
            'num_tandas' : tk.StringVar(),
            'vol_5x' : tk.StringVar(),
            'vol_40x': tk.StringVar(),
            'vol_nfw': tk.StringVar(),
            'vol_pc': tk.StringVar()

        }

        #### Valores por defecto

        self.shared_data['num_racks'].set('1')
        self.shared_data['first_tip'].set('A1')
        self.shared_data['last_tube'].set('E8')

        try:
            config = configparser.ConfigParser()
            config.read('../config.ini')

        except:
            pass

        try:
            self.shared_data['ot_2_ip'].set(config.get('OT-2-IP', 'ip'))

        except:
            self.shared_data['ot_2_ip'].set('')

        try:
            self.shared_data['vel_asp_p300'].set(config.get('VEL_P300', 'asp'))

        except:
            self.shared_data['vel_asp_p300'].set('')


        try:
            self.shared_data['vel_disp_p300'].set(config.get('VEL_P300', 'disp'))

        except:
            self.shared_data['vel_disp_p300'].set('150')

        try:
            self.shared_data['vel_asp_p1000'].set(config.get('VEL_P1000', 'asp'))

        except:
            self.shared_data['vel_asp_p1000'].set('')

        try:
            self.shared_data['vel_disp_p1000'].set(config.get('VEL_P1000', 'disp'))

        except:
            self.shared_data['vel_disp_p1000'].set('')

        try:
            self.shared_data['vel_mov_ot'].set(config.get('VEL_OT-2', 'vel_mov_ot'))

        except:
            self.shared_data['vel_mov_ot'].set('1')

        try:
            self.shared_data['vol_5x'].set(config.get('VOLUMENES_ALICUOTADO', 'vol_5x'))

        except:
            self.shared_data['vol_5x'].set('440')

        try:
            self.shared_data['vol_40x'].set(config.get('VOLUMENES_ALICUOTADO', 'vol_40x'))

        except:
            self.shared_data['vol_40x'].set('55')

        try:
            self.shared_data['vol_nfw'].set(config.get('VOLUMENES_ALICUOTADO', 'vol_nfw'))

        except:
            self.shared_data['vol_nfw'].set('1850')

        try:
            self.shared_data['vol_pc'].set(config.get('VOLUMENES_ALICUOTADO', 'vol_pc'))

        except:
            self.shared_data['vol_pc'].set('54')



        ###

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

        def next_available():
            button["state"] = "normal"

        frame_rvo = tk.Frame(self, relief = 'groove')
        frame_rvo['borderwidth'] = 2

        label_rvo = tk.Label(frame_rvo, text='Reactivo a alicuotar:')
        label_rvo.grid(row = 1, column = 1, padx = 3, pady = 4, sticky = 'w')

        rvo = self.controller.shared_data["rvo"]

        rb_rvo1 = tk.Radiobutton(
            master=frame_rvo,
            text='Master Mix 5x',
            value='5x',
            variable=rvo,
            command = next_available)



        rb_rvo1.grid(row = 2, column = 1, padx = 3, pady = 4, sticky = 'w')

        rb_rvo2 = tk.Radiobutton(
            master=frame_rvo,
            text='RT Mix 40x',
            value='40x',
            variable=rvo,
            command = next_available)

        rb_rvo2.grid(row = 3, column = 1, padx = 3, pady = 4, sticky = 'w')

        rb_rvo3 = tk.Radiobutton(
            master=frame_rvo,
            text='Nuclease Free Water',
            value='nfw',
            variable=rvo,
            command = next_available)

        rb_rvo3.grid(row = 4, column = 1, padx = 3, pady = 4, sticky = 'w')

        rb_rvo4 = tk.Radiobutton(
            master=frame_rvo,
            text='Positive Control',
            value='pc',
            variable=rvo,
            command = next_available)

        rb_rvo4.grid(row = 5, column = 1, padx = 3, pady = 4, sticky = 'w')


        frame_rvo.grid(row = 2, column = 1, padx = 3, pady = 4, sticky = 'w')


        ########### LOGO WL ############

        img = (Image.open('wl-logo.png'))
        resized_image= img.resize((150, 124), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(resized_image)

        panel_wl = tk.Label(self, image = self.logo)
        panel_wl.grid(row = 0, column = 1, padx = 3, pady = 4, rowspan = 1)


        ########### LOGO CIBIO ############

        img2 = (Image.open('cibio-logo.png'))
        resized_image2= img2.resize((136, 200), Image.ANTIALIAS)
        self.logo2 = ImageTk.PhotoImage(resized_image2)

        panel_cibio = tk.Label(self, image = self.logo2)
        panel_cibio.grid(row = 0, column = 2, padx = 3, pady = 4, rowspan = 1)



        ############# BOTON SIGUIENTE ##############


        button = tk.Button(self, text="Siguiente", command=self.next_page, state = 'disabled')
        button.grid(row = 6, column = 1, padx = 3, pady = 4, sticky = 's')



        ################## BOTON OPCIONES AVANZADAS ##################


        frame_botones = tk.Frame(self, relief = 'groove')

        def opciones_avanzadas():

            def guardar_config_avanzada():

                self.controller.shared_data['ot_2_ip'].set(entry_IP.get())
                self.controller.shared_data['vel_asp_p300'].set(entry_vel_asp_p300.get())
                self.controller.shared_data['vel_disp_p300'].set(entry_vel_disp_p300.get())
                self.controller.shared_data['vel_asp_p1000'].set(entry_vel_asp_p1000.get())
                self.controller.shared_data['vel_disp_p1000'].set(entry_vel_disp_p1000.get())
                self.controller.shared_data['vel_mov_ot'].set(scale_vel.get())
                self.controller.shared_data['vol_5x'].set(entry_5x.get())
                self.controller.shared_data['vol_40x'].set(entry_40x.get())
                self.controller.shared_data['vol_nfw'].set(entry_nfw.get())
                self.controller.shared_data['vol_pc'].set(entry_pc.get())


                try:
                    config = configparser.ConfigParser()
                    config.read("../config.ini")
                    config['OT-2-IP'] = {'ip' : self.controller.shared_data['ot_2_ip'].get()}
                    config['VEL_P300'] = {'asp' : self.controller.shared_data['vel_asp_p300'].get(),
                                        'disp' : self.controller.shared_data['vel_disp_p300'].get()}
                    config['VEL_P1000'] = {'asp' : self.controller.shared_data['vel_asp_p1000'].get(),
                                        'disp' : self.controller.shared_data['vel_disp_p1000'].get()}
                    config['VEL_OT-2'] = {'vel_mov_ot' : self.controller.shared_data['vel_mov_ot'].get()}

                    config['VOLUMENES_ALICUOTADO'] = {'vol_5x' : self.controller.shared_data['vol_5x'].get(),
                                                      'vol_40x': self.controller.shared_data['vol_40x'].get(),
                                                      'vol_nfw': self.controller.shared_data['vol_nfw'].get(),
                                                      'vol_pc': self.controller.shared_data['vol_pc'].get()
                                                      }


                    with open('../config.ini', 'w') as configfile:
                        config.write(configfile)

                except Exception as e:
                    print(e)

                finally:
                    popup_oa.destroy()


            popup_oa = tk.Toplevel(self)
            popup_oa.wm_title("Opciones Avanzadas")



            frame_ip = tk.Frame(popup_oa, relief='groove')
            frame_ip['borderwidth'] = 2

            label_config_ip = ttk.Label(frame_ip, text='Configuracion de IP')
            label_IP = ttk.Label(frame_ip, text='IP OT-2:')
            entry_IP = tk.Entry(frame_ip, width = 16)
            entry_IP.insert(0, self.controller.shared_data['ot_2_ip'].get())
            label_config_ip.grid(row = 1, column = 1, padx = 3, pady = 10, columnspan = 2)
            label_IP.grid(row = 2, column = 1, padx = 3, pady = 10, sticky = 'W')
            entry_IP.grid(row = 2, column = 2, padx = 3, pady = 10, sticky = 'E')


            frame_ip.grid(row = 1, column = 1, columnspan=6, padx = 3, pady = 10, ipadx = 5)



            frame_p300 = tk.Frame(popup_oa, relief='groove')
            frame_p300['borderwidth'] = 2


            label_p300 = ttk.Label(frame_p300, text='Configuracion p300')

            label_vel_asp_p300 = ttk.Label(frame_p300, text='Velocidad de aspiracion (μL/seg):')
            entry_vel_asp_p300 = tk.Entry(frame_p300, width = 5)
            entry_vel_asp_p300.insert(0, self.controller.shared_data['vel_asp_p300'].get())
            label_p300.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan = 2)
            label_vel_asp_p300.grid(row = 2, column = 1, padx = 3, pady = 10)
            entry_vel_asp_p300.grid(row = 2, column = 2, padx = 3, pady = 10)

            label_vel_disp_p300 = ttk.Label(frame_p300, text='Velocidad de dispensado (μL/seg):')
            entry_vel_disp_p300 = tk.Entry(frame_p300, width = 5)
            entry_vel_disp_p300.insert(0, self.controller.shared_data['vel_disp_p300'].get())
            label_vel_disp_p300.grid(row = 3, column = 1, padx = 3, pady = 10)
            entry_vel_disp_p300.grid(row = 3, column = 2, padx = 3, pady = 10)

            frame_p300.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 10)



            frame_p1000 = tk.Frame(popup_oa, relief='groove')
            frame_p1000['borderwidth'] = 2

            label_p1000 = ttk.Label(frame_p1000, text='Configuracion p1000')

            label_vel_asp_p1000 = ttk.Label(frame_p1000, text='Velocidad de aspiracion (μL/seg):')
            entry_vel_asp_p1000 = tk.Entry(frame_p1000, width = 5)
            entry_vel_asp_p1000.insert(0, self.controller.shared_data['vel_asp_p1000'].get())
            label_p1000.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan = 2)
            label_vel_asp_p1000.grid(row = 2, column = 1, padx = 3, pady = 10)
            entry_vel_asp_p1000.grid(row = 2, column = 2, padx = 3, pady = 10)

            label_vel_disp_p1000 = ttk.Label(frame_p1000, text='Velocidad de dispensado (μL/seg):')
            entry_vel_disp_p1000 = tk.Entry(frame_p1000, width = 5)
            entry_vel_disp_p1000.insert(0, self.controller.shared_data['vel_disp_p1000'].get())
            label_vel_disp_p1000.grid(row = 3, column = 1, padx = 3, pady = 10)
            entry_vel_disp_p1000.grid(row = 3, column = 2, padx = 3, pady = 10)


            frame_p1000.grid(row = 2, column = 4, columnspan = 2, padx = 10, pady = 10)



            frame_vel_ot_2 = tk.Frame(popup_oa, relief='groove')
            frame_vel_ot_2['borderwidth'] = 2

            label_config_ot_2 = ttk.Label(frame_vel_ot_2, text='Configuracion movimiento OT-2')

            label_config_ot_2.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan = 2)

            scale_vel = tk.Scale(frame_vel_ot_2, from_=0.5, to=1.5, orient = 'horizontal',
                tickinterval = 0.5, length = 300, resolution = 0.05,
                label = 'Factor de velocidad', variable = controller.shared_data['vel_mov_ot'])
            scale_vel.grid(row = 2, column = 1, padx = 3, pady = 10)

            frame_vel_ot_2.grid(row = 3, column = 1, columnspan = 6, padx = 10, pady = 10)


            frame_volumenes = tk.Frame(popup_oa, relief = 'groove')
            frame_volumenes['borderwidth'] = 2

            label_volumenes = tk.Label(frame_volumenes, text = 'Configuracion de volumenes de alicuotado (μL)')
            label_volumenes.grid(row = 1, column = 1, columnspan = 4, padx = 10, pady = 10)

            label_5x = tk.Label(frame_volumenes, text = 'Master Mix 5x:')
            entry_5x = tk.Entry(frame_volumenes, width = 4)
            entry_5x.insert(0, self.controller.shared_data['vol_5x'].get())
            label_5x.grid(row = 2, column = 1, columnspan = 1, padx = 3, pady = 10, sticky = 'E')
            entry_5x.grid(row = 2, column = 2, columnspan = 1, padx = 3, pady = 10, sticky = 'W')

            label_40x = tk.Label(frame_volumenes, text = 'RT Mix 40x:')
            entry_40x = tk.Entry(frame_volumenes, width = 4)
            label_40x.grid(row = 3, column = 1, columnspan = 1, padx = 3, pady = 10, sticky = 'E')
            entry_40x.grid(row = 3, column = 2, columnspan = 1, padx = 3, pady = 10, sticky = 'W')
            entry_40x.insert(0, self.controller.shared_data['vol_40x'].get())

            label_nfw = tk.Label(frame_volumenes, text = 'Nuclease Free Water:')
            entry_nfw = tk.Entry(frame_volumenes, width = 4)
            label_nfw.grid(row = 4, column = 1, columnspan = 1, padx = 3, pady = 10, sticky = 'E')
            entry_nfw.grid(row = 4, column = 2, columnspan = 1, padx = 3, pady = 10, sticky = 'W')
            entry_nfw.insert(0, self.controller.shared_data['vol_nfw'].get())

            label_pc = tk.Label(frame_volumenes, text = 'Positive Control:')
            entry_pc = tk.Entry(frame_volumenes, width = 4)
            label_pc.grid(row = 5, column = 1, columnspan = 1, padx = 3, pady = 10, sticky = 'E')
            entry_pc.grid(row = 5, column = 2, columnspan = 1, padx = 3, pady = 10, sticky = 'W')
            entry_pc.insert(0, self.controller.shared_data['vol_pc'].get())

            frame_volumenes.grid(row = 4, column = 1, columnspan = 6, padx = 10, pady = 10)


            B3 = ttk.Button(popup_oa, text="Volver", command=popup_oa.destroy)
            B3.grid(row = 5, column = 2, columnspan = 2, padx = 10, pady = 10)

            B4 = ttk.Button(popup_oa, text="Guardar", command=guardar_config_avanzada)
            B4.grid(row = 5, column = 3, columnspan = 2, padx = 10, pady = 10)



            popup_oa.resizable(False, False)
            popup_oa.mainloop()

        boton_oa = tk.Button(frame_botones, text ="Opciones Avanzadas", command = opciones_avanzadas)
        boton_oa.grid(row = 1, column = 1, padx = 3, pady = 4)



    ################## BOTON INTRUCCIONES ##################

        def instrucciones():


            popup_info = tk.Toplevel(self)
            popup_info.wm_title("Manual de instrucciones")

            with open('instrucciones.txt', 'r') as file:
                manual = file.read()


            text_manual = tk.Text(popup_info, width = 110)
            # scroll = tk.Scrollbar(popup_info)
            # text_manual.configure(yscrollcommand=scroll.set)
            text_manual.insert(tk.END, manual)
            text_manual['state'] = 'disabled'
            text_manual.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 10)
    


            B4 = ttk.Button(popup_info, text="Cerrar", command=popup_info.destroy)
            B4.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 10)

            popup_info.resizable(False, False)
            popup_info.mainloop()


        boton_intrucciones = tk.Button(frame_botones, text ="Instrucciones", command = instrucciones)
        boton_intrucciones.grid(row = 2, column = 1, padx = 3, pady = 4)


        ####### BOTON SALIR #######

        boton_intrucciones = tk.Button(frame_botones, text ="Cerrar", command = controller.destroy)
        boton_intrucciones.grid(row = 3, column = 1, padx = 3, pady = 4)


        frame_botones.grid(row = 2, column = 2, padx = 3, pady = 4, ipady = 10)


    def update_widgets(self):
        pass

    def next_page(self):
        rvo = self.controller.shared_data["rvo"].get()
        self.controller.show_frame(rvo)

class Page5X(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        def guardar():

            config = configparser.ConfigParser()

            config['REACTIVO'] = {'Reactivo' : controller.shared_data['rvo'].get()}
            config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
            config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}
            config['NUM_TANDAS'] = {'num_tandas' : 1}
            config['FIRST_TIP'] = {'tip': controller.shared_data['first_tip'].get()}
            config['OT-2-IP'] = {'ip': controller.shared_data['ot_2_ip'].get()}
            config['LAST_TUBE'] = {'tube': controller.shared_data['last_tube'].get()}
            config['VEL_P300'] = {'asp': controller.shared_data['vel_asp_p300'].get(), 
                                'disp': controller.shared_data['vel_disp_p300'].get()}
            config['VEL_P1000'] = {'asp': controller.shared_data['vel_asp_p1000'].get(), 
                                'disp': controller.shared_data['vel_disp_p1000'].get()}
            config['VEL_OT-2'] = {'vel_mov_ot': controller.shared_data['vel_mov_ot'].get()}
            config['VOLUMENES_ALICUOTADO'] = {'vol_5x': self.controller.shared_data['vol_5x'].get(),
                                              'vol_40x': self.controller.shared_data['vol_40x'].get(),
                                              'vol_nfw': self.controller.shared_data['vol_nfw'].get(),
                                              'vol_pc': self.controller.shared_data['vol_pc'].get()
                                              }


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

            OT2_IP = controller.shared_data['ot_2_ip'].get()

            upload_script = ["scp",
                             "-i",
                             "ot2_ssh_key",
                             "../config.ini",
                             "root@" + OT2_IP + ":/data/user_storage"]


            try:                 
                p = subprocess.check_call(upload_script, timeout = 7)
                tkmb.showinfo(title = "Atencion!", message = "Configuracion guardada exitosamente!")

            except subprocess.TimeoutExpired:
                tkmb.showerror(title='Error!', message='No se pudo guardar la configuracion!')

                


        def seleccion_vol_falcons(event):

            num_falcon = int(menu_num_falcon.get())
            for i, v in enumerate(falcons):

                if i < num_falcon:
                    falcons[i].config(state='normal')
                    falcons[i].delete(0, tk.END)
                    falcons[i].insert(0, 44)
                else:
                    falcons[i].delete(0, tk.END)
                    falcons[i].config(state='disabled')

        ################## CANTIDAD DE RACKS A USAR ##################

        sub_frame0 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_num_racks = tk.Label(sub_frame0, text='Cantidad de racks a utilizar')
        label_num_racks.pack(padx=10)

        vlist = list(range(1, 10))
        menu_num_racks = ttk.Combobox(master=sub_frame0, values=vlist, state='readonly', width=3)
        menu_num_racks.set(6)

        menu_num_racks.pack(padx=10, pady=10)

        sub_frame0.grid(row=3, column=1, padx=10, pady = 5)




        ################## SETEO FALCONS ##################


        sub_frame1 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        label_falcons = tk.Label(sub_frame1, text='Cantidad de Falcons a utilizar')
        label_falcons.pack(padx=10)

        falcon_list = list(range(1, 7))
        menu_num_falcon = ttk.Combobox(master=sub_frame1, values=falcon_list, state='readonly', width=3)
        menu_num_falcon.bind('<<ComboboxSelected>>', seleccion_vol_falcons)
        menu_num_falcon.pack(padx=10, pady=10)


        sub_frame1_1 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_falcons = tk.Label(sub_frame1_1, text='Ingrese el volumen en cada Falcon (mL)')
        label_falcons.grid(row=0, column=0, padx=10, pady=3, columnspan = 3)


        for i in range(3):

            for j in range(0, 4, 2):

                if j == 0:
                    row = 'A'
                elif j == 2:
                    row = 'B'

                falcon_label = tk.Label(sub_frame1_1, text=row + str(i + 1))
                falcon_label.grid(row=j+1, column=i, padx=3, pady=3)

        falcons = []

        for i in range(3):

            for j in range(1, 5, 2):
                volfalcon = tk.Entry(sub_frame1_1, width=4, state='disabled')
                volfalcon.insert(0, '44')
                falcons.append(volfalcon)
                volfalcon.grid(row=j+1, column=i, padx=3)


        sub_frame1.grid(row=1, column=1, padx=10, pady = 5)
        sub_frame1_1.grid(row=2, column=1, padx=10, pady = 5, ipady = 10)

        ################## SELECCION DEL ULTIMO TUBO ##################

        sub_frame2 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        def disable_enable_button():
            if boton_ult_tubo["state"] == "normal":
                boton_ult_tubo["state"] = "disabled"
                self.controller.shared_data["last_tube"].set('E8')
                entry_ult_tubo.configure(state = 'normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
                entry_ult_tubo.configure(state='readonly')

            else:
                boton_ult_tubo["state"] = "normal"

        def popup_select_tube():


            def guardar_seleccion_tubo():
                entry_ult_tubo.configure(state='normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
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

            tubes_list = []
            for i in range(8):
                for j in range(5):
                    tube = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=controller.shared_data["last_tube"])

                    tubes_list.append(tube)

                    tube.grid(row=3 + j, column=2 + i, padx=10, pady=10)


            self.controller.shared_data["last_tube"].set('E8')


            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tubo)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()




        checkb_ult_tubo = tk.Checkbutton(sub_frame2,
                                         text="Ultimo rack completo",
                                         variable=self.controller.shared_data['rack_completo_check'],
                                         height=1,
                                         width=21,
                                         command=disable_enable_button,
                                         onvalue=1, offvalue=0)

        self.controller.shared_data['rack_completo_check'].set(1)


        checkb_ult_tubo.grid(row=1, column=1, columnspan=3, padx=3, pady=3)

        label_ult_tubo2 = tk.Label(sub_frame2, text='Ultimo tubo:')
        label_ult_tubo2.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        entry_ult_tubo = tk.Entry(sub_frame2, width=4)
        entry_ult_tubo.insert(0, 'E8')
        entry_ult_tubo.configure(state='readonly')
        entry_ult_tubo.grid(row=3, column=1, padx=3, pady=3)

        boton_ult_tubo = tk.Button(sub_frame2, text="Seleccionar", state='disable', command=popup_select_tube)
        boton_ult_tubo.grid(row=3, column=2, padx=3, pady=3, sticky = 'W')





        ################## SELECCION DEL PRIMER TIP ##################

        def popup_select_tip():
            first_tip = controller.shared_data['first_tip']

            def guardar_seleccion_tip():
                entry_primer_tip.configure(state='normal')
                entry_primer_tip.delete(0, tk.END)
                entry_primer_tip.insert(0, first_tip.get())
                entry_primer_tip.configure(state='readonly')
                popup.destroy()

            popup = tk.Toplevel(self)
            popup.wm_title("Seleccion del primer tip")

            label_tips = tk.Label(popup, text='Seleccione el primer tip disponible:')
            label_tips.grid(row=1, column=1, columnspan=12, padx=10, pady=10)

            for i in range(12):
                label_tips = tk.Label(popup, text=str(i + 1))
                label_tips.grid(row=2, column=2 + i, padx=10, pady=10)

            for j in range(8):
                label_tips = tk.Label(popup, text=string.ascii_uppercase[j])
                label_tips.grid(row=3 + j, column=1, padx=10, pady=10)

            tips_list = []
            for i in range(12):
                for j in range(8):
                    tip = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=first_tip)

                    tips_list.append(tip)

                    tip.grid(row=3 + j, column=2 + i, padx=10, pady=10)

            first_tip.set('A1')

            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tip)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()


        label_tips = tk.Label(sub_frame2, text='Primer tip disponible:')
        label_tips.grid(row=4, column=1, columnspan=2, padx=10, pady=3)

        entry_primer_tip = tk.Entry(sub_frame2, width=4)
        entry_primer_tip.insert(0, 'A1')
        entry_primer_tip.configure(state='readonly')
        entry_primer_tip.grid(row=5, column=1, padx=5, pady=3)

        boton_select_tip = tk.Button(sub_frame2, text="Seleccionar", command=popup_select_tip)
        boton_select_tip.grid(row=5, column=2, padx=3, pady=3, sticky = 'W')


        sub_frame2.grid(row=4, column=1, padx=10, pady = 5, ipady = 3)


        ################## BOTON GUARDAR ##################

        frame_botones = tk.Frame(self)

        boton_guardar = tk.Button(frame_botones, text ="Guardar", command = guardar)
        boton_guardar.grid(row=1, column=2, padx=10, pady = 5)


        ################## BOTON VOLVER ##################


        def regresar():
            self.controller.show_frame('StartPage')

        boton_guardar = tk.Button(frame_botones, text ="Volver", command = regresar)
        boton_guardar.grid(row=1, column=1, padx=10, pady = 5)

        frame_botones.grid(row=6, column=1, padx=10, pady = 5)



    def update_widgets(self):
        pass


class Page40X(tk.Frame):


    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller



        def guardar():

            config = configparser.ConfigParser()

            config['REACTIVO'] = {'Reactivo' : controller.shared_data['rvo'].get()}
            config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
            config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}
            config['NUM_TANDAS'] = {'num_tandas' : menu_num_tandas.get()}
            config['FIRST_TIP'] = {'tip': controller.shared_data['first_tip'].get()}
            config['OT-2-IP'] = {'ip': controller.shared_data['ot_2_ip'].get()}
            config['LAST_TUBE'] = {'tube': controller.shared_data['last_tube'].get()}
            config['VEL_P300'] = {'asp': controller.shared_data['vel_asp_p300'].get(), 
                                'disp': controller.shared_data['vel_disp_p300'].get()}
            config['VEL_P1000'] = {'asp': controller.shared_data['vel_asp_p1000'].get(), 
                                'disp': controller.shared_data['vel_disp_p1000'].get()}
            config['VEL_OT-2'] = {'vel_mov_ot': controller.shared_data['vel_mov_ot'].get()}
            config['VOLUMENES_ALICUOTADO'] = {'vol_5x': self.controller.shared_data['vol_5x'].get(),
                                              'vol_40x': self.controller.shared_data['vol_40x'].get(),
                                              'vol_nfw': self.controller.shared_data['vol_nfw'].get(),
                                              'vol_pc': self.controller.shared_data['vol_pc'].get()
                                              }


            with open('../config.ini', 'w') as configfile:
                config.write(configfile)

            #### Carga en OT-2

            OT2_IP = controller.shared_data['ot_2_ip'].get()

            upload_script = ["scp",
                             "-i",
                             "ot2_ssh_key",
                             "../config.ini",
                             "root@" + OT2_IP + ":/data/user_storage"]


            try:                 
                p = subprocess.check_call(upload_script, timeout = 7)
                tkmb.showinfo(title = "Atencion!", message = "Configuracion guardada exitosamente!")

            except subprocess.TimeoutExpired:
                tkmb.showerror(title='Error!', message='No se pudo guardar la configuracion!')

                


        def seleccion_vol_falcons(event):

            num_falcon = int(menu_num_falcon.get())
            for i, v in enumerate(falcons):

                if i < num_falcon:
                    falcons[i].config(state='normal')
                    falcons[i].delete(0, tk.END)
                    falcons[i].insert(0, 50)
                else:
                    falcons[i].delete(0, tk.END)
                    falcons[i].config(state='disabled')

        ################## CANTIDAD DE RACKS A USAR ##################

        sub_frame0 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_num_racks = tk.Label(sub_frame0, text='Cantidad de racks por tanda')
        label_num_racks.pack(padx=10)

        vlist = list(range(1, 10))
        menu_num_racks = ttk.Combobox(master=sub_frame0, values=vlist, state='readonly', width=3)
        menu_num_racks.set(6)

        menu_num_racks.pack(padx=10, pady=10)

        sub_frame0.grid(row=3, column=1, padx=10, pady = 5, ipady = 5)


        ################## CANTIDAD DE TANDAS ##################

        sub_frame3 = tk.Frame(self)

        label_num_tandas = tk.Label(sub_frame0, text='Cantidad de tandas')
        label_num_tandas.pack(padx=10)

        tlist = list(range(1, 11))
        menu_num_tandas = ttk.Combobox(master=sub_frame0, values=tlist, state='readonly', width=3)
        menu_num_tandas.set(1)

        menu_num_tandas.pack(padx=10, pady=1)

        sub_frame3.grid(row=4, column=1, padx=10, pady = 5)



        ################## SETEO FALCONS ##################


        sub_frame1 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_falcons = tk.Label(sub_frame1, text='Cantidad de tubos 2,5 mL RT-Mix a alicuotar')
        label_falcons.pack(padx=10)

        falcon_list = list(range(1, 29))
        menu_num_falcon = ttk.Combobox(master=sub_frame1, values=falcon_list, state='readonly', width=3)
        menu_num_falcon.pack(padx=10, pady=10)

        sub_frame1.grid(row=1, column=1, padx=10, pady = 5)

        ################## SELECCION DEL ULTIMO TUBO ##################

        sub_frame2 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        def disable_enable_button():
            if boton_ult_tubo["state"] == "normal":
                boton_ult_tubo["state"] = "disabled"
                self.controller.shared_data["last_tube"].set('E8')
                entry_ult_tubo.configure(state = 'normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
                entry_ult_tubo.configure(state='readonly')

            else:
                boton_ult_tubo["state"] = "normal"

        def popup_select_tube():


            def guardar_seleccion_tubo():
                entry_ult_tubo.configure(state='normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
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

            tubes_list = []
            for i in range(8):
                for j in range(5):
                    tube = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=controller.shared_data["last_tube"])

                    tubes_list.append(tube)

                    tube.grid(row=3 + j, column=2 + i, padx=10, pady=10)


            self.controller.shared_data["last_tube"].set('E8')


            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tubo)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()




        checkb_ult_tubo = tk.Checkbutton(sub_frame2,
                                         text="Ultimo rack completo",
                                         variable=self.controller.shared_data['rack_completo_check'],
                                         height=1,
                                         width=21,
                                         command=disable_enable_button,
                                         onvalue=1, offvalue=0)

        self.controller.shared_data['rack_completo_check'].set(1)


        checkb_ult_tubo.grid(row=1, column=1, columnspan=3, padx=3, pady=3)

        label_ult_tubo2 = tk.Label(sub_frame2, text='Ultimo tubo:')
        label_ult_tubo2.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        entry_ult_tubo = tk.Entry(sub_frame2, width=4)
        entry_ult_tubo.insert(0, 'E8')
        entry_ult_tubo.configure(state='readonly')
        entry_ult_tubo.grid(row=3, column=1, padx=3, pady=3)

        boton_ult_tubo = tk.Button(sub_frame2, text="Seleccionar", state='disable', command=popup_select_tube)
        boton_ult_tubo.grid(row=3, column=2, padx=3, pady=3, sticky = 'W')





        ################## SELECCION DEL PRIMER TIP ##################

        def popup_select_tip():
            first_tip = controller.shared_data['first_tip']

            def guardar_seleccion_tip():
                entry_primer_tip.configure(state='normal')
                entry_primer_tip.delete(0, tk.END)
                entry_primer_tip.insert(0, first_tip.get())
                entry_primer_tip.configure(state='readonly')
                popup.destroy()

            popup = tk.Toplevel(self)
            popup.wm_title("Seleccion del primer tip")

            label_tips = tk.Label(popup, text='Seleccione el primer tip disponible:')
            label_tips.grid(row=1, column=1, columnspan=12, padx=10, pady=10)

            for i in range(12):
                label_tips = tk.Label(popup, text=str(i + 1))
                label_tips.grid(row=2, column=2 + i, padx=10, pady=10)

            for j in range(8):
                label_tips = tk.Label(popup, text=string.ascii_uppercase[j])
                label_tips.grid(row=3 + j, column=1, padx=10, pady=10)

            tips_list = []
            for i in range(12):
                for j in range(8):
                    tip = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=first_tip)

                    tips_list.append(tip)

                    tip.grid(row=3 + j, column=2 + i, padx=10, pady=10)

            first_tip.set('A1')

            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tip)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()


        label_tips = tk.Label(sub_frame2, text='Primer tip disponible:')
        label_tips.grid(row=4, column=1, columnspan=2, padx=10, pady=3)

        entry_primer_tip = tk.Entry(sub_frame2, width=4)
        entry_primer_tip.insert(0, 'A1')
        entry_primer_tip.configure(state='readonly')
        entry_primer_tip.grid(row=5, column=1, padx=5, pady=3)

        boton_select_tip = tk.Button(sub_frame2, text="Seleccionar", command=popup_select_tip)
        boton_select_tip.grid(row=5, column=2, padx=3, pady=3, sticky = 'W')


        sub_frame2.grid(row=5, column=1, padx=10, pady = 5, ipady = 3)


        ################## BOTON GUARDAR ##################

        frame_botones = tk.Frame(self)

        boton_guardar = tk.Button(frame_botones, text ="Guardar", command = guardar)
        boton_guardar.grid(row=1, column=2, padx=10, pady = 5)


        ################## BOTON VOLVER ##################


        def regresar():
            self.controller.show_frame('StartPage')

        boton_guardar = tk.Button(frame_botones, text ="Volver", command = regresar)
        boton_guardar.grid(row=1, column=1, padx=10, pady = 5)

        frame_botones.grid(row=6, column=1, padx=10, pady = 5)





    def update_widgets(self):
        pass

class PageNFW(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        def guardar():

            config = configparser.ConfigParser()

            config['REACTIVO'] = {'Reactivo' : controller.shared_data['rvo'].get()}
            config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
            config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}
            config['NUM_TANDAS'] = {'num_tandas' : 1}
            config['FIRST_TIP'] = {'tip': controller.shared_data['first_tip'].get()}
            config['OT-2-IP'] = {'ip': controller.shared_data['ot_2_ip'].get()}
            config['LAST_TUBE'] = {'tube': controller.shared_data['last_tube'].get()}
            config['VEL_P300'] = {'asp': controller.shared_data['vel_asp_p300'].get(), 
                                'disp': controller.shared_data['vel_disp_p300'].get()}
            config['VEL_P1000'] = {'asp': controller.shared_data['vel_asp_p1000'].get(), 
                                'disp': controller.shared_data['vel_disp_p1000'].get()}
            config['VEL_OT-2'] = {'vel_mov_ot': controller.shared_data['vel_mov_ot'].get()}
            config['VOLUMENES_ALICUOTADO'] = {'vol_5x': self.controller.shared_data['vol_5x'].get(),
                                              'vol_40x': self.controller.shared_data['vol_40x'].get(),
                                              'vol_nfw': self.controller.shared_data['vol_nfw'].get(),
                                              'vol_pc': self.controller.shared_data['vol_pc'].get()
                                              }


            falcons_dict_9 = {}
            a = 0
            for i in range(3):
                for j in string.ascii_uppercase[:2]:
                    if falcons[a].get() != "":
                        falcons_dict_9[j+str(i+1)] = falcons[a].get()
                    else:
                        falcons_dict_9[j + str(i + 1)] = "0"
                    a += 1

            a = 6

            falcons_dict_11 = {}

            for i in range(3):
                for j in string.ascii_uppercase[:2]:
                    if falcons[a].get() != "":
                        falcons_dict_11[j+str(i+1)] = falcons[a].get()
                    else:
                        falcons_dict_11[j + str(i + 1)] = "0"
                    a += 1

            config['VOL_FALCONS_9'] = falcons_dict_9
            config['VOL_FALCONS_11'] = falcons_dict_11

            with open('../config.ini', 'w') as configfile:
                config.write(configfile)

            #### Carga en OT-2

            OT2_IP = controller.shared_data['ot_2_ip'].get()

            upload_script = ["scp",
                             "-i",
                             "ot2_ssh_key",
                             "../config.ini",
                             "root@" + OT2_IP + ":/data/user_storage"]


            try:                 
                p = subprocess.check_call(upload_script, timeout = 7)
                tkmb.showinfo(title = "Atencion!", message = "Configuracion guardada exitosamente!")

            except subprocess.TimeoutExpired:
                tkmb.showerror(title='Error!', message='No se pudo guardar la configuracion!')


                


        def seleccion_vol_falcons(event):

            num_falcon = int(menu_num_falcon.get())
            for i, v in enumerate(falcons):

                if i < num_falcon:
                    falcons[i].config(state='normal')
                    falcons[i].delete(0, tk.END)
                    falcons[i].insert(0, 50)
                else:
                    falcons[i].delete(0, tk.END)
                    falcons[i].config(state='disabled')

        ################## CANTIDAD DE RACKS A USAR ##################

        sub_frame0 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_num_racks = tk.Label(sub_frame0, text='Cantidad de racks a utilizar')
        label_num_racks.pack(padx=10)

        vlist = list(range(1, 8))
        menu_num_racks = ttk.Combobox(master=sub_frame0, values=vlist, state='readonly', width=3)
        menu_num_racks.set(6)

        menu_num_racks.pack(padx=10, pady=10)

        sub_frame0.grid(row=5, column=1, padx=10, pady = 5)




        ################## SETEO FALCONS ##################


        sub_frame1 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        label_falcons = tk.Label(sub_frame1, text='Cantidad de Falcons a utilizar')
        label_falcons.pack(padx=10)

        falcon_list = list(range(1, 13))
        menu_num_falcon = ttk.Combobox(master=sub_frame1, values=falcon_list, state='readonly', width=3)
        menu_num_falcon.bind('<<ComboboxSelected>>', seleccion_vol_falcons)
        menu_num_falcon.pack(padx=10, pady=10)




        ##### Primer rack #####



        sub_frame1_0 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_falcons = tk.Label(sub_frame1_0, text='Ingrese el volumen en cada Falcon (mL)')
        label_falcons.grid(row=0, column=0, columnspan = 3, padx=10, pady=3)

        sub_frame1_1 = tk.Frame(sub_frame1_0, relief = 'groove', borderwidth = 2)

        label_rack_9 = tk.Label(sub_frame1_1, text='Rack posición 9')
        label_rack_9.grid(row=1, column=0, columnspan = 3, padx=10, pady=3)


        for i in range(3):

            for j in range(0, 4, 2):

                if j == 0:
                    row = 'A'
                elif j == 2:
                    row = 'B'

                falcon_label = tk.Label(sub_frame1_1, text=row + str(i + 1))
                falcon_label.grid(row=j+2, column=i, padx=10, pady=3)

        falcons = []


        for i in range(3):

            for j in range(1, 5, 2):
                volfalcon = tk.Entry(sub_frame1_1, width=4, state='disabled')
                volfalcon.insert(0, '50')
                falcons.append(volfalcon)
                volfalcon.grid(row=j+2, column=i, padx=10)



        ##### Segundo rack #####

        sub_frame1_2 = tk.Frame(sub_frame1_0, relief = 'groove', borderwidth = 2)

        label_rack_11 = tk.Label(sub_frame1_2, text='Rack posición 11')
        label_rack_11.grid(row=1, column=0, columnspan = 3, padx=10, pady=3)



        for i in range(3):

            for j in range(0, 4, 2):

                if j == 0:
                    row = 'A'
                elif j == 2:
                    row = 'B'

                falcon_label = tk.Label(sub_frame1_2, text=row + str(i + 1))
                falcon_label.grid(row=j+2, column=i, padx=10, pady=3)


        for i in range(3):

            for j in range(1, 5, 2):
                volfalcon = tk.Entry(sub_frame1_2, width=4, state='disabled')
                volfalcon.insert(0, '50')
                falcons.append(volfalcon)
                volfalcon.grid(row=j+2, column=i, padx=10)



        sub_frame1.grid(row=1, column=1, padx=10, pady = 5)
        sub_frame1_0.grid(row=2, column=1, padx=10, pady = 5)
        sub_frame1_1.grid(row=1, column=1, padx=10, pady = 5, ipady = 5)

        sub_frame1_2.grid(row=1, column=2, padx=10, pady = 5, ipady = 5)


        ################## SELECCION DEL ULTIMO TUBO ##################

        sub_frame2 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        def disable_enable_button():
            if boton_ult_tubo["state"] == "normal":
                boton_ult_tubo["state"] = "disabled"
                self.controller.shared_data["last_tube"].set('E8')
                entry_ult_tubo.configure(state = 'normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
                entry_ult_tubo.configure(state='readonly')

            else:
                boton_ult_tubo["state"] = "normal"

        def popup_select_tube():


            def guardar_seleccion_tubo():
                entry_ult_tubo.configure(state='normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
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

            tubes_list = []
            for i in range(8):
                for j in range(5):
                    tube = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=controller.shared_data["last_tube"])

                    tubes_list.append(tube)

                    tube.grid(row=3 + j, column=2 + i, padx=10, pady=10)


            self.controller.shared_data["last_tube"].set('E8')


            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tubo)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()




        checkb_ult_tubo = tk.Checkbutton(sub_frame2,
                                         text="Ultimo rack completo",
                                         variable=self.controller.shared_data['rack_completo_check'],
                                         height=1,
                                         width=21,
                                         command=disable_enable_button,
                                         onvalue=1, offvalue=0)

        self.controller.shared_data['rack_completo_check'].set(1)


        checkb_ult_tubo.grid(row=1, column=1, columnspan=3, padx=3, pady=3)

        label_ult_tubo2 = tk.Label(sub_frame2, text='Ultimo tubo:')
        label_ult_tubo2.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        entry_ult_tubo = tk.Entry(sub_frame2, width=4)
        entry_ult_tubo.insert(0, 'E8')
        entry_ult_tubo.configure(state='readonly')
        entry_ult_tubo.grid(row=3, column=1, padx=3, pady=3)

        boton_ult_tubo = tk.Button(sub_frame2, text="Seleccionar", state='disable', command=popup_select_tube)
        boton_ult_tubo.grid(row=3, column=2, padx=3, pady=3, sticky = 'W')





        ################## SELECCION DEL PRIMER TIP ##################

        def popup_select_tip():
            first_tip = controller.shared_data['first_tip']

            def guardar_seleccion_tip():
                entry_primer_tip.configure(state='normal')
                entry_primer_tip.delete(0, tk.END)
                entry_primer_tip.insert(0, first_tip.get())
                entry_primer_tip.configure(state='readonly')
                popup.destroy()

            popup = tk.Toplevel(self)
            popup.wm_title("Seleccion del primer tip")

            label_tips = tk.Label(popup, text='Seleccione el primer tip disponible:')
            label_tips.grid(row=1, column=1, columnspan=12, padx=10, pady=10)

            for i in range(12):
                label_tips = tk.Label(popup, text=str(i + 1))
                label_tips.grid(row=2, column=2 + i, padx=10, pady=10)

            for j in range(8):
                label_tips = tk.Label(popup, text=string.ascii_uppercase[j])
                label_tips.grid(row=3 + j, column=1, padx=10, pady=10)

            tips_list = []
            for i in range(12):
                for j in range(8):
                    tip = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=first_tip)

                    tips_list.append(tip)

                    tip.grid(row=3 + j, column=2 + i, padx=10, pady=10)

            first_tip.set('A1')

            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tip)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()


        label_tips = tk.Label(sub_frame2, text='Primer tip disponible:')
        label_tips.grid(row=4, column=1, columnspan=2, padx=10, pady=3)

        entry_primer_tip = tk.Entry(sub_frame2, width=4)
        entry_primer_tip.insert(0, 'A1')
        entry_primer_tip.configure(state='readonly')
        entry_primer_tip.grid(row=5, column=1, padx=5, pady=3)

        boton_select_tip = tk.Button(sub_frame2, text="Seleccionar", command=popup_select_tip)
        boton_select_tip.grid(row=5, column=2, padx=3, pady=3, sticky = 'W')


        sub_frame2.grid(row=6, column=1, padx=10, pady = 5, ipady = 3)

        ################## BOTON GUARDAR ##################

        frame_botones = tk.Frame(self)

        boton_guardar = tk.Button(frame_botones, text ="Guardar", command = guardar)
        boton_guardar.grid(row=1, column=2, padx=10, pady = 5)


        ################## BOTON VOLVER ##################


        def regresar():
            self.controller.show_frame('StartPage')

        boton_guardar = tk.Button(frame_botones, text ="Volver", command = regresar)
        boton_guardar.grid(row=1, column=1, padx=10, pady = 5)

        frame_botones.grid(row=7, column=1, padx=10, pady = 5)



    def update_widgets(self):
        pass


class PagePC(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        def guardar():

            config = configparser.ConfigParser()

            config['REACTIVO'] = {'Reactivo' : controller.shared_data['rvo'].get()}
            config['NUM_RACKS'] = {'num_racks' : menu_num_racks.get()}
            config['NUM_FALCONS'] = {'num_falcons' : menu_num_falcon.get()}
            config['NUM_TANDAS'] = {'num_tandas' : 1}
            config['FIRST_TIP'] = {'tip': controller.shared_data['first_tip'].get()}
            config['OT-2-IP'] = {'ip': controller.shared_data['ot_2_ip'].get()}
            config['LAST_TUBE'] = {'tube': controller.shared_data['last_tube'].get()}
            config['VEL_P300'] = {'asp': controller.shared_data['vel_asp_p300'].get(), 
                                'disp': controller.shared_data['vel_disp_p300'].get()}
            config['VEL_P1000'] = {'asp': controller.shared_data['vel_asp_p1000'].get(), 
                                'disp': controller.shared_data['vel_disp_p1000'].get()}
            config['VEL_OT-2'] = {'vel_mov_ot': controller.shared_data['vel_mov_ot'].get()}
            config['VOLUMENES_ALICUOTADO'] = {'vol_5x': self.controller.shared_data['vol_5x'].get(),
                                              'vol_40x': self.controller.shared_data['vol_40x'].get(),
                                              'vol_nfw': self.controller.shared_data['vol_nfw'].get(),
                                              'vol_pc': self.controller.shared_data['vol_pc'].get()
                                              }


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

            OT2_IP = controller.shared_data['ot_2_ip'].get()

            upload_script = ["scp",
                             "-i",
                             "ot2_ssh_key",
                             "../config.ini",
                             "root@" + OT2_IP + ":/data/user_storage"]


            try:                 
                p = subprocess.check_call(upload_script, timeout = 7)
                tkmb.showinfo(title = "Atencion!", message = "Configuracion guardada exitosamente!")

            except subprocess.TimeoutExpired:
                tkmb.showerror(title='Error!', message='No se pudo guardar la configuracion!')


                


        def seleccion_vol_falcons(event):

            num_falcon = int(menu_num_falcon.get())
            for i, v in enumerate(falcons):

                if i < num_falcon:
                    falcons[i].config(state='normal')
                    falcons[i].delete(0, tk.END)
                    falcons[i].insert(0, 50)
                else:
                    falcons[i].delete(0, tk.END)
                    falcons[i].config(state='disabled')

        ################## CANTIDAD DE RACKS A USAR ##################

        sub_frame0 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_num_racks = tk.Label(sub_frame0, text='Cantidad de racks a utilizar')
        label_num_racks.pack(padx=10)

        vlist = list(range(1, 10))
        menu_num_racks = ttk.Combobox(master=sub_frame0, values=vlist, state='readonly', width=3)
        menu_num_racks.set(6)

        menu_num_racks.pack(padx=10, pady=10)

        sub_frame0.grid(row=3, column=1, padx=10, pady = 5)




        ################## SETEO FALCONS ##################


        sub_frame1 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        label_falcons = tk.Label(sub_frame1, text='Cantidad de Falcons a utilizar')
        label_falcons.pack(padx=10)

        falcon_list = list(range(1, 7))
        menu_num_falcon = ttk.Combobox(master=sub_frame1, values=falcon_list, state='readonly', width=3)
        menu_num_falcon.bind('<<ComboboxSelected>>', seleccion_vol_falcons)
        menu_num_falcon.pack(padx=10, pady=10)



        sub_frame1_1 = tk.Frame(self, relief = 'groove', borderwidth = 2)

        label_falcons = tk.Label(sub_frame1_1, text='Ingrese el volumen en cada Falcon (mL)')
        label_falcons.grid(row=0, column=0, padx=10, pady=3, columnspan = 3)


        for i in range(3):

            for j in range(0, 4, 2):

                if j == 0:
                    row = 'A'
                elif j == 2:
                    row = 'B'

                falcon_label = tk.Label(sub_frame1_1, text=row + str(i + 1))
                falcon_label.grid(row=j+1, column=i, padx=10, pady=3)

        falcons = []

        for i in range(3):

            for j in range(1, 5, 2):
                volfalcon = tk.Entry(sub_frame1_1, width=4, state='disabled')
                volfalcon.insert(0, '50')
                falcons.append(volfalcon)
                volfalcon.grid(row=j+1, column=i, padx=10)


        sub_frame1.grid(row=1, column=1, padx=10, pady = 5)
        sub_frame1_1.grid(row=2, column=1, padx=10, pady = 5, ipady = 5)

        ################## SELECCION DEL ULTIMO TUBO ##################

        sub_frame2 = tk.Frame(self, relief = 'groove', borderwidth = 2)


        def disable_enable_button():
            if boton_ult_tubo["state"] == "normal":
                boton_ult_tubo["state"] = "disabled"
                self.controller.shared_data["last_tube"].set('E8')
                entry_ult_tubo.configure(state = 'normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
                entry_ult_tubo.configure(state='readonly')

            else:
                boton_ult_tubo["state"] = "normal"

        def popup_select_tube():


            def guardar_seleccion_tubo():
                entry_ult_tubo.configure(state='normal')
                entry_ult_tubo.delete(0, tk.END)
                entry_ult_tubo.insert(0, self.controller.shared_data["last_tube"].get())
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

            tubes_list = []
            for i in range(8):
                for j in range(5):
                    tube = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=controller.shared_data["last_tube"])

                    tubes_list.append(tube)

                    tube.grid(row=3 + j, column=2 + i, padx=10, pady=10)


            self.controller.shared_data["last_tube"].set('E8')


            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tubo)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()




        checkb_ult_tubo = tk.Checkbutton(sub_frame2,
                                         text="Ultimo rack completo",
                                         variable=self.controller.shared_data['rack_completo_check'],
                                         height=1,
                                         width=21,
                                         command=disable_enable_button,
                                         onvalue=1, offvalue=0)

        self.controller.shared_data['rack_completo_check'].set(1)


        checkb_ult_tubo.grid(row=1, column=1, columnspan=3, padx=3, pady=3)

        label_ult_tubo2 = tk.Label(sub_frame2, text='Ultimo tubo:')
        label_ult_tubo2.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        entry_ult_tubo = tk.Entry(sub_frame2, width=4)
        entry_ult_tubo.insert(0, 'E8')
        entry_ult_tubo.configure(state='readonly')
        entry_ult_tubo.grid(row=3, column=1, padx=3, pady=3)

        boton_ult_tubo = tk.Button(sub_frame2, text="Seleccionar", state='disable', command=popup_select_tube)
        boton_ult_tubo.grid(row=3, column=2, padx=3, pady=3, sticky = 'W')





        ################## SELECCION DEL PRIMER TIP ##################

        def popup_select_tip():
            first_tip = controller.shared_data['first_tip']

            def guardar_seleccion_tip():
                entry_primer_tip.configure(state='normal')
                entry_primer_tip.delete(0, tk.END)
                entry_primer_tip.insert(0, first_tip.get())
                entry_primer_tip.configure(state='readonly')
                popup.destroy()

            popup = tk.Toplevel(self)
            popup.wm_title("Seleccion del primer tip")

            label_tips = tk.Label(popup, text='Seleccione el primer tip disponible:')
            label_tips.grid(row=1, column=1, columnspan=12, padx=10, pady=10)

            for i in range(12):
                label_tips = tk.Label(popup, text=str(i + 1))
                label_tips.grid(row=2, column=2 + i, padx=10, pady=10)

            for j in range(8):
                label_tips = tk.Label(popup, text=string.ascii_uppercase[j])
                label_tips.grid(row=3 + j, column=1, padx=10, pady=10)

            tips_list = []
            for i in range(12):
                for j in range(8):
                    tip = tk.Radiobutton(
                        master=popup,
                        value=string.ascii_uppercase[j] + str(i + 1),
                        variable=first_tip)

                    tips_list.append(tip)

                    tip.grid(row=3 + j, column=2 + i, padx=10, pady=10)

            first_tip.set('A1')

            B1 = ttk.Button(popup, text="Guardar seleccion", command=guardar_seleccion_tip)
            B1.grid(row=11, column=1, columnspan=12, padx=10, pady=10)

            popup.resizable(False, False)
            popup.mainloop()


        label_tips = tk.Label(sub_frame2, text='Primer tip disponible:')
        label_tips.grid(row=4, column=1, columnspan=2, padx=10, pady=3)

        entry_primer_tip = tk.Entry(sub_frame2, width=4)
        entry_primer_tip.insert(0, 'A1')
        entry_primer_tip.configure(state='readonly')
        entry_primer_tip.grid(row=5, column=1, padx=5, pady=3)

        boton_select_tip = tk.Button(sub_frame2, text="Seleccionar", command=popup_select_tip)
        boton_select_tip.grid(row=5, column=2, padx=3, pady=3, sticky = 'W')


        sub_frame2.grid(row=4, column=1, padx=10, pady = 5, ipady = 3)


        ################## BOTON GUARDAR ##################

        frame_botones = tk.Frame(self)

        boton_guardar = tk.Button(frame_botones, text ="Guardar", command = guardar)
        boton_guardar.grid(row=1, column=2, padx=10, pady = 5)


        ################## BOTON VOLVER ##################


        def regresar():
            self.controller.show_frame('StartPage')

        boton_guardar = tk.Button(frame_botones, text ="Volver", command = regresar)
        boton_guardar.grid(row=1, column=1, padx=10, pady = 5)

        frame_botones.grid(row=6, column=1, padx=10, pady = 5)


    def update_widgets(self):
        pass


if __name__ == "__main__":
    keep = Keep()
    keep.mainloop()