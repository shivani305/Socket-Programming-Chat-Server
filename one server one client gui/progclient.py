import socket
from sys import *
from tkinter import *
import _thread

def LoadMyEntry(ChatBox, EntryText):
    if EntryText != '':
        ChatBox.config(state=NORMAL)
        if ChatBox.index('end') != NONE :
            LineNumber = float(ChatBox.index('end'))-1.0
            ChatBox.insert(END, "You: " + EntryText)
            ChatBox.tag_add("You", LineNumber, LineNumber+0.4)
            ChatBox.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"))
            ChatBox.config(state=DISABLED)
            ChatBox.yview(END)
    return EntryText

def LoadOtherEntry(ChatBox, EntryText):
    global LineNumber
    if EntryText != '':
        ChatBox.config(state=NORMAL)
        if ChatBox.index('end') != NONE :
            try:
                LineNumber = float(ChatLog.index('end'))-1.0
            except:
                pass
            ChatBox.insert(END, "Other: " + EntryText)
            ChatBox.tag_add("Other", LineNumber, LineNumber+0.6)
            ChatBox.tag_config("Other", foreground="#04B404", font=("Arial", 12, "bold"))
            ChatBox.config(state=DISABLED)
            ChatBox.yview(END)
    return EntryText

def LoadConnectionInfo(ChatBox, EntryText):
    if EntryText != '':
        ChatBox.config(state=NORMAL)
        if ChatBox.index('end') != None:
            ChatBox.insert(END, EntryText+'\n')
            ChatBox.config(state=DISABLED)
            ChatBox.yview(END)

def FilteredMessage(EntryText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(EntryText)-1,-1,-1):
        if EntryText[i]!='\n':
            EndFiltered = EntryText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return EntryText


WindowTitle = 'Chat-Client'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
port=12345


# ---------------------------------------------------#
# ------------------ MOUSE EVENTS -------------------#
# ---------------------------------------------------#
def ClickAction():
    # Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0", END))
    LoadMyEntry(ChatLog, EntryText)

    # Scroll to the bottom of chat windows
    ChatLog.yview(END)

    # Erace previous message in Entry Box
    EntryBox.delete("0.0", END)

    # Send my mesage to all others
    s.sendall(EntryText.encode())


# ---------------------------------------------------#
# ----------------- KEYBOARD EVENTS -----------------#
# ---------------------------------------------------#
def PressAction(event):
    EntryBox.config(state=NORMAL)
    ClickAction()


def DisableEntry(event):
    EntryBox.config(state=DISABLED)


# ---------------------------------------------------#
# -----------------GRAPHICS MANAGEMENT---------------#
# ---------------------------------------------------#

# Create a window
root = Tk()
root.title(WindowTitle)
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

# Create a Chat window
ChatLog = Text(root, bd=0, bg="white", height="8", width="50", font="Arial", )
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)

# Bind a scrollbar to the Chat window
scrollbar = Scrollbar(root, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create the Button to send message
SendButton = Button(root, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=ClickAction)

# Create the box to enter message
EntryBox = Text(root, bd=0, bg="white", width="29", height="5", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

# Place all components on the screen
scrollbar.place(x=376, y=6, height=386)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)


# ---------------------------------------------------#
# ----------------CONNECTION MANAGEMENT--------------#
# ---------------------------------------------------#

def ReceiveData():
    try:
        s.connect(('10.250.14.157', port))
        LoadConnectionInfo(ChatLog,
                           '[ Succesfully connected ]\n---------------------------------------------------------------')
    except:
        LoadConnectionInfo(ChatLog, '[ Unable to connect ]')
        return

    while 1:
        try:
            data = (s.recv(1024)).decode()
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            LoadOtherEntry(ChatLog, data)
        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
            # s.close()


_thread.start_new_thread(ReceiveData, ())

root.mainloop()
