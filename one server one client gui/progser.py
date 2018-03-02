import socket
from sys import *
from tkinter import *
import _thread


def FilteredMessage(EntryText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(EntryText) - 1, -1, -1):
        if EntryText[i] != '\n':
            EndFiltered = EntryText[0:i + 1]
            break
    for i in range(0, len(EndFiltered), 1):
        if EndFiltered[i] != "\n":
            return EndFiltered[i:] + '\n'
    return EntryText


def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText + '\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def LoadMyEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            LineNumber = float(ChatLog.index('end')) - 1.0
            ChatLog.insert(END, "You: " + EntryText)
            ChatLog.tag_add("You", LineNumber, LineNumber + 0.4)
            ChatLog.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
    return EntryText

def LoadOtherEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            try:
                LineNumber = float(ChatLog.index('end')) - 1.0
            except:
                pass
            ChatLog.insert(END, "Other: " + EntryText)
            ChatLog.tag_add("Other", LineNumber, LineNumber + 0.6)
            ChatLog.tag_config("Other", foreground="#04B404", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
    return EntryText


WindowTitle = 'Chat- Server'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
port=12345
s.bind(('10.250.14.157',port))


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
ChatLog = Text(root, bd=0, bg="white",height="8", width="50",  font="Arial", )
ChatLog.insert(END, "Waiting for your partner to connect..\n")
ChatLog.config(state=DISABLED)

# Bind a scrollbar to the Chat window
scrollbar = Scrollbar(root, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create the Button to send message
SendButton = Button(root, font=30, text="Send", width="12", height="5",
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
def GetConnected():
    s.listen(10)
    global connection
    connection, client_address = s.accept()
    LoadConnectionInfo(ChatLog, 'Connected with: ' + str(
        client_address) + '\n---------------------------------------------------------------')

    while True:
        try:
            data = (connection.recv(1024)).decode()
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            LoadOtherEntry(ChatLog, data)
        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break

_thread.start_new_thread(GetConnected, ())

root.mainloop()
