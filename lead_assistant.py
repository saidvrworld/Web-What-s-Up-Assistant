from tkinter import messagebox,PhotoImage
import tkinter as tk
from notes_manager import NotesManager
from screen_operation_manager import ScreenOperationManager
from contacts_manager import ContactsManager
from pynput import keyboard
import threading
import time

# This class manages leads from SRM System: sends intro messages to providet list of leads in wp 
class LeadAssistant:
    """
    This class Sends Messages to numbers from Excell File, on whats up,
    It takes contacts from Excell file, using ContactsManager class
    Then lets user create and save Template messages with photo attachments on different languages using NotesManager
    Then Sends messages to every number in Excell File using ScreenOperationManager
    """

    def __init__(self):
        self.IntroAlreadySentLeadsList = []          # numbers that already were processed
        self.current_phone_list_progress = [0,0]
        self.paused = False  # Add a paused state variable
        self.screenOperationManager = ScreenOperationManager()      # to manage interactions with Screen
        self.noteManager = NotesManager()            # load manager for Intro Text
        self.contactsManager = ContactsManager()         # load contact manager to get contacts from excel file
        self.listener_thread = threading.Thread(target=self._StartListener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        self._InitializeGUI()                            # initialize GUI to Start work

        
    # calls in order to start the job    
    def StartJob(self):
        self.paused = False
        self.noteManager.GetIntro()
        contacts = self.contactsManager.GetContacts()
        if(self.screenOperationManager.ScanForWPButtons()):

            # Send Report to Notification Number
            self._SendReport("Start to Send Intros",contacts)


            # Actualy Sending Intros To Numbers
            self._SendIntroToNumberList(contacts)

            # Send Report to Notification Number
            self._SendReport("Finished Sending Intros", contacts)

    # Start Job In Separate Thread so the main GUI would be still responsive
    def StartJobInSeparateThread(self):
        thread = threading.Thread(target=self.StartJob)

        # Set the thread as a daemon thread
        thread.daemon = True

        # Start the thread
        thread.start()
    def _SendIntroToNumberList(self,contacts):

        self.current_phone_list_progress = [0,len(contacts)]    # [numbers intro sended, total numbers]
        for number in contacts:
            if self.paused:
                print("Process paused. Waiting to resume...")
                while self.paused:
                    pass
            self.current_phone_list_progress[0]+=1
            self._ProccessNumberToSendIntro(number)
                  
    # set up User Interface for Application
    def _InitializeGUI(self):
        self.rootTK = tk.Tk()
        self.rootTK.title("Lead Assistant")
        self.rootTK.geometry("350x500")
        self.rootTK.configure(bg="white")  # Set the background color to white

        # Load the logo image
        self.logo = PhotoImage(file="media/logo.png")  # Replace with your image path
        logo_label = tk.Label(self.rootTK, image=self.logo)
        logo_label.pack(pady=10)

        start_button = tk.Button(self.rootTK, text="Start Job", command=self.StartJobInSeparateThread)
        start_button.pack(pady=20)
        select_CSV_file_button = tk.Button(self.rootTK, text="Load Contacts", command=self.contactsManager.LoadContacts)
        select_CSV_file_button.pack(pady=20)
        load_intro_button = tk.Button(self.rootTK, text="Load Intro", command=self.noteManager.OpenNotesMenu)
        load_intro_button.pack(pady=20)
        add_notification_number_button = tk.Button(self.rootTK, text="Add Number For Notification", command=self.contactsManager.AssignNotificationNumber)
        add_notification_number_button.pack(pady=20)
        show_progress_button = tk.Button(self.rootTK, text="Show Progress",
                                                   command=self._ShowProgress)
        show_progress_button.pack(pady=20)
        # Bind the 'Esc' key to pause the process
        self.rootTK.mainloop()
        
    # Proccess Number by Sending intro to it 
    def _ProccessNumberToSendIntro(self,number):
        number = self.contactsManager.FixNumberTypeAndFormat(number)                                                 # fix number to str and adds + if there is no
        if(self._NumberAlreadyProccessed(number)):                                                   # checks if intro were already sent to this number
            pass
        else:
            self._AddNumberToProcessedList(number)                                                  # adds number so later if wont be proccessed again
            intro_text = self.noteManager.GetIntro(number)
            intro_file = self.noteManager.GetFilesForAttachment(number)
            self.screenOperationManager.sendMessageToNumber(number,intro_text,intro_file)
                     
    # adds Number to List of Numbers that where already processed
    def _AddNumberToProcessedList(self,number):
        
        self.IntroAlreadySentLeadsList.append(number)

    # Checks if number were already proccesed
    def _NumberAlreadyProccessed(self,number):
        numberProccesed = (number in self.IntroAlreadySentLeadsList)

    def _StartListener(self):
        with keyboard.Listener(on_press=self._OnPress) as listener:
            listener.join()

    def _OnPress(self, key):
        try:
            if key == keyboard.Key.shift_l:  # Detect left Shift key
                self.paused = not self.paused
                if self.paused:
                    print("Process paused. Press Left Shift again to resume.")
                else:
                    print("Process resumed.")
        except AttributeError:
            pass

    # Sends Report to number from WP

    def _SendReport(self,text,numbers):
        # Number to Send Notifications about results
        number_for_notifications = self.contactsManager.GetNotificationNumber()
        current_time = time.strftime("%H:%M", time.localtime())
        text_for_notification = f"{text}, Numbers: {len(numbers)}, Time:{current_time}"
        self.screenOperationManager.sendMessageToNumber(number_for_notifications, text_for_notification)

    def _ShowProgress(self):
        progress_info = f"{len(self.IntroAlreadySentLeadsList)} numbers were processed Today\n"
        progress_info+=f"{self.current_phone_list_progress[0]} out of {self.current_phone_list_progress[1]} number in Current Excell File were Processed "
        messagebox.showinfo("Progress Report", progress_info)


if __name__ == "__main__":
     
    m = LeadAssistant()
    