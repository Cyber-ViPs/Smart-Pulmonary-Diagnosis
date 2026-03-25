
import threading
import os
import reportlab 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from tkinter import filedialog, messagebox
from reportlab.lib import colors
import time
import serial.tools.list_ports
from tkinter import filedialog
from tkinter import filedialog
from  moto import Moto
import tensorflow as tf
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import ttk, Label
from tkinter import messagebox as mb
#import serial
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import simpledialog


class Med_AI_:
    """
    Main Application class for the Med AI Pulmonary Diagnosis system.
    Integrates deep learning analysis, hardware feedback, and automated reporting.
    """

    def __init__(self,win):
        """
        Initializes the GUI components, assets, and background variables.
        
        Args:
            win (tk.Tk): The main Tkinter window instance.
        """
        self.win = win
        self.motoCRUD = Moto()
        self.final_status = ""  # Start empty, will hold "Doente" or "Normal" after analysis
                                 
        color01 = '#078EA0'      

        # === ASSETS BUTTONS ICON SECTION ===
        # Assets icons changer them to your own icons in the assets folder
        trash1 = os.path.join("assets", "Trash01.png") # Change to your actual path logo
        img_trash = Image.open(trash1).resize((30, 30))
        self.icon_trash = ImageTk.PhotoImage(img_trash)
        #print icon
        print1 = os.path.join("assets", "print_001.png") # Change to your actual path logo
        img_print = Image.open(print1).resize((30, 30))
        self.icon_print = ImageTk.PhotoImage(img_print)
        #search icon
        search1 = os.path.join("assets", "search01.png") # Change to your actual path logo
        img_search = Image.open(search1).resize((33, 33))
        self.icon_busca = ImageTk.PhotoImage(img_search)
        #analysis icon static
        scan1 = os.path.join("assets", "dna01.png") # Change to your actual path logo
        img_scan = Image.open(scan1).resize((28, 28))
        self.icon_analise = ImageTk.PhotoImage(img_scan)
        #email icon
        email1 = os.path.join("assets", "email01.png") # Change to your actual path logo
        img_email = Image.open(email1).resize((30, 30))
        self.icon_email = ImageTk.PhotoImage(img_email)

        """------------------------------------------------"""
       
        #Gif test frame by frame for the analysis button, you can change the gif in the assets folder but make sure to adjust the path and size accordingly
        self.path_gif = "assets/dna_scan.gif"
        self.frames_gif = []
        # Load all frames of the GIF into a list
        img_gif = Image.open(self.path_gif)
        for frame in ImageSequence.Iterator(img_gif):
            # resize and convert to RGBA for better display in Tkinter
            frame_redimensionado = frame.copy().resize((30, 30)).convert("RGBA")
            self.frames_gif.append(ImageTk.PhotoImage(frame_redimensionado))

        self.animation_01 = False # Control flag for the animation state
        self.indice_frame = 0
                        
        self.motoed2Label = tk.Label(win, text='_____________________________________', background='#078EA0',foreground="#ffffff")
        self.motoed2Label.place(x=320,y=80)
        self.motoedLabel = tk.Label(win, text='______________________________________',background='#078EA0',foreground="#fafafa")
        self.motoedLabel.place(x=350,y=105)
        self.bottomLabel = tk.Label(win, text='© 2026 Med AI. All Rights Reserved by Emanuel',font="Bold 9", background='#078EA0',foreground="#1F201E") 
        self.bottomLabel.place(x=330,y=628)
        
        # Window for the analysis history (file name + result)
        self.tree = ttk.Treeview(win, columns=(1,2), show='headings', selectmode='browse')
        self.tree.heading(1, text='File Name')
        self.tree.heading(2, text='Diagnosis Result')
        self.tree.tag_configure('sick_tag', foreground='red')
        self.tree.tag_configure('healthy_tag', foreground='green')
        self.tree.place(x=70,y=330, width=550, height=230)
        
        #Scrollbar for the Treeview
        self.verscrlbar = ttk.Scrollbar(win,orient="vertical", command=self.tree.yview)
        self.verscrlbar.pack(side = 'right', fill='x')
        self.tree.configure(yscrollcommand = self.verscrlbar.set)
        self.verscrlbar.place(x=630,y=330, height=230)
       
        # IA Analysis Section:
        # 1. Field to show the file path (readonly)
        self.path_var01 = tk.StringVar()
        self.entry_path01 = tk.Entry(win, textvariable=self.path_var01, width=50, state='readonly', bg='#dde')
        self.entry_path01.pack()
        self.entry_path01.place(x=70,y=298, width=500)

        
        # === TOOLBAR BUTTONS SECTION ===
        # These buttons handle the core workflow actions (Print, Email, Clear, Scan)
        # 2. Botton to open file dialog and load image
        self.btn_search01 = tk.Button(win, text=" image preview", command=self.load_image, borderwidth=0, highlightthickness=0, background="#dde", activebackground="#0AF33D")
        self.btn_search01.pack()
        self.btn_search01.place(x=580,y=298)
        
        #trash Botton for clear the selection and reset the interface for a new analysis
        self.btn_clear = tk.Button(win, image=self.icon_trash, command=self.clear_img,
        borderwidth=0,      # Remove the border around the button
        highlightthickness=0, # Remove the highlight border when the button is focused
        background="#078EA0",      # background color of the button
        activebackground="#078EA0" # background color when the button is pressed (active state)
            )
        self.btn_clear.place(x=865, y=298) 
        
        # Botton to generate PDF report of the analysis result, it will be enabled after the first analysis is done (when we have a valid result to show in the report)
        self.btn_print = tk.Button(win, image=self.icon_print, command=self.Pdf_Generate, borderwidth=0, highlightthickness=0, background="#078EA0", activebackground="#078EA0")
        self.btn_print.place(x=780, y=298)
        
        # 3. Label for the image preview (starts empty, will show the selected image as a thumbnail)
        self.lbl_preview = tk.Label(win,bg=color01)
        self.lbl_preview.pack()
        self.lbl_preview.place(x=660,y=330)
        
        # 4. Botton to run the analysis (starts disabled, will be enabled after we load an image)
        self.btn_analysis01 = tk.Button(win, image=self.icon_analise, command=self.check_and_run, state='normal', borderwidth=0, highlightthickness=0, background="#078EA0",activebackground="#078EA0")
        self.btn_analysis01.pack()
        self.btn_analysis01.place(x=740,y=298)
        #5. Botton to send the report by email, it will be enabled after the first analysis is done (when we have a valid result to show in the report)
        self.btn_email = tk.Button(win, image=self.icon_email, command=self.email_report, borderwidth=0, highlightthickness=0, background="#078EA0", activebackground="#078EA0")
        self.btn_email.place(x=820, y=298)
        
    def load_image(self):
        """ Opens a file dialog to select an image, updates the path variable, shows a preview, and enables the analysis button. """
        file_01 = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if file_01:
            self.path_var01.set(file_01)
            img = Image.open(file_01).resize((250, 300))
            self.photo_show = ImageTk.PhotoImage(img)
            self.lbl_preview.config(image=self.photo_show, text="")
            self.btn_analysis01.config(state='normal')

    
       
    def check_and_run(self):
        """ Checks if the folder structure is correct before starting the analysis. If everything is in place, it starts the analysis process. """
        if not self.folder_verfication_med_ai():
            return
        path_01 = self.path_var01.get()
        
        # Check if we have a valid path before starting the analysis
        if not path_01 or path_01 == "":
            mb.showwarning("Warning", "Please select an image first!")
            return

        # 1. Start animation
        self.animation_01 = True
        self.indice_frame = 0 # Reset to the beginning of the GIF
        self.reload_animation()

        # 2. Run the AI in a separate thread (to not freeze the GIF)
        # The daemon=True ensure that if you close the window, the thread also closes
        threading.Thread(target=self.background_process, args=(path_01,), daemon=True).start()
        
       
       
    def clear_img(self):
        # 1. Clear the path string
        self.path_var01.set("")
        
        # 2. Remove the image from the Label and restore the original text
        self.lbl_preview.config(image='')
        # Note: Clear the reference to the image in memory
        self.photo_show = None
        
        # 3. Disable the analysis button (since there's no more image)
        self.btn_analysis01.config(state="disabled")
        
        
        for item in self.tree.get_children():
            self.tree.delete(item)# Clear the history table
            self.final_status = "" #Reset the status to empty, since we cleared the selection
        print("Interface cleared. Ready for new selection.")
       
    
    
    def reload_animation(self):
        """ This function updates the analysis button with the next frame of the GIF. It keeps scheduling itself to run every 50ms as long as the animation flag is True. """
        if self.animation_01:
            # Get the next frame
            frame = self.frames_gif[self.indice_frame]
            self.btn_analysis01.config(image=frame)
            
            # Increment the index for the next loop
            self.indice_frame = (self.indice_frame + 1) % len(self.frames_gif)
            
            # Schedule the next update (e.g., 50ms for a smooth GIF, adjust as needed based on the GIF's frame rate)
            self.win.after(50, self.reload_animation)  
    
    def background_process(self, path_01):
        """ This function runs in a separate thread to perform the AI analysis. It loads the model, processes the image, and then brings the result back to the main thread to update the UI. """
        try:
            analysis_result = self.motoCRUD.rayx_analysis(path_01)
            
            # 3. Bring back to the main Tkinter thread to update the UI
            self.win.after(0, lambda: self.finish_process(analysis_result, path_01))
        except Exception as e:
            print(f"Error on thread: {e}")
            self.animation_01 = False # Stop the GIF if there's an error
            self.btn_analysis01.config(image=self.icon_analise) # Restore the original icon
            mb.showerror("Error", f"Failed to process the image: {e}")
      
            
    def finish_process(self, analysis_result, path_01):
        """ This function runs in the main thread after the analysis is done, so it's safe to update the UI here. It receives the result from the AI and the path of the analyzed image. """
           
        # Para a animação e volta o ícone original
        self.animation_01 = False
        self.btn_analysis01.config(image=self.icon_analise)
        
        if analysis_result is not None:
            status = "Sick" if analysis_result > 0.5 else "Healthy"
            self.final_status = status
            self.add_to_history(path_01, status)
            self.send_to_arduino(status)
            mb.showinfo("Success", f"Analysis completed!\nResult: {status}")
            

    def add_to_history(self, full_path, status):
        """ Adds a new entry to the history Treeview with the file name and diagnosis result. The text color is set based on the status (red for Sick, green for Healthy). """
        # 1. Get only the filename (without the folder path)
        file_name = os.path.basename(full_path)
        
        # 2. Remove the extension (.jpg, .png, etc)
        file_no_extension = os.path.splitext(file_name)[0]
        
        # 3. Add the line color depending on the status
        if status == "Sick":
            tag_cor = 'sick_tag'
        else:
            tag_cor = 'healthy_tag'
        # 3. Insert into the Treeview
        # Let's assume your widget is named self.tree
        # '' means it has no "parent" (it's a main line)
        # 'end' places it at the end of the list
        self.tree.insert('', 'end', values=(file_no_extension, status), tags=(tag_cor,))
       
       
    
    
    
   

    def Pdf_Generate(self):
        """ Generates a PDF report of the analysis result, including the selected image and the diagnosis. It first checks if we have a valid result to show, then opens a save dialog to choose where to save the PDF, and finally creates the PDF with the reportlab library. """
        if not self.final_status:
            mb.showwarning("Warning", "You must perform an analysis before printing!")
            return

        # 1. Select where to save the file
        path_to_save = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"Report_{datetime.now().strftime('%d%m%Y_%H%M')}.pdf",
            title="Save Report As"
        )

        if not path_to_save: # If the user cancels the save dialog
            return

        try:
            c = canvas.Canvas(path_to_save, pagesize=A4)
            Width_01, height_01 = A4

            # --- Watermark (In the middle of the page) ---
            water_logo_path = os.path.join("assets", "company_logo.png") # Change to your actual path logo
            self.Watermark_full(c, Width_01, height_01, water_logo_path) # Ajuste para seu caminho real
            # --- Company Logo (Top Left Corner) ---
            path_logo = os.path.join("assets", "company_logo.png") # Change to your actual path logo
            if os.path.exists(path_logo):
                c.drawImage(path_logo, 50, height_01 - 80, width=50, height=50, mask='auto')
            
            # --- HEADER ---
            c.setFont("Helvetica-Bold", 16)
            c.drawString(120, height_01 - 50, "MED AI - MEDICAL SYSTEMS")
            c.setFont("Helvetica", 10)
            c.drawString(120, height_01 - 65, "Analysis of Images by Artificial Intelligence")
            
            # --- PARTITION LINE ---
            c.setStrokeColor(colors.black)
            c.line(50, height_01 - 90, Width_01 - 50, height_01 - 90)

            # --- BODY ---
            c.setFont("Helvetica", 12)
            c.drawString(50, height_01 - 120, f"Issue Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            nome_img = os.path.basename(self.path_var01.get())
            c.drawString(50, height_01 - 140, f"Patient/File: {nome_img}")

            # --- RESULTS ---
            c.setFont("Helvetica-Bold", 18)
            if self.final_status == "Sick":
                c.setFillColor(colors.red)
            else:
                c.setFillColor(colors.darkgreen)
                
            c.drawCentredString(Width_01/2, height_01/2 - 50, f"RESULT: {self.final_status}")
            # --- SELECTED IMAGE  (If available) within the pdf file ---
            if PATH_img := self.path_var01.get():
                c.drawImage(PATH_img, 160, 390, width=300, height=300)

            # --- FOOTER ---
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(160, 50, "Document generated automatically by the Med AI System.")
            c.save()
            self.path_last_pdf = path_to_save # Save the path to the last generated PDF (ex: C:/Users/Docs/relatorio.pdf)
            mb.showinfo("Successfully", "Report saved successfully!")
            return path_logo
        except Exception as e:
            mb.showerror("Error", f"Failed to generate PDF: {e}")
            
              
           
    def Watermark_full(self, canvas_obj, Width_01, height_01, path_logo):
        if os.path.exists(path_logo):
            canvas_obj.saveState()
            canvas_obj.setFillAlpha(0.1)  # Make the image very transparent to be a watermark
            
            space = 150  #  Logos every 150 points (adjust as needed)
            logo_size = 50
            
            # Double loop for coverage of width (x) and height (y)
            # Start with a negative value or 0 to ensure complete coverage
            for x in range(0, int(Width_01) + space, space):
                for y in range(0, int(height_01) + space, space):
                    
                    # Optional: Move the 'y' with base on 'x' to create a disoriented effect
                    # This reinforces the visual perception of diagonal
                    offset_y = (x / space) % 2 * (space / 2)
                    
                    canvas_obj.drawImage(
                        path_logo, 
                        x, 
                        y + offset_y, 
                        width=logo_size, 
                        height=logo_size, 
                        mask='auto'
                    )
            
            canvas_obj.restoreState()
           
           
       
       
      
    def arduino_detect(self):
        """ Detects the serial port to which the Arduino is connected by checking for common identifiers in the port descriptions. Returns the port name if found, or None if no compatible device is detected. """
        # List all the active serial ports and their descriptions
        ports = serial.tools.list_ports.comports()
    
        for port in ports:
            # Print all ports to the terminal for debugging
            print(f"Port checking: {port.device} - Description: {port.description}")
            
            # Now we check for common terms in USB-Serial adapters (like my CH340)
            desc = port.description.upper()
            if "CH340" in desc or "USB-SERIAL" in desc or "ARDUINO" in desc:
                print(f"-> Compatible device found on {port.device}!")
                return port.device # Returns the port name (e.g., COM3, /dev/ttyUSB0, etc)
        return None
      
       
    def send_to_arduino(self, status):
        """ Sends a signal to the Arduino based on the diagnosis result. It first detects the correct serial port, then sends 'A' for Sick and 'B' for Healthy. The connection is opened, the signal is sent, and then it is closed. """
        port_com = self.arduino_detect()
        
        if port_com:
            try:
                # Open the connection (9600 is the default for Arduino)
                # timeout=1 avoids the Python script from "waiting" indefinitely for the Arduino to respond, which can happen if there's a connection issue
                ser = serial.Serial(port_com, 9600, timeout=1)
                time.sleep(2) # Wait for the Arduino to reset after the connection
                
                # Define the character based on the status
                commend = 'A' if status == "Sick" else 'B'
                
               
                ser.write(commend.encode()) # Send as bytes
                ser.close() # Close the connection after sending
                print(f"Signal '{commend}' sent successfully to {port_com}")
                
                ser.close()
            except Exception as e:
                print(f"Error communicating with Arduino: {e}")
       #-------------Arduino communication functions end here----------------


    def folder_verfication_med_ai(self):
        """ Verifies if the essential folders and files for the Med AI system are present. It checks for the existence of the training, test, production, assets, and models folders, as well as the model weights file. If any are missing, it shows an error message with the list of missing items. Returns True if everything is in place, or False if there are missing items. """
        essential_folders = [
            "data/training", 
            "data/test", 
            "data/production",
            "assets",
            "models"
            
        ]
        
        lost_folders = []
        for folder_00 in essential_folders:
            if not os.path.exists(folder_00):
                lost_folders.append(folder_00)
        
        # Check if the model weights file exists (adjust the name if your weights file has a different name)
        path_weights = os.path.join("models", "my_trained_model.weights.h5")
        if not os.path.exists(path_weights):
            lost_folders.append(f"{path_weights} (File of weights for the AI model not found!)")

        if lost_folders:
            erro_msg = "The following files/folders were not found:\n\n"
            erro_msg += "\n".join([f"• {p}" for p in lost_folders])
            erro_msg += "\n\nMake sure the project structure is correct."
            
            mb.showerror("Configuration Error", erro_msg)
            return False
        return True  
     
     # Email sending function, it first checks if we have a generated PDF to send, then asks the user for the recipient's email address, and finally sends the email with the PDF attached. The email sending is done in a separate thread to avoid freezing the UI.  
    def email_report(self):
        if not hasattr(self, 'path_last_pdf') or not os.path.exists(self.path_last_pdf):
            mb.showwarning("Warning", "Generate the PDF report before sending by email!")
            return

        email_user = simpledialog.askstring("Send Report", "Enter the recipient's email address:")
        
        if email_user:
            threading.Thread(target=self.start_send_email, args=(email_user, self.path_last_pdf), daemon=True).start()
        
    def start_send_email(self, destination, path_pdf):
        """
        Handles the SMTP connection and dispatches the PDF report via email.
        Runs in a background thread to maintain UI responsiveness.

        Args:
            destination (str): Recipient's email address.
            path_pdf (str): Local file system path to the generated diagnostic report.
        """
        your_email = "YOUR_EMAIL_HERE" # Attention: For Gmail, it is recommended to use a specific app password for greater security (instead of the main account password)
        your_senha = "YOUR_APP_PASSWORD_HERE" # Attention: For Gmail, it is recommended to use a specific app password for greater security (instead of the main account password)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = destination
            msg['Subject'] = f"Digital Medical Report - {self.final_status}"

            body = "Dear Patient,\n\nPlease find the attached report of your pulmonary analysis conducted via Med AI.\n\nBest regards,\nMedical Team."
            msg.attach(MIMEText(body, 'plain'))

            # Attach the PDF
            with open(path_pdf, "rb") as anexo:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(anexo.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(path_pdf)}")
                msg.attach(part)

            # Sercurity configuration for Gmail (adjust if using another email provider)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(your_email, your_senha)
            server.send_message(msg)
            server.quit()
            
            self.win.after(0, lambda: mb.showinfo("E-mail", "Report sent successfully!"))
        except Exception as e:
            self.win.after(0, lambda: mb.showerror("Erro E-mail", f"Falha ao enviar: {e}"))      
 
 
            
win = tk.Tk()
main_ = Med_AI_(win)
win.title("IA Pulmonary Diagnosis")
win.geometry("950x650+0+0")
win.configure(background="#078EA0")
campany_Logo = os.path.join("assets", "MED_AI-1.png") # Change to your actual path logo
imagem_ = ImageTk.PhotoImage(file=campany_Logo)
Label_Mad_IA=Label(win,image=imagem_,bg="#078EA0",pady=0,).place(x=390,y=30,)
win_logo = os.path.join("assets", "med-ia.ico") # Change to your actual path logo
win.iconbitmap(win_logo)
win.mainloop()
