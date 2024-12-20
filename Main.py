import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException        
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from PIL import Image,ImageDraw,ImageFont
import time
import os
import shutil
import cv2
import glob
import numpy as np
import re
import wget
import textwrap
import ffmpeg
import subprocess


#for display all error msg
def errorMsg(num, txt1 = None, txt2 = None):
    output_txt = ""

    if(num == 900):
        txt1 = "Error code 900 -- Error msg from __Main__"
        output_txt += txt1
        
    elif(num == 901):
        output_txt = errorMsg(900)+"\n"
        output_txt += "Error code 901 -- Empty list, plz edit the TUAliast"
        sg.popup(output_txt)
        
    elif(num == 100):
        txt1 = "Error code 100 -- Error msg from ListFilter"
        output_txt += txt1
    
    elif(num == 101):
        output_txt = errorMsg(100)+"\n"
        output_txt += f"Error code 101 -- text {str(txt1) } : {str(txt2)}"
        sg.popup(output_txt)


    elif(num == 200):
        txt2 = "Error code 200 -- Error msg from DownIGvideo"
        output_txt += txt2

    elif(num == 201):
        output_txt = errorMsg(200)+"\n"
        output_txt += "Error code 201 -- the chromedriver is unable, please download the new cheomedriver in \nUrl : https://chromedriver.chromium.org/downloads "
        sg.popup(output_txt)

    elif(num == 202):
        output_txt = errorMsg(200)+"\n"
        output_txt += "Error code 202 -- Selenium xpath error error"
        sg.popup(output_txt)

    elif(num == 203):
        output_txt = errorMsg(200)+"\n"
        output_txt += f"Error code 203 -- Failed to delete {txt1}. Reason: {txt2}"
        sg.popup(output_txt)
        
    elif(num == 204):
        output_txt = errorMsg(200)+"\n"
        output_txt += f"Error code 204 -- Please remove the file {txt1}\nNext, Press Ok to proceed"
        
        file = sg.popup_get_file(output_txt,  title="Delete File", default_path = txt2)
        
        if file == "OK":
            pass
    return output_txt

#remove all unnessuary item form InputTUATxt
def ListFilter(InputTUATxt, correctList = "", errorList = "", TitleList = [], UrlList = [], AuthorList = []):
    
    TUAlist = []
    IntLine = 1

    for row in InputTUATxt.split("\n"):
        item = row.split("|")
        print(item)
        if(len(item) == 3):                   
            TitleList.append(item[0])
            UrlList.append(item[1])
            AuthorList.append(item[2])
            correctList += row+ "\n"
        else:
            print(errorMsg(101, IntLine, item))
            errorList += row+ "\n"
        IntLine+=1

    return TitleList, UrlList, AuthorList, correctList, errorList

#For download the instagram video or photo
def DownIGvideo(Urls, chromedriver_path, ElemPath, OutputPath, DownloadVideoWebsiteUrl):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", {
                    "download.default_directory": ElemPath,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True
            })
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        driver.get(DownloadVideoWebsiteUrl)
        
    except:
        print(errorMsg(201))
        
    counter = 1
    for url in Urls:
            
        inputbarxpath = "/html/body/main/div[1]/form/div/input[1]"
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, inputbarxpath))).send_keys(url)
            
        download_xpath = "/html/body/main/div[1]/form/button"
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, download_xpath))).click()
        time.sleep(2)

        try:
            close_adv_btn_xpath = "/html/body/div[1]/div/div/div[2]/button"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, close_adv_btn_xpath))).click()
        except:
  
            print(errorMsg(202))
            ch = sg.popup("Press <Close>, then Press Ok to proceed")
            if ch=="OK":
                pass
        try:
            elems = driver.find_elements(By.XPATH, "/html/body/main/div[2]/div/div[1]/div/div/div[2]/div/a")
            for elem in elems:
                link = elem.get_attribute("href")
                #print(elem.get_attribute("href"))

            driver.get(link)
        except:
            pass
        
        ##2)check the video finish download
        TrueValue = True
        while TrueValue == True:
            list = os.listdir(ElemPath)
            for i in range(len(list)):
                time.sleep(0.5)
                if list[i].endswith(".mp4") == True:
                    TrueValue = False
                    #print(list[i])
                    break

        # Change the name and path of the downloaded file
        old_file_path = os.path.join(ElemPath, list[i])
        """
        try:
            new_file_path = OutputPath+"/"+str(counter)+".mp4"
        except:
            new_file_path = OutputPath+str(counter)+".mp4"
        """
        new_file_path = os.path.join(OutputPath, str(counter)+".mp4")
        counter+=1
        try:
            os.rename(old_file_path, new_file_path)
        except:
            print(errorMsg(204, old_file_path, OutputPath))
            os.rename(old_file_path, new_file_path)

        #remove all the file in ElemPath
        
        for filename in os.listdir(ElemPath):
            file_path = os.path.join(ElemPath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(errorMsg(203, str(file_path), e))
                
        driver.get(DownloadVideoWebsiteUrl)

    driver.quit()
    
def Info4videoAccount1(url, author):
    return "The Word you want to put into the description"

def Info4videoAccount2(url, author):
    return "The Word you want to put into the description"




def GUI(DownloadVideoWebsiteUrl, ytlogin, ytuploadvideo,
        email, pwd,
        MainPath, ToolsPath, ElemPath, OutputPath, ffmpegExe, chromedriver_path, UsedUrlPath):
    sg.theme('LightGreen')

    SettingLayout = [

            [sg.Text('DownloadVideoWebsiteUrl :'), sg.Input(DownloadVideoWebsiteUrl, key='DownloadVideoWebsiteUrl')],
            [sg.Text('ytlogin :'), sg.Input(ytlogin, key='ytlogin', size=(90, 1))],
            [sg.Text('ytuploadvideo :'), sg.Multiline(ytuploadvideo, key='ytuploadvideo', size=(100, 2))],
            
            [sg.Text('email:'), sg.Input(default_text = email, key='email')],
            [sg.Text('pwd:'), sg.Input(default_text = pwd, key='pwd')],
            
            [sg.Text('MainPath :'),sg.Input(default_text = MainPath, key = 'MainPath', size=(90, 1)), sg.FolderBrowse(initial_folder = MainPath, target='MainPath')],
            [sg.Text('ToolsPath :'),sg.Input(default_text = ToolsPath, key='ToolsPath'), sg.FolderBrowse(initial_folder = ToolsPath, target='ToolsPath')],
            [sg.Text('ElemPath :'),sg.Input(default_text = ElemPath, key = 'ElemPath'), sg.FolderBrowse(initial_folder = ElemPath, target='ElemPath')],
            [sg.Text('OutputPath :'),sg.Input(default_text = OutputPath, key ='OutputPath'), sg.FolderBrowse(initial_folder = OutputPath, target='OutputPath')],
            
            [sg.Text('ffmpegExe :'),sg.Input(default_text = ffmpegExe, key = 'ffmpegExe'), sg.FilesBrowse(initial_folder  = ffmpegExe, target='ffmpegExe')],
            [sg.Text('chromedriver_path :'),sg.Input(default_text = chromedriver_path, key = 'chromedriver_path', size=(50, 1)), sg.FilesBrowse(initial_folder  = chromedriver_path, target='chromedriver_path')],
            [sg.Text('UsedUrlPath :'),sg.Input(default_text = UsedUrlPath, key = 'UsedUrlPath'), sg.FilesBrowse(initial_folder  = UsedUrlPath, target='UsedUrlPath')],
            

            [sg.Button('Update', key='Update')],
        ]
    
    MainLayout = [
            [sg.Radio("Account 1", "ChooseAcc", default=True, key = "ChooseAcc1"), sg.Radio("Account 2", "ChooseAcc", key = "ChooseAcc2")],
            
            [sg.Text('Step 1 --- Please follow the format : Title|Url|Author', key='Step1',size=(40, 1))],
            [sg.Multiline('', size=(140,8), key='InputTUA')],
            [sg.Button('Submit', key='submit1')],
            
            [sg.Text('Step 2 --- Please correct the error text below', key='Step2', size=(40, 1), visible=False)],
            [sg.Multiline('', size=(120,5), key='ErrorMsg', visible=False)],
            [sg.Button('Submit', key='submit2', visible=False)],

            [sg.Text('Step 3 --- Download the indtagram video', key='Step3', visible=False)],
        ]
    
    layout = [[sg.TabGroup([
        [sg.Tab(title='Main Page', layout = MainLayout), sg.Tab(title='Setting Page', layout = SettingLayout)]
        ])]]

    return layout

def ifExists(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def getResolution(videoPath):
    cap = cv2.VideoCapture(videoPath)
    return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def getDuration(video_file):
    cap = cv2.VideoCapture(video_file)
    return int(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS)))

def runErrorCheck(cmd):
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print('FFmpeg output:', result.stdout)
    except subprocess.CalledProcessError as e:
        print('FFmpeg error:', e.stderr)

    print(cmd)



def createVideoWithWord(word, deminishScale, backgroundColor, textColor, fileName, video_folder, final_folder, edit_folder, ffmpegExe):
    print("Start create Video With Word process")
    
    input_file = os.path.join(video_folder, fileName)
    
    width, height = getResolution(input_file)

    if(width != 1080 or height != 1920): 
        width, height = (1080, 1920)
    
    output_file = os.path.join(edit_folder, "output.mp4")
    #print(output_file)
    ifExists(output_file)
    deminished_cmd = [ffmpegExe,'-i', input_file, '-vf', f'scale=iw*{deminishScale}:-1','-c:v', 'libx264','-preset', 'slow','-crf', '22', output_file]
    runErrorCheck(deminished_cmd)

    
    white_file = os.path.join(edit_folder, "white.mp4")
    ifExists(white_file)
    background_white_cmd = [ffmpegExe, '-f', 'lavfi', '-i', f'color={backgroundColor}:s={str(width)}x{str(height)}', '-t', str(getDuration(output_file)), '-pix_fmt', 'yuv420p', white_file]
    runErrorCheck(background_white_cmd)

    output_final_file =  os.path.join(edit_folder, "output_final.mp4")
    ifExists(output_final_file)
    merge_cmd = [ffmpegExe, '-i', white_file, '-i', output_file, '-filter_complex', f'[0:v]pad=ceil(iw/2)*2:ceil(ih/2)*2 [background]; [background][1:v]overlay=(W-w)/2:(H-h)/2:shortest=1', output_final_file]
    runErrorCheck(merge_cmd)

    output_final_with_word_file = os.path.join(edit_folder, "output_final_with_word.mp4")
    ifExists(output_final_with_word_file)
    addText_cmd = [ffmpegExe, '-i', output_final_file, '-vf', f"drawtext=text='Rate 1 to 10, Comment below':fontfile=Humor-Sans.ttf:fontsize=50:fontcolor={textColor}:x=(w-tw)/2:y=50", '-c:a', 'copy', output_final_with_word_file]
    runErrorCheck(addText_cmd)
    time.sleep(5)

    output_final_with_word_muted_file = os.path.join(final_folder, f"{fileName}")
    ifExists(output_final_with_word_muted_file)
    mute_cmd = [ffmpegExe, '-i', output_final_with_word_file, '-vcodec', 'copy', '-an', output_final_with_word_muted_file]
    runErrorCheck(mute_cmd)

    ifExistsList = [output_file,white_file,output_final_file,output_final_with_word_file] 
    for IfExistsItem in ifExistsList:
        ifExists(IfExistsItem)
    print("Remove All unwanted file")


def videoEdit(TitleList, video_folder, final_folder, edit_folder, ffmpegExe):
    for i in range(len(TitleList)):
        input_file = os.path.join(video_folder, f"{i+1}.mp4")
        if os.path.exists(input_file):
            print("Start doing: ", input_file)
            createVideoWithWord(TitleList[i], 0.85, "black", "white", f"{i+1}.mp4", video_folder, final_folder, edit_folder, ffmpegExe)
            print("Done: ", input_file)
        else:
            print(f"file not found, please put all the videos in the {video_folder} folder!")
            break

            
    
def ProcessMain(Urls, chromedriver_path, ElemPath, OutputPath, DownloadVideoWebsiteUrl,
                email, pwd, ytlogin, ytuploadvideo, TitleList, UrlList, AuthorList, NumMain):
    
    DownIGvideo(Urls, chromedriver_path, ElemPath, OutputPath, DownloadVideoWebsiteUrl)

    videoEdit(TitleList, OutputPath, OutputPath, ElemPath, ffmpegExe)
    
    mp4_files = [f for f in os.listdir(OutputPath) if f.endswith(".mp4")]
    urlpath = [] 
    for mp4name in mp4_files:
        urlpath.append(OutputPath+mp4name)
        
    for i in range(len(os.listdir(OutputPath))):
        print(f"--------------------{i+1}----------------------")
        print(TitleList[i])
        if values['ChooseAcc1'] == True:
            print(Info4videoAccount1(UrlList[i], AuthorList[i]))
            
        elif values['ChooseAcc2'] == True:
            print(Info4videoAccount2(UrlList[i], AuthorList[i]))
        
        print("\n")

    sg.popup("Finish")
    

#All requirement

#YT Num
NumMain = 4

#website
DownloadVideoWebsiteUrl = "https://snapinsta.app/"
ytlogin = 'https://www.youtube.com/signin_prompt?app=desktop&next=https%3A%2F%2Fwww.youtube.com%2F'
ytuploadvideo = ""

#email and pwd
email = 'YourEmailAddress'+'\n'
pwd = 'YourPassword'+'\n'

#path
MainPath = os.path.abspath(os.getcwd()) 
ToolsPath = os.path.join(MainPath, "tools")
ElemPath = os.path.join(MainPath, "element")
OutputPath = os.path.join(MainPath, "output")
ffmpegExe = os.path.join(ToolsPath, "ffmpeg.exe")
chromedriver_path = os.path.join(MainPath, "chromedriver.exe")
UsedUrlPath = os.path.join(MainPath, "UsedUrl.txt")



if __name__ == "__main__":
    
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    if not os.path.exists(ElemPath):
        os.makedirs(ElemPath)

    layout = GUI(DownloadVideoWebsiteUrl, ytlogin, ytuploadvideo,
                 email, pwd,
                 MainPath, ToolsPath, ElemPath, OutputPath, ffmpegExe, chromedriver_path, UsedUrlPath)

    
    
    window = sg.Window('Your window name', layout)

    while True:
        event, values = window.read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        
        #Step 1
        if event == "submit1":              
            correctList = ""
            errorList = ""
            TitleList = []
            UrlList = []
            AuthorList = []
            
            TitleList, UrlList, AuthorList, correctList, errorList = ListFilter(values['InputTUA'])
            
            if(errorList == "\n" or errorList == ""):
                if (correctList == ""):
                    print(errorMsg(901))
                else:

                    window['Step1'].hide_row()
                    window['InputTUA'].hide_row()
                    window['submit1'].hide_row()
                    sg.popup_auto_close("Process Continue")

                    ProcessMain(UrlList, values['chromedriver_path'], values['ElemPath'], values['OutputPath'], values['DownloadVideoWebsiteUrl'],
                                values['email'], values['pwd'], values['ytlogin'], values['ytuploadvideo'], TitleList, UrlList, AuthorList, NumMain)
                    
            else:

                window['Step1'].hide_row()
                window['submit1'].hide_row()
                
                window['Step2'].update(visible=True)
                window['ErrorMsg'].update(visible=True)
                window['submit2'].update(visible=True)

                window['Step3'].hide_row()
                
                window['InputTUA'].update(value = correctList)
                window['ErrorMsg'].update(value = errorList)


        #Step 2
        if event == "submit2":
            TitleList, UrlList, AuthorList, correctList, errorList = ListFilter(values['ErrorMsg'], correctList, "", TitleList, UrlList, AuthorList)
            #for i in TitleList, UrlList, AuthorList, correctList, errorList:
                #print(i)
            window['InputTUA'].update(value = correctList)
            window['ErrorMsg'].update(value = errorList)
            
            if(errorList == ""):
                sg.popup("Complete the TUA text list")
                #print(TitleList, UrlList, AuthorList) #['5', '1', '1', '1'] ['6', '2', '3', '2'] ['7', '3', '4', '3']

                window['Step1'].hide_row()
                window['InputTUA'].hide_row()
                window['submit1'].hide_row()
                
                window['Step2'].hide_row()
                window['ErrorMsg'].hide_row()
                window['submit2'].hide_row()

                window['Step3'].update(visible=True)

                sg.popup_auto_close("Process Continue")
                
                ProcessMain(UrlList, values['chromedriver_path'], values['ElemPath'], values['OutputPath'], values['DownloadVideoWebsiteUrl'],
                            values['email'], values['pwd'], values['ytlogin'], values['ytuploadvideo'], TitleList, UrlList, AuthorList, NumMain)

                
        if event == "Update":
            window['DownloadVideoWebsiteUrl'].update()
            window['ytlogin'].update()
            window['ytuploadvideo'].update()
            
            window['email'].update()
            window['pwd'].update()
            
            window['MainPath'].update()
            window['ToolsPath'].update()
            window['ElemPath'].update()
            window['OutputPath'].update()
            
            window['ffmpegExe'].update()
            window['chromedriver_path'].update()
            window['UsedUrlPath'].update()
                                  
    window.close()
    









