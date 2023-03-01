import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import sys
from PIL import Image
from code import QrCode
import numpy as np

qrcode = QrCode()

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 980 #780
    HEIGHT = 720 #520

    def __init__(self):
        super().__init__()
        self.title("E-Learning Tools")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)


        # ============ create two frames ============


        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0,
                                                 )
        self.frame_left.grid(row=0, column=0, sticky="nswe")



        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_cornerleft = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_cornerleft.grid(row=0, column=2, sticky="nswe",)



        # ============ frame_left ============

        # configure grid layout
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Generate",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.display_qr_code)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Read",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="OCR",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text = "Advanced",
                                                command = self.show_tab_view)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        for i in [0, 1, 2, 3]:
            self.frame_right.rowconfigure(i, weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        #self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=5, pady=20, padx=20, sticky="nsew")

        # ============ frame_right -> frame_info ============

        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        
        # self.textbox = customtkinter.CTkTextbox(master=self.frame_info, height = 100, width=0,
        #                                         fg_color=("white", "gray38"),
        #                                         scrollbar_button_color= "black")
        # self.textbox.grid(row=0, column=0,rowspan = 2, padx=(20, 0), pady=(15, 15), sticky="nsew")
        

        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        self.progressbar = customtkinter.CTkProgressBar(master = self.frame_info)
        self.progressbar.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # ============ frame_right <- ============
        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Configuration:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="Image to Text",
                                                       command=self.readfile)
        self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="Image Size",
                                                       command=self.open_input_dialog_event)
        self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                       height=25,
                                                       text="Save As",
                                                       command=self.save_as)
        self.slider_button_5.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")


        # self.progress_bar_label = customtkinter.CTkLabel(master=self.frame_right,
        #                                              text="Image Size")
        # self.progress_bar_label.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        # self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                              text="CTkCheckBox")
        # self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        image = Image.open("./qrcode.png")
        self.image = customtkinter.CTkImage(image,size = (300,300))
        self.image_label = customtkinter.CTkLabel(master = self.frame_right, image=self.image, text= "")
        self.image_label.grid(row=5, column=0, columnspan=2,rowspan = 3, pady=10, padx=20, sticky="we")



        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Display",
                                                command=self.display_qr_code)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")



        
        self.set_default_values()
    
    def cache(self):
        self.text_cache = None

    def set_default_values(self):
        # set default values
        self.create_segmented_button()
        self.frame_cornerleft.grid_forget()#.destroy()
        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        self.radio_button_1.select()
        # self.slider_1.set(0.2)
        #self.slider_2.set(0.7)
        self.progressbar.set(0.5) #state=tkinter.DISABLED
        self.slider_button_1.configure( text="Read Text File")
        self.slider_button_2.configure( text="Image Size")
        #self.set_default_button.configure( text="Restore Default")
        #self.progress_bar_label.configure(state=tkinter.DISABLED, text="Image Size:")
        #self.check_box_2.select()
        self.seg_button_1.configure(values=["Text", "Url", "Email"],command = self.switch_embedding)
        self.seg_button_1.set("Text")
        self.switch_embedding(value = "Text")
        

    def create_segmented_button(self):
        self.seg_button_1 = customtkinter.CTkSegmentedButton(master=self.frame_info)
        self.seg_button_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")


    def add_title(self):
        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="CTkEntry")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

    def url_embedding(self):
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=3, pady=20, padx=20, sticky="nsew")
        self.entry = customtkinter.CTkEntry(master=self.frame_info,
                                            width=120,
                                            height=28,
                                            fg_color=("white", "gray38"),
                                            placeholder_text="https://github.com/mk-armah")
        self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
   
    def text_embedding(self):
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=5, pady=20, padx=20, sticky="nsew")
        self.textbox = customtkinter.CTkTextbox(master=self.frame_info, height = 100, width=0,
                                                fg_color=("white", "gray38"),
                                                scrollbar_button_color= "black")
        self.textbox.grid(row=0, column=0,rowspan = 2, padx=(20, 0), pady=(15, 15), sticky="nsew")
        self.current_text = "Text Embeding \n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 5
        self.textbox.insert("0.0", self.current_text)
        
        print(self.textbox.get("0.0","50.0"))
        #print(dir(self.textbox))
        


    def email_embedding():
        pass

    def switch_embedding(self,value):
        if value == "Text":       
            try:    
                self.textbox.grid_forget()
                self.entry.grid_forget() #.destroy()
            except (AttributeError,ValueError):
                print("Url embedding is Inactive")
            finally:         
                self.text_embedding()
                print("Text")
                
        if value == "Url":
            try:
                self.textbox.grid_forget()
            except (ValueError,AttributeError):
                 print("Text Box Inactive")
            finally:
                self.url_embedding()
                print("Switched to Url")

        if value == 'Email':
            print("Switch to Email")


    def button_event(self):
        print("Button pressed")

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def show_tab_view(self):
        if self.switch_1.get() == 0:
            self.frame_cornerleft.pack()
            
        else:
    
            self.frame_cornerleft = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
            self.frame_cornerleft.grid(row=0, column=2, sticky="nswe")
            
            self.tabview = customtkinter.CTkTabview(self.frame_cornerleft, width=20)
            self.tabview.grid(row=3, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.tabview.add("Appearance")
            self.tabview.add("System") 

            self.tabview.tab("System").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tabview.tab("Appearance").grid_columnconfigure(0, weight=1)

            self.scaling_label = customtkinter.CTkLabel(self.tabview.tab("System"), text="UI Scaling:", anchor="w")
            self.scaling_label.grid(row=0, column=0, padx=20, pady=(10, 0))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("System"), dynamic_resizing=True,
                                                                    command=self.change_scaling_event,
                                                            values=["Default","80%", "90%", "100%", "110%", "120%"])
            self.scaling_optionemenu.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("System"),
                                                        values=["Value 1", "Value 2", "Value Long....."])
            self.combobox_1.grid(row=2, column=0, padx=20, pady=(10, 10))
            self.string_input_button = customtkinter.CTkButton(self.tabview.tab("System"), text="Open CTkInputDialog",
                                                            command=self.open_input_dialog_event)
            self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))
            
            #IMAGE Properties
            self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Appearance"), text="Image Properties")
            self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
            

            
            image_tab_image_format = customtkinter.CTkOptionMenu(self.tabview.tab("Appearance"), dynamic_resizing=True,
                                                        command=self.switch_image_format,
                                                values=["Image Format","PNG","SVG", "JPEG"])
            image_tab_image_format.grid(row=1, column=0, padx=20, pady=(20, 10))
            
            image_inner_embedding = customtkinter.CTkButton(self.tabview.tab("Appearance"), text="Choose Embedding",
                                                            command=self.choose_embedding)
            image_inner_embedding.grid(row = 2,column =0,padx=20, pady=(20, 10))

            image_outer_layer = customtkinter.CTkButton(self.tabview.tab("Appearance"), text="Outer layer",
                                                            command=self.save_as)
            image_outer_layer.grid(row = 3,column =0,padx=20, pady=(20, 10))

            # image_tab_save_as= customtkinter.CTkButton(self.tabview.tab("Appearance"), text="Save As",
            #                                                 command=self.save_as)
            # image_tab_save_as.grid(row=4, column=0, padx=20, pady=(20, 10))

            self.set_default_button = customtkinter.CTkButton(self.tabview.tab("Appearance"),
                                                         height=25,
                                                         text="Restore Default",
                                                         border_width=3,   # <- custom border_width
                                                         fg_color=None,   # <- no fg_color
                                                         command=self.set_default_values)
            self.set_default_button.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="we")



    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def readfile(self):
        filedir = filedialog.askopenfilename()
        items = open(filedir, 'r+')
        text = items.read()
        self.textbox.insert("0.0", text)

    def save_as(self):
        filedir = filedialog.asksaveasfilename()
        items = open(filedir,'wb')
        

    def switch_image_format(self,format:str):
        "Default format is PNG"
        if format == "SVG":
            print("SVG Format")
        if format == "JPEG":
            print("JPEG Format")
        else:
            print("PNG Format")

    
    def choose_embedding(self):
        """set embedded image of qrcode"""
        filedir = filedialog.asksaveasfilename()
        items = open(filedir,'w+')

    def set_out_layer():
        """Sets output layer of Qrcode image"""
        filedir = filedialog.asksaveasfilename()
        items = open(filedir,'w+')



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Set Image Size")
        self.set_image_size = int(dialog.get_input())
        print(self.set_image_size)


    def change_scaling_event(self, new_scaling: str):
        if new_scaling == "Default":
            new_scaling = "100%"
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    
    def set_image_properties(self,reset = True):
        if reset:
            img = qrcode.make_qr(text = self.textbox.get("0.0","50000.0"),embedded_image_path = "./designs/embedded_logo.png")
            
        try:
            img = qrcode.add_enclosure(img,ratio = 1.82)
        except AttributeError as atterror:
            pass
        try:
            img = img.resize((self.set_image_size,self.set_image_size),resample= Image.Resampling.NEAREST)
        except Exception as exc:
            raise exc

        finally:
            return img

    def display_qr_code(self):
        img = self.set_image_properties(reset = True)

        #img.save(fp = r"{filedir}{qrcode_name}.png".format(filedir = args.filedir,qrcode_name = args.qrcode_name),format = 'png')
        print(img)
        img.show()


if __name__ == "__main__":
    app = App()
    app.start()