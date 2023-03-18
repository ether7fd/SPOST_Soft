import tkinter

def screenpri(str1, str2, str3, str4, str5):
    root = tkinter.Tk()
    root.title(u"宅配送料")
    root.geometry("800x480")

    #ラベル
    Static3 = tkinter.Label(text=u' ',bg="black",height="30",width="100")
    Static3.pack()
    Static3.place(x=0,y=0)

    if str1 == 0:
        Static1 = tkinter.Label(anchor='w',justify='left',text="料金: 取扱なし",font=("MSゴシック", "80", "bold"),fg="white",bg="black")
    else:
        Static1 = tkinter.Label(anchor='w',justify='left',text="料金: "+str(str1)+" 円",font=("MSゴシック", "80", "bold"),fg="white",bg="black")
    #Static1.pack(side="middle")
    Static1.pack()
    Static1.place(x=10,y=20)

    if str2 == 1:
        Static2 = tkinter.Label(text="厚さ: 1cm以内",font=("MSゴシック", "40"),fg="white",bg="black",width=20,anchor='w',justify='left')
    else:    
        Static2 = tkinter.Label(text="厚さ: 1cm以上3cm未満",font=("MSゴシック", "40"),fg="white",bg="black",width=20,anchor='w',justify='left')
    #Static2.pack()
    Static2.place(x=10,y=160)

    Static3 = tkinter.Label(text="重量:{:.1f} g".format(str3),font=("MSゴシック", "40"),fg="white",bg="black",width=20,anchor='w')
    Static3.pack()
    Static3.place(x=10,y=230)
    
    st1 = "サイズ:{:.1f}".format(str4)
    st2 = "{:.1f} cm".format(str5)
    st3 = st1 + " cm ✕ " +st2
    Static4 = tkinter.Label(text=st3 ,font=("MSゴシック", "40"),fg="white",bg="black",width=20,anchor='w')
    Static4.pack()
    Static4.place(x=10,y=300)

    button = tkinter.Button(root, font=("MSゴシック", "30"), padx=10, pady=10, anchor='center', text="支払い完了", command=lambda:root.destroy())
    button.pack()
    button.place(x=280,y=380)

    root.mainloop()
