import pyautogui
from tkinter import messagebox
import time
import pyperclip
import os


class WpWebUIController:
    """  This Class Helps Controll WP web application interface throught class method and python pyautogui Library
     It Scans screen for WP Web Application Buttons,  there is saves images of these buttons in /media/ Folder,
     you can replace them if there is a UI Update in Whats Up Web Application
     Once It scans for most used buttons and areas like 'Send','Attach','Look for Number','Type Message Area'.
     It saves their location so it wount be scanning for them every time
     It allows to send text along with messages to particular number
     """

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.wpFirstAttachedChatLocation = None
        self.wpSendButtonLocation = None
        self.wpTypeMsgAreaLocation = None
        self.wpAttachButtonLocation = None
        self.wpContactSearhLocation = None

    def ScanForWPButtons(self):
        self._InitializewpSendButtonLocation()  # Looks for Send Button on WP Web and saves its location
        self._InitializewpTypeMsgAreaLocation()  # Looks for Attach Button on WP Web and calculates type message area and saves its location
        self._InitializewpFirstAttachedChatLocation()  # Looks for First Attached Chat on WP Web and saves its location
        self._InitializewpAttachButtonLocation()  # Looks for Attach Button on WP Web and saves its location
        self._InitializeWPContactSearchArea()

        all_button_are_found = self._CheckIfAllButtonsInit()  # checks if all buttons were found
        return all_button_are_found

    def _CheckIfAllButtonsInit(self):
        allWpButtonsInitialized = (self.wpContactSearhLocation and
                    self.wpFirstAttachedChatLocation and self.wpAttachButtonLocation and self.wpSendButtonLocation and self.wpTypeMsgAreaLocation)
        if (allWpButtonsInitialized):
            return True
        else:
            return False

    # Add New Number on Whats Up

    def _AddWhatsUpNumber(self, number):

        # clicks on chat with yourself
        self._openYourChat()
        time.sleep(0.3)
        #sends new number to chat in order to see if there is a whats up
        self._SendWhatsUpMessage(message_text=number)

    # Send Whats Up Message and attaches image to it If There is an Image 
    def _SendWhatsUpMessage(self, message_text=None, attachment=None):
        """
            Send Whats Up Message and attaches image to it If There is an Image .

            Parameters:
            message_text(str): Text of Message to sent.
            message_image(str): Name of image to Send. Image has to be in media folder.
                """

        # clicks on "Type a message" Area on WP Web, locating it by attach button location with vertical offset, 
        self._ClickWPTypeMessageArea()

        if message_text:
            # writes  message_text that passed from argument
            self._copyPasteText(message_text)

            # Waits for screen update after sending message so WP send button will appear
            time.sleep(0.5)

            if (not attachment):  # If there is file to attach doesnt press send
                #Clicks on WP Send Button to send message 
                self._ClickWPSendButton()
            time.sleep(1)
        if (attachment):
            self._copyPasteFile(attachment)
            send_button_search_area = (self.screen_width // 2, self.screen_height // 2, self.screen_width,
                                       self.screen_height)  # Area of Possible Apperance of wp_send_msg
            self._waitForImageToAppear("wp_attached_file_send.png", send_button_search_area,10)  # waits for image to appear
            if(self._ClickImage("wp_attached_file_send.png", send_button_search_area, clicks_amount=1)):
                pass
            else:
                self._ClickWPSendButton()

            # selects new number sended to your chat and press Chat with  and returns True if any or returns False if There is no WP

    def _CheckIfNumberHasWPAndOpenChat(self, number):
        """
            Checks if number that was send to chat, has whats up by clicking on it and if it has opens chats with this number.

            Parameters:
            number(int): number to check if it has Whats Up Account.

            Returns:
            bool: Returns True if number has Whats Up Account, False if not

        """
        pyautogui.click(x=self.wpSendButtonLocation[0] - 160, y=self.wpSendButtonLocation[1] - 90,
                        clicks=1)  #clicks on last sended number
        chat_with_search_area = (self.wpSendButtonLocation[0] - 600, self.wpSendButtonLocation[1] - 600,
                                 # square area 400*400 with right bottom at wpSendButtonLocation
                                 self.wpSendButtonLocation[0], self.wpSendButtonLocation[1])
        time.sleep(0.3)  # minimun time for chat with to appear
        self._waitForImageToAppear('copy_phone_number.png',chat_with_search_area,6)
        if (self._ClickImage(image_name='chat_with.png', image_search_area=chat_with_search_area,
                              clicks_amount=1)):  # clicks on chat_with in search area
            return True
        else:
            return False

            # Clicks on Image, Search image on introduced area, possible to offset by passed offset Points,

    def _ClickImage(self, image_name, image_search_area=None, x_offset=0, y_offset=0, clicks_amount=2):
        """
                    Click on image if there is any on screen, can click with offset.

                    Parameters:
                    image_name(str): image name , images should be located in media folder.
                    image_search_area(tuple,optional): coordinates of square area where this image could be located, in order to reduce time for search. Defaults to None.
                    clicks_amount(int): Amount of clicks to be clicked.
                    x_offset(int,optional): horizontal offset if 'action area' of button is different from it Apperance, positive to move left, negative to move right. Defaults to 0.
                    y_offset(int,optional): vertical offset if 'action area' of button is different from it Apperance, positive to move down, negative to move up. Defaults to 0.

                    Returns:
                    bool: Returns True if was able to find and click on image, False if not

                """

        media_location = "media/"
        try:
            imageLocation = pyautogui.locateCenterOnScreen(media_location + image_name, region=image_search_area,
                                                           confidence=0.8)

            # print(imageName[:-4] + " located at " + str(imageLocation[0])+","+str(imageLocation[1]))
            pyautogui.moveTo(imageLocation[0] + x_offset, imageLocation[1] + y_offset, 1)
            pyautogui.click(x=imageLocation[0] + x_offset, y=imageLocation[1] + y_offset, clicks=clicks_amount)
            return True

        except Exception as e:
            print(image_name + " not found!")
            print(e)
            return False

    def _GetImageCenterLocation(self, image_name, image_search_area=None):
        """
            Find Central Point of image

            Parameters:
            image_name(str): image name , images should be located in media folder.
            image_search_area(tuple,optional): coordinates of square area where this image could be located, in order to reduce time for search. Defaults to None.

            Returns:
            list: Coordinates of button central location on screen in form of [x,y]

        """
        try:
            media_location = "media/"
            imageLocation = pyautogui.locateCenterOnScreen(media_location + image_name, region=image_search_area,
                                                           confidence=0.8)
            #print(imageName + " located at " + str(buttonLocation[0])+","+str(buttonLocation[1]))

            return imageLocation
        except Exception as e:
            print(image_name + " not found!")
            print(e)
            return None

            # presses on WP Send Button

    def _ClickWPSendButton(self):
        pyautogui.moveTo(self.wpSendButtonLocation[0], self.wpSendButtonLocation[1], 1)
        pyautogui.click(x=self.wpSendButtonLocation[0], y=self.wpSendButtonLocation[1], clicks=1)

    # tripple click on WP Type Message Area 
    def _ClickWPTypeMessageArea(self):
        area_to_search_delete_audio_button = (
        0, self.wpTypeMsgAreaLocation[1] - 50, self.screen_width, self.wpTypeMsgAreaLocation[1] + 50)
        self._ClickImage("delete_voice.png", area_to_search_delete_audio_button, clicks_amount=1)
        pyautogui.moveTo(self.wpTypeMsgAreaLocation[0], self.wpTypeMsgAreaLocation[1], 1)
        pyautogui.click(x=self.wpTypeMsgAreaLocation[0], y=self.wpTypeMsgAreaLocation[1], clicks=2)

    # click attach file button on WP web    
    def _ClickAttachFileButton(self):
        pyautogui.moveTo(self.wpTypeMsgAreaLocation[0], self.wpTypeMsgAreaLocation[1], 1)
        pyautogui.click(x=self.wpAttachButtonLocation[0], y=self.wpAttachButtonLocation[1], clicks=1)

    def _ClickWPContactSearchArea(self):
        """
            Click at WP Web Contact Search area 
        """
        pyautogui.moveTo(self.wpContactSearhLocation[0], self.wpContactSearhLocation[1], 1)
        pyautogui.click(x=self.wpContactSearhLocation[0], y=self.wpContactSearhLocation[1], clicks=2)

    # opens attached chat in wp 
    def _openYourChat(self):
        self._ClickWPContactSearchArea()
        pyautogui.press("backspace")
        pyautogui.write('(You)')
        time.sleep(0.5)
        pyautogui.moveTo(self.wpFirstAttachedChatLocation[0], self.wpFirstAttachedChatLocation[1], 1)
        pyautogui.click(x=self.wpFirstAttachedChatLocation[0], y=self.wpFirstAttachedChatLocation[1], clicks=1)

    def _copyPasteFile(self, file_path):
        """
        Copies file to Clipboard, them pastes it , then presses WP Send Button 
        Parameters:
        file_path(str): Path to Image 
        
        """
        try:
            command = "powershell Set-Clipboard -Path " + file_path
            os.system(command)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v')
        except Exception as e:
            print(e)

    def _copyPasteText(self, text):
        """
        Copies text to Clipboard, them pastes it , there should be text enter field selected in order for text to be pasted there.
        Parameters:
        text(str): Text that should be pasted 
        
        """
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')

    def _InitializewpSendButtonLocation(self):
        """
        Set Up location of Send Button in Global Varriable self.wpSendButtonLocation, but searching wp_send_msg.png on screen.

        """
        send_button_search_area = (self.screen_width // 2, self.screen_height // 2, self.screen_width,
                                   self.screen_height)  # Area of Possible Apperance of wp_send_msg
        send_button_possible_images = ['wp_send_msg.png', 'wp_audio_button.png']
        self.wpSendButtonLocation = self._GetButtonLocation(send_button_possible_images, send_button_search_area)

    def _InitializewpTypeMsgAreaLocation(self):
        """
            Set Up location of "Type a message" Area on WP Web and saves it in Global Variable self.wpTypeMsgAreaLocation , 
            locating it by attach button location with vertical offset.
            
        """
        type_message_search_area = (0, self.screen_height // 2, self.screen_width,
                                    self.screen_height)  # Area of Possible Apperance of wp_attach_button
        self.wpTypeMsgAreaLocation = self._GetButtonLocation(['wp_attach_button.png'],
                                                              search_area=type_message_search_area, x_offset=100)

    def _InitializewpAttachButtonLocation(self):
        """
            Set Up location of wp_attach_button on WP Web and saves it in Global Variable self.wpAttachButtonLocation, locating it by wp_attach_button  on screen.

        """
        wp_attach_button_search_area = (0, self.screen_height // 2, self.screen_width,
                                        self.screen_height)  # Area of Possible Apperance of wp_attach_button
        self.wpAttachButtonLocation = self._GetButtonLocation(['wp_attach_button.png'],
                                                               search_area=wp_attach_button_search_area)  # get center location of wp_attach_button

    def _InitializewpFirstAttachedChatLocation(self):
        """
            Set Up location of first chat that is attached on WP Web and saves it in Global Variable self.wpFirstAttachedChatLocation ,
            locating it by searching for  wp_search_1 and wp_search_2.

        """
        wp_search_button_search_area = (0, 0, self.screen_width // 2,
                                        self.screen_height // 2)  # Area of Possible Apperance of wp_search_1 and wp_search_2
        wp_search_possible_images = ['wp_search_1.png', 'wp_search_2.png']
        self.wpFirstAttachedChatLocation = self._GetButtonLocation(wp_search_possible_images,
                                                                    search_area=wp_search_button_search_area,
                                                                    y_offset=50)  # get center location of wp_search_1

    def _InitializeWPContactSearchArea(self):
        """
        Set Up location of WP Contact Search Area  on WP Web and saves it in Global Variable self.wpContactSearhLocation , locating it by searching for
             wp_search_1 and wp_search_2 and givint it 50 points horizontal offset   
        """
        wp_search_contact_area = (0, 0, self.screen_width // 2,
                                  self.screen_height // 2)  # Area of Possible Apperance of wp_search_1 and wp_search_2
        wp_search_possible_images = ['wp_search_1.png', 'wp_search_2.png']

        # get center location of wp_search_1 and adds horizontal offset of 50 pixels
        self.wpContactSearhLocation = self._GetButtonLocation(wp_search_possible_images,
                                                               search_area=wp_search_contact_area, x_offset=50)

    def _GetButtonLocation(self, images_name_list, search_area = None, x_offset = 0, y_offset = 0):
        """
        Find location of button from images of button on different stages(presses,selected,normal), once any of button images appears returns it.

        Parameters:
        images_name_list(List): List of images of button on different stages for example presses,selected,normal, images should be located in media folder.
        search_area(tuple,optional): coordinates of square area where this image could be located, in order to reduce time for search. Defaults to None.        
        x_offset(int,optional): horizontal offset if 'action area' of button is different from it Apperance, positive to move left, negative to move right. Defaults to 0.
        y_offset(int,optional): vertical offset if 'action area' of button is different from it Apperance, positive to move down, negative to move up. Defaults to 0.        

        Returns:
        list: Coordinates of button location on screen in form of [x,y] 
        
        """
        buttonLocation = None
        for image_name in images_name_list:
            buttonLocation = self._GetImageCenterLocation(image_name=image_name,
                                                           image_search_area=search_area)  # get center location of image
            # once location is found, stops loop
            if (buttonLocation):
                buttonLocation = [buttonLocation[0] + x_offset, buttonLocation[1] + y_offset]  # adds offset if any
                break
        # If there is no such button on screen , Pops up an error 
        if (buttonLocation == None):
            self.show_error(f" No Locations for {images_name_list} were found")

        return buttonLocation

    def _waitForImageToAppear(self,image_name,search_area,time_to_wait):
        time_left = time_to_wait
        while(time_left>0):
            time_left-=1
            if(self._GetImageCenterLocation(image_name,search_area)):
                break
            time.sleep(1)

    def show_error(self, error_message):
        """
        Function to show the error message, it creates a new window with error message in it
        Parameters:
        error_message(str): Error Message Text that will be printed on pop up window.  
        """

        messagebox.showerror("Error", error_message)
