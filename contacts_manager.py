from tkinter import filedialog,messagebox,simpledialog
import pandas as pd
import os
import pickle

class ContactsManager:

    def __init__(self):
        self.contacts = None
        self._LoadNotificationNumber()
    def GetContacts(self):
        try:
            if self.contacts:
                return self.contacts
            else:
                self.LoadContacts()
                return self.GetContacts()
        except Exception as e:
            print(e)
            self._show_error(e)
            self.LoadContacts()
            return self.GetContacts()

    def LoadContacts(self):
        file_path = self._SelectFileWithContacs()
        self.contacts = self._GetContactsFromFile(file_path)

    def FixNumberTypeAndFormat(self, number):
        number = str(number)
        if not number.startswith('+'):
            number = '+' + number

        return number


    # open file select window to choose CSV File
    def _SelectFileWithContacs(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[
            ("xlsx files", "*.xlsx")])  # call dialog window for file selection
        if file_path:
            # print(file_path)
            file_extension = os.path.splitext(file_path)[1]  # checks if file type is correct
            return file_path

        else:
            return None

    def _GetContactsFromFile(self, file_path):

        # Read the Excel file into a DataFrame
        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            self._show_error(f"The file at {file_path} was not found.")
            return
        except pd.errors.EmptyDataError:
            self._show_error("No data found in the file.")
            return
        except pd.errors.ParserError:
            self._show_error("Error parsing the file.")
            return

        phones = []
        try:
            phone_cols = df.filter(regex='(?i)^phones?$').columns

            # Extract the  and 'phone' columns
            phones = df.filter(regex='(?i)^phones?$').squeeze().tolist()
        except Exception as e:
            self._show_error("The CSV file does not contain and 'phone' columns.")
        # Print the extracted columns
        # print(names_and_phones['Phone'])

        return phones

    def _show_error(self, error_message):
        """
        Function to show the error message, it creates a new window with error message in it
        Parameters:
        error_message(str): Error Message Text that will be printed on pop up window.
        """

        messagebox.showerror("Error", error_message)

        # Assigns Number to send Wp after work is finished
    def AssignNotificationNumber(self):
            self._number_for_notification = simpledialog.askstring("Notification, Number", "Enter What Up Number To Notify :")

            data_to_save = {'number_for_notification': self._number_for_notification}

            # Save the number_to_save to a file
            with open('saved_data.pkl', 'wb') as f:
                pickle.dump(data_to_save, f)

    # Loads Number from local saved file to send Notofication about work done
    def _LoadNotificationNumber(self):

        try:
            # Load the number_for_notification from the file
            with open('saved_data.pkl', 'rb') as f:
                loaded_data = pickle.load(f)

            self._number_for_notification = loaded_data['number_for_notification']

        except Exception as error:
            self._number_for_notification = None

    # Returns Notification Number if Any , Ask To Enter it if there is no
    def GetNotificationNumber(self):
        if not self._number_for_notification:
            self.AssignNotificationNumber()
            return self.GetNotificationNumber()
        else:
            return self._number_for_notification