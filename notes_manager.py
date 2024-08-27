import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import os


# this class creates a GUI for creating and editing notes for Intros
class NotesManager:

    def __init__(self):
        self.intro = {}           # Text in Different Languages
        self.files_to_attach = {}  # Attachment to Text

    #return Introduction for this number
    def GetIntro(self, number=None):
        """ Chech if there is Intro loaded, if not asks you to create one or loads one, OtherWise Get appropirate language and returns it,
         if there is no number passed, returns empty string in order to keep application work
         """
        if (not self.intro):
            self.OpenNotesMenu()
            return self.GetIntro(number)
        elif(number):
            language_of_number = self._GetLanguageByPhone(number)
            if(language_of_number in list(self.intro.keys())):
                return self.intro[language_of_number]
            elif ("English" in list(self.intro.keys())):     # pick up English text if there was no appropirate text for this language
                return self.intro["English"]
            else:
                first_text = next(iter(self.intro.values()))    # pick up fist available text if there was no English or appropirate text for this language
                return first_text
        else:
            return ""

    def OpenNotesMenu(self):
        #self.root = tk.Toplevel(root)
        self.root = tk.Tk()
        self.root.title("Create OR Edit Notes")
        #self.root.geometry("300x200")        
        
        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=True, fill='both')

        self.add_button = tk.Button(self.root, text="Add Text", command=self._AddText)
        self.add_button.pack( padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Save Template", command=self._SaveTemplate)
        self.save_button.pack( padx=10, pady=10)

        self.load_button = tk.Button(self.root, text="Load Template", command=self._LoadTemplate)
        self.load_button.pack(padx=10, pady=10)

        self.load_pic_button = tk.Button(self.root, text="Add Attachment", command=self._AddAttachmentFiles)
        self.load_pic_button.pack(padx=10, pady=10)
        
        self.load_button = tk.Button(self.root, text="Close", command=self.root.destroy)
        self.load_button.pack( padx=10, pady=10)
        self.root.mainloop()

    def _AddText(self):
        language = simpledialog.askstring("Input", "Enter Language :")
        language = language.strip()    # remove empty spaces if any on sides
        if language:
            text = simpledialog.askstring("Input", "Enter Text in this Language:")
            if text:
                self.intro[language] = text
                self._UpdateTextArea()
            else:
                messagebox.showerror("Error", "Text cannot be empty.")
        else:
            messagebox.showerror("Error", "Language cannot be empty.")

    def _UpdateTextArea(self):
        self.text_area.delete(1.0, tk.END)
        separator = "#"*90
        for key, value in self.intro.items():
            self.text_area.insert(tk.END, f"{separator}\n")
            self.text_area.insert(tk.END, f"||||{key}||||: {value}\n")
        for key, value in self.files_to_attach.items():
            self.text_area.insert(tk.END, f"{separator}\n")
            self.text_area.insert(tk.END, f"|||{key}||||: {value}\n")

    def _SaveTemplate(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                template = {"text":self.intro,"files_to_attach":self.files_to_attach}
                json.dump(template, file)
            messagebox.showinfo("Success", "Dictionary saved successfully.")
            self.root.destroy()

    def _LoadTemplate(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as file:
                template = json.load(file)
                self.intro = template["text"]
                self.files_to_attach = template["files_to_attach"]
            self._UpdateTextArea()
            messagebox.showinfo("Success", "Dictionary loaded successfully.")


    # lets Choose Picture to attach to message
    def _AddAttachmentFiles(self):

        language = simpledialog.askstring("FIle To Attach", "Enter Language:")
        language = language.strip()    # remove empty spaces if any on sides
        if language:
            file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
            if file_path and os.path.exists(file_path):

                self.files_to_attach[language] = file_path

            else:
                messagebox.showerror("Error", "Attachment File cannot be empty.")
        else:
            messagebox.showerror("Error", "Language cannot be empty.")


    def GetFilesForAttachment(self,number):
        """ Chech if there is Files loaded, if not returns None, OtherWise Get appropirate language File and returns it,
                 if there is no file for this number, returns None  to keep application work
                 """
        if (not self.files_to_attach):
            return None
        else:
            number_language = self._GetLanguageByPhone(number)
            languages_of_attaments = list(self.files_to_attach.keys())
            if number_language in languages_of_attaments:
                return self.files_to_attach[number_language]
            elif "English" in languages_of_attaments:     # pick up English File if there was no appropirate text for this language
                return self.files_to_attach["English"]
            else:
                return None   # If there is no Attachment in this language and no attachment in English, sends plain text


    def _GetLanguageByPhone(self, phone_number):

        # Dictionary mapping country codes to languages
        country_languages = {
            '+93': 'Dari',  # Afghanistan
            '+355': 'Albanian',  # Albania
            '+213': 'French',  # Algeria
            '+376': 'Catalan',  # Andorra
            '+244': 'Portuguese',  # Angola
            '+54': 'Spanish',  # Argentina
            '+374': 'Russian',  # Armenia
            '+61': 'English',  # Australia
            '+43': 'German',  # Austria
            '+994': 'Russian',  # Azerbaijan
            '+973': 'Arabic',  # Bahrain
            '+880': 'Bengali',  # Bangladesh
            '+375': 'Russian',  # Belarus
            '+32': 'French',  # Belgium
            '+501': 'English',  # Belize
            '+229': 'French',  # Benin
            '+975': 'Dzongkha',  # Bhutan
            '+591': 'Spanish',  # Bolivia
            '+387': 'Serbian',  # Bosnia and Herzegovina
            '+267': 'English',  # Botswana
            '+55': 'Portuguese',  # Brazil
            '+673': 'Malay',  # Brunei
            '+359': 'Bulgarian',  # Bulgaria
            '+226': 'French',  # Burkina Faso
            '+257': 'French',  # Burundi
            '+855': 'Khmer',  # Cambodia
            '+237': 'English',  # Cameroon
            '+238': 'Portuguese',  # Cape Verde
            '+236': 'French',  # Central African Republic
            '+235': 'French',  # Chad
            '+56': 'Spanish',  # Chile
            '+86': 'Mandarin Chinese',  # China
            '+57': 'Spanish',  # Colombia
            '+269': 'French',  # Comoros
            '+242': 'French',  # Congo
            '+243': 'French',  # DR Congo
            '+506': 'Spanish',  # Costa Rica
            '+385': 'Croatian',  # Croatia
            '+53': 'Spanish',  # Cuba
            '+357': 'Greek',  # Cyprus
            '+420': 'Czech',  # Czech Republic
            '+45': 'Danish',  # Denmark
            '+253': 'Arabic',  # Djibouti
            '+593': 'Spanish',  # Ecuador
            '+20': 'Arabic',  # Egypt
            '+503': 'Spanish',  # El Salvador
            '+240': 'Spanish',  # Equatorial Guinea
            '+291': 'Arabic',  # Eritrea
            '+372': 'Estonian',  # Estonia
            '+268': 'English',  # Eswatini
            '+251': 'Amharic',  # Ethiopia
            '+679': 'English',  # Fiji
            '+358': 'Finnish',  # Finland
            '+33': 'French',  # France
            '+241': 'French',  # Gabon
            '+220': 'English',  # Gambia
            '+995': 'Georgian',  # Georgia
            '+49': 'German',  # Germany
            '+233': 'English',  # Ghana
            '+30': 'Greek',  # Greece
            '+299': 'Greenlandic',  # Greenland
            '+502': 'Spanish',  # Guatemala
            '+224': 'French',  # Guinea
            '+245': 'Portuguese',  # Guinea-Bissau
            '+592': 'English',  # Guyana
            '+509': 'French',  # Haiti
            '+504': 'Spanish',  # Honduras
            '+852': 'Cantonese',  # Hong Kong
            '+36': 'Hungarian',  # Hungary
            '+354': 'Icelandic',  # Iceland
            '+91': 'English',  # India
            '+62': 'Indonesian',  # Indonesia
            '+98': 'Persian',  # Iran
            '+964': 'Arabic',  # Iraq
            '+353': 'English',  # Ireland
            '+972': 'Arabic',  # Israel
            '+39': 'Italian',  # Italy
            '+225': 'French',  # Côte d'Ivoire
            '+81': 'Japanese',  # Japan
            '+962': 'Arabic',  # Jordan
            '+7': 'Russian',  # Kazakhstan
            '+254': 'English',  # Kenya
            '+686': 'English',  # Kiribati
            '+383': 'Albanian',  # Kosovo
            '+965': 'Arabic',  # Kuwait
            '+996': 'Russian',  # Kyrgyzstan
            '+856': 'Lao',  # Laos
            '+371': 'Latvian',  # Latvia
            '+961': 'Arabic',  # Lebanon
            '+266': 'English',  # Lesotho
            '+231': 'English',  # Liberia
            '+218': 'Arabic',  # Libya
            '+423': 'German',  # Liechtenstein
            '+370': 'Lithuanian',  # Lithuania
            '+352': 'French',  # Luxembourg
            '+853': 'Cantonese',  # Macau
            '+389': 'Macedonian',  # North Macedonia
            '+261': 'French',  # Madagascar
            '+265': 'English',  # Malawi
            '+60': 'Malay',  # Malaysia
            '+960': 'Dhivehi',  # Maldives
            '+223': 'French',  # Mali
            '+356': 'English',  # Malta
            '+692': 'English',  # Marshall Islands
            '+222': 'Arabic',  # Mauritania
            '+230': 'English',  # Mauritius
            '+52': 'Spanish',  # Mexico
            '+691': 'English',  # Micronesia
            '+373': 'Romanian',  # Moldova
            '+377': 'French',  # Monaco
            '+976': 'Mongolian',  # Mongolia
            '+382': 'Montenegrin',  # Montenegro
            '+212': 'French',  # Morocco
            '+258': 'Portuguese',  # Mozambique
            '+95': 'Burmese',  # Myanmar
            '+264': 'English',  # Namibia
            '+674': 'English',  # Nauru
            '+977': 'Nepali',  # Nepal
            '+31': 'Dutch',  # Netherlands
            '+687': 'French',  # New Caledonia
            '+64': 'English',  # New Zealand
            '+505': 'Spanish',  # Nicaragua
            '+227': 'French',  # Niger
            '+234': 'English',  # Nigeria
            '+47': 'Norwegian',  # Norway
            '+968': 'Arabic',  # Oman
            '+92': 'English',  # Pakistan
            '+680': 'English',  # Palau
            '+507': 'Spanish',  # Panama
            '+675': 'English',  # Papua New Guinea
            '+595': 'Spanish',  # Paraguay
            '+51': 'Spanish',  # Peru
            '+63': 'English',  # Philippines
            '+48': 'Polish',  # Poland
            '+351': 'Portuguese',  # Portugal
            '+974': 'Arabic',  # Qatar
            '+40': 'Romanian',  # Romania
            '+250': 'English',  # Rwanda
            '+685': 'English',  # Samoa
            '+378': 'Italian',  # San Marino
            '+239': 'Portuguese',  # São Tomé and Príncipe
            '+966': 'Arabic',  # Saudi Arabia
            '+221': 'French',  # Senegal
            '+381': 'Serbian',  # Serbia
            '+248': 'English',  # Seychelles
            '+232': 'English',  # Sierra Leone
            '+65': 'English',  # Singapore
            '+421': 'Slovak',  # Slovakia
            '+386': 'Slovene',  # Slovenia
            '+677': 'English',  # Solomon Islands
            '+252': 'Arabic',  # Somalia
            '+27': 'English',  # South Africa
            '+82': 'Korean',  # South Korea
            '+211': 'English',  # South Sudan
            '+34': 'Spanish',  # Spain
            '+94': 'Sinhala',  # Sri Lanka
            '+249': 'Arabic',  # Sudan
            '+597': 'Dutch',  # Suriname
            '+46': 'Swedish',  # Sweden
            '+41': 'German',  # Switzerland
            '+963': 'Arabic',  # Syria
            '+886': 'Mandarin Chinese',  # Taiwan
            '+992': 'Russian',  # Tajikistan
            '+255': 'English',  # Tanzania
            '+66': 'Thai',  # Thailand
            '+670': 'Portuguese',  # Timor-Leste
            '+228': 'French',  # Togo
            '+690': 'English',  # Tokelau
            '+676': 'Tongan',  # Tonga
            '+216': 'French',  # Tunisia
            '+90': 'Turkish',  # Turkey
            '+993': 'Russian',  # Turkmenistan
            '+688': 'English',  # Tuvalu
            '+256': 'English',  # Uganda
            '+380': 'Russian',  # Ukraine
            '+971': 'Arabic',  # United Arab Emirates
            '+44': 'English',  # United Kingdom
            '+1': 'English',  # United States
            '+598': 'Spanish',  # Uruguay
            '+998': 'Russian',  # Uzbekistan
            '+678': 'English',  # Vanuatu
            '+58': 'Spanish',  # Venezuela
            '+84': 'Vietnamese',  # Vietnam
            '+967': 'Arabic',  # Yemen
            '+260': 'English',  # Zambia
            '+263': 'English'  # Zimbabwe
        }

        # Normalize the phone number to ensure it starts with '+'
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        # Check each country code in the dictionary
        for code, language in country_languages.items():
            if phone_number.startswith(code):
                return language

        # Return 'English' if the phone number doesn't match any known country code
        return 'English'
