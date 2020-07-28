from telegram.ext import Updater, CommandHandler,Filters,MessageHandler,ConversationHandler
import subprocess, urllib.request, re,webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time
from splinter.browser import Browser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot_token = "935797879:AAGCXLqMikLffz-eGedZB0th7waxpOVCS58"

print("start")

MUSIC,CLOSE = range(2)
Film = range(1)
video = ""
window = ""


def search_video(word):
    
    global video
    sentences = word.replace(' ','+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+sentences)
    video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
    video ="https://www.youtube.com/watch?v="+video_ids[0]
    #new version
    '''
    executable_path = {'executable_path':'.\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    browser.visit(video)
    print(browser.title)
    time.sleep(2)
    element = browser.find_by_css('.ytp-play-button')
    element.click()
    time.sleep(2)
    window = browser.windows[0]
    '''
    # old version
    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    webbrowser.register('firefox',None,webbrowser.BackgroundBrowser(firefox_path))
    webbrowser.get('firefox').open(video)

def close_tab():
    # old version 
    subprocess.run('taskkill /F /FI "imagename eq firefox.exe"',shell=True)
    #new version
    #window.close()
def open_Film(url):
    webbrowser.open(url=url)


def shutdownCMD():
    subprocess.run("shutdown -s -t 005",shell=True)



###############################################################################################################################################




def shutdown(update, context):
    shutdownCMD()
    update.message.reply_text(
        "your server is shutdown"
    )


def start(update, context):
    update.message.reply_text(
        f"ciao{update.message.from_user.first_name},\nI comandi sono:\n\n/start per visualizzare tutti i comandi disponibili,\n"
        +"/hello per visualizzare tutti i clienti registrati,\n "
        +"turn off pc:\n/shutdown\n"
        +"scegliere la musica:\n/musicApp\n"
        +"scegliere il film:\n/filmApp"
    )
    
    
def musicApp(update,context):
    update.message.reply_text(
        "da qui in poi ogni tua parola sarà il titolo di una canzone\n"
        +"scegli con cura le tue parole "
    )
    return MUSIC

def closeTab(update,context):
    update.message.reply_text(
        "tab chiusa"
    )
    close_tab()


def music(update, context):
    search_video(update.message.text)
    update.message.reply_text(
        "comando per chiudere la tab:\n"
        +"/closeTab"
    )
    return ConversationHandler.END


def done(update, context):
    update.message.replay_text(
        "fine musica"
    )
    return ConversationHandler.END

def filmApp(update,context):
    update.message.reply_text(
        "metti l' URL del film che vuoi vedere al pc\n"
        +"scegli con cura le tue parole "
    )
    return Film

def film(update, context):
    open_Film(update.message.text)
    return ConversationHandler.END




def main():
    updater = Updater(bot_token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    # command to shutdown the pc
    dp.add_handler(CommandHandler('shutdown', shutdown))
    dp.add_handler(CommandHandler('closetab', closeTab))
    
    #here start the conversation for the music
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('musicApp',musicApp)],
        states={
            MUSIC : [
                MessageHandler(Filters.text, music),
                #CommandHandler('closetab',closeTab)
                    ]
        },
        fallbacks=[CommandHandler('Done', done)]
    )
    
    conv_handlers = ConversationHandler(
        entry_points=[CommandHandler('filmApp',filmApp)],
        states={
            Film : [MessageHandler(Filters.text, film)]
        },
        fallbacks=[CommandHandler('Done', done)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(conv_handlers)
    
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
''''
    browser = Browser('chrome', **executable_path)
    browser.visit('https://www.youtube.com/')
    browser.find_by_id('search')
    '''