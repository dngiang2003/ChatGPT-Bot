from customtkinter import CTk, CTkTextbox, CTkEntry, CTkButton
import openai
import os
from threading import Thread

def destroyAll():
    try:
        rootAPI.destroy()
    except:
        pass
    root.destroy()


root = CTk()
root.geometry('550x570+1200+80')
root.title('ChatGPT Bot @dngiang2003')
root.protocol('WM_DELETE_WINDOW', destroyAll)
root.iconbitmap(r'data\chatgpt.ico')
root.tk.call('tk', 'scaling', 1.3)
root.resizable(False, False)
root.attributes('-topmost', True)

textbox = CTkTextbox(master=root,width=510,height=400)

textbox.pack(side='top', padx=10, pady=15)


def clearText():
    textbox.delete('0.0', 'end')


def sendText(text):
    clearText()
    textbox.insert('0.0', text)


def getKey():
    try:
        readKey = open(r'data\APIChatGPT.txt', 'r')
        key = readKey.readline()
        readKey.close()
    except FileNotFoundError:
        key = 'null'
    return key


def saveHistory(ques, ans):
    if os.path.isfile('history.csv'):
        writeFile = open('history.csv', 'a', encoding='utf-8')
        writeFile.write(f'{ques}, {ans}\n')
        writeFile.close()
    else:
        writeFile = open('history.csv', 'a', encoding='utf-8')
        writeFile.write(f'question, answer\n{ques}, {ans}\n')
        writeFile.close()


def askChatGPT():
    def getAns():
        openai.api_key = getKey()
        prompt = entryQues.get()

        if openai.api_key == 'null':
            sendText('Vui lòng kiểm tra lại API Key!')
            return

        if prompt == '' or prompt == ' ':
            sendText('Vui lòng điền câu hỏi!')
            return

        sendText('ChatGPT đang trả lời...')
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=4000)
            message = response.choices[0].text.strip()
        except:
            message = 'Vui lòng kiểm tra lại API Key!'
        sendText(message)
        saveHistory(prompt, message)

    Thread(target=getAns).start()


def updateAPI():
    def cancel():
        buttonUpdateAPI.configure(state='normal')
        rootAPI.destroy()

    def confirm():
        with open(r'data\APIChatGPT.txt', 'a+', encoding='utf-8') as wf:
            wf.write(entryAPI.get().strip())
        wf.close()
        cancel()

    def disable_event():
        pass

    buttonUpdateAPI.configure(state='disabled')

    global rootAPI
    rootAPI = CTk()
    rootAPI.title('Update APT Key')
    rootAPI.geometry('380x140')
    rootAPI.iconbitmap(r'data\chatgpt.ico')
    rootAPI.tk.call('tk', 'scaling', 1.3)
    rootAPI.protocol('WM_DELETE_WINDOW', disable_event)
    rootAPI.resizable(False, False)
    rootAPI.attributes('-topmost', True)

    entryAPI = CTkEntry(master=rootAPI,
                                      placeholder_text=' Please enter the ChatGPT API',
                                      width=340,
                                      height=35,
                                      border_width=2,
                                      corner_radius=5)
    entryAPI.pack(side='top', padx=10, pady=20)

    btnUpdateTrue = CTkButton(master=rootAPI,
                                            width=140,
                                            height=35,
                                            border_width=0,
                                            corner_radius=6,
                                            fg_color='#1ba164',
                                            hover_color='#177349',
                                            text='Confirm API new',
                                            command=confirm)
    btnUpdateTrue.place(x=25, y=80)

    btnUpdateFalse = CTkButton(master=rootAPI,
                                            width=140,
                                            height=35,
                                            border_width=0,
                                            fg_color='#1ba164',
                                            hover_color='#177349',
                                            corner_radius=6,
                                            text='Cancel',
                                            command=cancel)
    btnUpdateFalse.place(x=215, y=80)

    rootAPI.attributes('-topmost', True)
    rootAPI.mainloop()


entryQues = CTkEntry(master=root, placeholder_text=' Questions for ChatGPT',
                                   width=510,
                                   height=45,
                                   border_width=2,
                                   corner_radius=5)
entryQues.pack(side='top', padx=10, pady=15)

buttonAsk = CTkButton(master=root, width=135,
                                    height=35,
                                    border_width=0,
                                    fg_color='#1ba164',
                                    hover_color='#177349',
                                    corner_radius=6,
                                    text='Speak To ChatGPT',
                                    command=askChatGPT)
buttonAsk.place(x=22, y=510)

buttonClear = CTkButton(master=root, width=135,
                                    height=35,
                                    border_width=0,
                                    fg_color='#1ba164',
                                    hover_color='#177349',
                                    corner_radius=6,
                                    text='Clear Response',
                                    command=clearText)
buttonClear.place(x=208, y=510)

buttonUpdateAPI = CTkButton(master=root,
                                        width=135,
                                        height=35,
                                        border_width=0,
                                        fg_color='#1ba164',
                                        hover_color='#177349',
                                        corner_radius=6,
                                        text='Update API Key',
                                        command=updateAPI)
buttonUpdateAPI.place(x=395, y=510)

root.mainloop()