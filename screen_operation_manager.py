import pyautogui
import time
from wp_web_ui_controller import WpWebUIController

# This is value that waits between some interactions
# so computer and network will be able to keep up, Change it if needed on your computer
time_to_sleep = 0.2

# This class work with screen by scanning it, pressing buttons and scrolling
class ScreenOperationManager(WpWebUIController):
    """ This class work with screen by scanning it, pressing buttons and scrolling
    """
    def sendMessageToNumber(self, number, text,attachment_path=None):
        self._AddWhatsUpNumber(number)  #send number to Chat with Yourself
        time.sleep(time_to_sleep)
        if self._CheckIfNumberHasWPAndOpenChat(number):  #If number has WP Opens CHat with it
            time.sleep( 0.2)
            # Wait for Apperance of Attach Button signalizing that page were loaded
            wp_attach_button_search_area = (0, int(self.screen_height *0.75), self.screen_width,
                                            self.screen_height)  # Area of Possible Apperance of wp_attach_button
            self._waitForImageToAppear('wp_attach_button.png',wp_attach_button_search_area,5)
            self._SendWhatsUpMessage(text, attachment_path)  # sends intro to this number

    # opens attached chat in wp 
    def _openYourChat(self):
        pyautogui.moveTo(self.wpFirstAttachedChatLocation[0], self.wpFirstAttachedChatLocation[1], 1)
        pyautogui.click(x=self.wpFirstAttachedChatLocation[0], y=self.wpFirstAttachedChatLocation[1], clicks=1)




