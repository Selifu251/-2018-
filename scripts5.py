def Main_Pyautogui(): #主要pyautogui腳本##( 有時滑鼠會有礙搜圖 )
    global picture_steps,picture_time_steps,click_pos_steps,click_pos_steps_time,while_cot_num
    data_num=0 #串列數
    no_find_num=0 #找不到圖的次數
    time_start=time.time() #開始計時
    while_cot=0
    if (while_cot_num==-1):
        while_cot=-5 #計算整個迴圈輪數
    while (while_cot < while_cot_num): #超過(目前預設3輪)輪數就結束
        if (data_num >= len(picture_steps)):
            data_num=0 #迴圈重頭
            if (while_cot_num==-1): #當是無限迴圈時
                while_cot=-5
            else:
                while_cot+=1 #算整個迴圈輪數
        if (text_imagetime.get()<=0 or text_imagetime.get()>=61): #當搜圖時間設定超過 1hr
            text_warn.set("搜圖時間請在1~60之間")
            break
        if (picture_steps[data_num]==""): #當無給予圖片進行搜查
            if (click_pos_steps[data_num]==""): #當無圖 也 無位置 時 結束
                text_warn.set("搜圖跟位置不能同時空白")
                break
            else: #當無圖 有位置 時 繼續
                time_end=time.time() #結束計時
                if (time_end-time_start >= click_pos_steps_time[data_num]): #當超過等待秒數
                    pos=click_pos_steps[data_num]
                    posl=pos.strip("(")
                    poslr=posl.strip(")")
                    pos_lis=[]
                    for z in poslr.split(", "):
                        pos_lis.append(int(z))
                    pyautogui.click(clicks=2,x=pos_lis[0],y=pos_lis[1])
                    data_num+=1
                    time_start=time.time() #重新計時
        else: #當有給予圖片時
            print("data_num=",data_num) #
            print("len(picture_steps)=",len(picture_steps)) #
            image_file=picture_steps[data_num]
            print("image_file=",image_file) #
            find_image=pyautogui.locateOnScreen(image_file)
            if (find_image==None): #假如未搜到圖片
                print("目前找無圖片") #
                no_find_num+=1
                time_end=time.time() #結束計時
                print("秒數:",time_end-time_start,"s") #
                print("no_find_num=",no_find_num) #
                image_time=text_imagetime.get()+picture_time_steps[data_num]
                if (time_end-time_start >= image_time*60): #搜圖超過幾分鐘後
                    if (click_pos_steps[data_num]==""): #當有圖沒搜到 無位置 時
                        print("time_end-time_start=",time_end-time_start,"秒")
                        text_warn.set(image_file+"找不到")
                        break
                    else: #當有圖可沒搜到 有位置 時
                        time_end=time.time() #結束計時
                        if (time_end-time_start >= click_pos_steps_time[data_num]): #當超過等待秒數
                            pos=click_pos_steps[data_num]
                            posl=pos.strip("(")
                            poslr=posl.strip(")")
                            pos_lis=[]
                            for z in poslr.split(", "):
                                pos_lis.append(int(z))
                            pyautogui.click(clicks=2,x=pos_lis[0],y=pos_lis[1])
                            data_num+=1
                            time_start=time.time() #重新計時
            else: #當搜到圖時
                print(find_image)
                image_x,image_y=pyautogui.center(find_image)
                #print(image_x,image_y) #
                pyautogui.click(clicks=2,x=image_x,y=image_y)
                no_find_num=0
                data_num += 1
                time_start=time.time() #重新計時
                    
    print("迴圈結束...") #
    text_warn2.set("[ 程式已結束 ]")

def Click_pos_change(): #選取位置按鈕變化
    global num_button
    if ((globals()["tcxy_button_%s"%(num_button)]).get()=="選取位置-{}".format(num_button+1)):
        (globals()["tcxy_button_%s"%(num_button)]).set("Shift讀取-{}".format(num_button+1))
    else:
        (globals()["tcxy_button_%s"%(num_button)]).set("選取位置-{}".format(num_button+1))
        

def Shift_click_pos(event): #按 Shift 後可讀取位置
    global num_button
    if (num_button==-5):
        text_warn2.set("")
    else:
        if ((globals()["tcxy_button_%s"%(num_button)]).get()=="Shift讀取-{}".format(num_button+1)):
            if (event.keycode==16):
                pos=str(pyautogui.position())
                (globals()["tcxy_%s"%(num_button)]).set(pos)

def Building_Entry():#建立圖檔選擇
    def On_Configure(event): #滑輪程式
        canvas_finimg.configure(scrollregion=canvas_finimg.bbox('all'))
        
    def Choose_While_cot():
        global while_cot_num
        if (choice_while.get()=="無限"):
            while_cot_num=-1
            text_warn.set("")
        else:
            if (text_choice_whilenum.get() > 0):
                while_cot_num=text_choice_whilenum.get()
                text_warn.set("")
            else:
                text_warn.set("迴圈數不可是零或負數")
            
    ######################################
    if (text_imagenum.get()>0): #不能小於0
        for fram_button in frame4.winfo_children(): #清空 frame4
            fram_button.destroy()
        
        canvas_finimg=tk.Canvas(frame4,width=550) #創造畫布
        canvas_finimg.pack(side=tk.LEFT)
        scrollbar_finimg=tk.Scrollbar(frame4,command=canvas_finimg.yview) #創造滑輪
        scrollbar_finimg.pack(side=tk.LEFT,fill='y')
        canvas_finimg.configure(yscrollcommand=scrollbar_finimg.set)
        canvas_finimg.bind('<Configure>',On_Configure)
        frame4_1=tk.LabelFrame(canvas_finimg) #在畫布上放 Frame
        canvas_finimg.create_window((0,0),window=frame4_1,anchor='nw')
        
        for num in range(0,text_imagenum.get()): #創造按鈕及 entry
            globals()["tics_%s" %(num)]=tk.StringVar() #image目錄
            globals()["tics_time_%s"%(num)]=tk.IntVar() #額外搜圖時間
            globals()["entry_imagchos_%s"%(num)]=tk.Entry(frame4_1,
                   textvariable=(globals()["tics_%s" %(num)]),width=25,justify="right") # Entry(放圖片)
            (globals()["entry_imagchos_%s"%(num)]).grid(row=num,column=0)
            #(globals()["entry_imagchos_%s"%(num)]).config(state=tk.DISABLED)
            globals()["button_imagchos_%s"%(num)]=tk.Button(frame4_1,
                   text="選取檔案-{}".format(num+1),command=Finding_Image_TK) # Button(放圖片)
            globals()["button_imagchos_%s"%(num)].bind("<Button-1>",Button_Event) #滑鼠點擊找編號
            (globals()["button_imagchos_%s"%(num)]).grid(row=num,column=1)
            globals()["entry_image_time_%s"%(num)]=tk.Entry(frame4_1,
                   textvariable=globals()["tics_time_%s"%(num)],width=2) #額外搜圖時間entry
            (globals()["entry_image_time_%s"%(num)]).grid(row=num,column=2)
            globals()["label_image_time_%s"%(num)]=tk.Label(frame4_1,text="額外時間")
            (globals()["label_image_time_%s"%(num)]).grid(row=num,column=3)
            
            globals()["tcxy_%s"%(num)]=tk.StringVar() #位置 entry
            globals()["tcxy_button_%s"%(num)]=tk.StringVar() #滑鼠點擊搜位置 的按鈕名稱
            globals()["tcxy_time_%s"%(num)]=tk.IntVar() # 幾秒後點擊位置
            globals()["entry_clickxy_%s"%(num)]=tk.Entry(frame4_1,
                   textvariable=(globals()["tcxy_%s"%(num)]),width=9) #之後滑鼠點擊位置
            (globals()["entry_clickxy_%s"%(num)]).grid(row=num,column=4)
            globals()["button_clickxy_%s"%(num)]=tk.Button(frame4_1,
                   textvariable=globals()["tcxy_button_%s"%(num)],command=Click_pos_change) #選取位置之按鈕
            (globals()["tcxy_button_%s"%(num)]).set("選取位置-{}".format(num+1))
            (globals()["button_clickxy_%s"%(num)]).bind("<Button-1>",Button_Event) #滑鼠點擊找編號
            win.bind("<Key>",Shift_click_pos)
            (globals()["button_clickxy_%s"%(num)]).grid(row=num,column=5)
            globals()["entry_clickxy_time_%s"%(num)]=tk.Entry(frame4_1,
                   textvariable=globals()["tcxy_time_%s"%(num)],width=4) #幾秒後點擊 Entry
            (globals()["entry_clickxy_time_%s"%(num)]).grid(row=num,column=6)
            globals()["label_clickxy_time_%s"%(num)]=tk.Label(frame4_1,text="秒後點擊") #幾秒後點擊 Label
            (globals()["label_clickxy_time_%s"%(num)]).grid(row=num,column=7)
            
        button_right=tk.Button(frame4_1,text="確定",command=Running_All_Entry) #確定按鈕(執行程式)
        button_right.grid(row=text_imagenum.get())
        frame4_1_1=tk.LabelFrame(frame4_1,text="搜圖最多")
        frame4_1_1.grid(row=text_imagenum.get(),sticky="e")
        entry_imagetime=tk.Entry(frame4_1_1,textvariable=text_imagetime,
                                 width=2,justify="right") #圖片的間隔時間
        text_imagetime.set(1)
        entry_imagetime.grid(row=0,column=0)
        label_imagetime_minute=tk.Label(frame4_1_1,text="分鐘") #label_分鐘
        label_imagetime_minute.grid(row=0,column=1)
        
        frame4_1_2=tk.LabelFrame(frame4_1,text="程式運作")
        frame4_1_2.grid(row=text_imagenum.get(),sticky="w")
        radiobutton_while_infinite=tk.Radiobutton(frame4_1_2,text="無限",value="無限"
                                                  ,variable=choice_while,command=Choose_While_cot) #單選 無限迴圈
        radiobutton_while_infinite.grid(row=0)
        radiobutton_while_num=tk.Radiobutton(frame4_1_2,text="有限",value="有限",
                                             variable=choice_while,command=Choose_While_cot) #單選 有限迴圈
        radiobutton_while_num.grid(row=1)
        text_choice_whilenum=tk.IntVar()
        entry_whilenum=tk.Entry(frame4_1_2,textvariable=text_choice_whilenum,width=2) #選擇的迴圈數
        entry_whilenum.grid(row=2)
        
    elif (text_imagenum.get()<=0):
        text_warn.set("不能為零")
    else:
        print("TryEntry() 錯誤...") #

def Running_All_Entry(): #選取圖片後之確認
    global picture_steps,picture_time_steps,click_pos_steps,click_pos_steps_time
    for i in range(0,text_imagenum.get()):
        print((globals()["tics_%s" %(i)]).get()) ###
        img=globals()["tics_%s"%(i)].get()
        img_time=(globals()["tics_time_%s"%(i)]).get()
        clickpos=(globals()["tcxy_%s"%(i)]).get()
        clickpos_time=(globals()["tcxy_time_%s"%(i)]).get()
        
        picture_steps.append(img)
        picture_time_steps.append(img_time)
        click_pos_steps.append(clickpos)
        click_pos_steps_time.append(clickpos_time)
    text_warn.set("")
    Main_Pyautogui()
        
def Button_Event(event): #滑鼠點擊獲取資訊
    global num_button
    textbutton=event.widget['text']
    texbut_lis=[]
    texbutnum_lis=[]
    for i in textbutton:
        texbut_lis.append(i)
    for j in texbut_lis: #利用除錯 找出數字
        try:
            type(int(j))==int
        except:
            print("",end="") #
        else:
            texbutnum_lis.append(j)
    word_num=""
    for k in range(0,len(texbutnum_lis)): #將數字字串合併
        word_num += texbutnum_lis[k]
    num_button=int(word_num)-1
            

def Finding_Image_TK():#尋找圖檔#####
    def Building_dir_listbox(num): #創建 listbox
        global alldir_lis,K
        K=num #判斷 K
        subfil=["子目錄","檔案"]
        for i in range(1,len(alldir_lis[num])):
            for j in range(0,len(alldir_lis[num][i])):
                listbox_subfil.insert(0,str(alldir_lis[num][i][j])+"\n")
            listbox_subfil.insert(0,"***"+subfil[i-1]+"***\n")
    
    def Running_listbox(event): ######點擊所選列表選項######
        global K
        select=listbox_subfil.curselection() # 選取的列表選項
        text_file=listbox_subfil.get(select) #選取的列表選項_名稱
        k,i,j=Existing_alldir_lis(text_file.rstrip(),K) #是否存在 alldir串列中
        Judging_alldir_lis(k,i,j,text_file.rstrip()) #判斷類別 及 執行
        
    def Existing_alldir_lis(file,k): #是否存在 alldir串列中
        global alldir_lis
        lis_1=-5
        lis_2=-5
        lis_3=-5
        for i in range(1,len(alldir_lis[k])):
            if (len(alldir_lis[k][i])==1): #假如只有一個 檔案 或 子目錄
                for j in alldir_lis[k][i]: #因為alldir_lis[k][i]為list不是str
                    if (file==j): #假如 選取=檔案(子目錄)
                        lis_1=k
                        lis_2=i
                        lis_3=-5
                        break
            elif (len(alldir_lis[k][i])>1): #假如許多個 檔案 或 子目錄
                for j in range(0,len(alldir_lis[k][i])):
                    if (file==alldir_lis[k][i][j]): #假如 選取=檔案(子目錄)
                        lis_1=k
                        lis_2=i
                        lis_3=j
                        break
        return lis_1,lis_2,lis_3 
    
    def Judging_alldir_lis(k,i,j,file): # 判斷類別 及 執行
        global num_button
        if (i==1):
            word=text_dirname.get()+"\\"+file ### word=子目錄的路徑
            for m in range(1,len(alldir_lis)): #尋找路徑目錄
                if (word==alldir_lis[m][0]):
                    listbox_subfil.delete(0,listbox_subfil.size())
                    Building_dir_listbox(m)
                    text_dirname.set(word)
                    break
        elif (i==2):
            #print("2-檔案") #
            refile=file[::-1]
            #print(refile[0:4])
            if (refile[0:4]!="GNP." or refile[0:4]!="gnp."):
                text_warn.set("不是PNG檔")
            else:
                text_warn.set("")
                print(num_button) #
                py_dir=text_dirname.get().replace(alldir_lis[0][0]+"\\","") #將前面目錄省略
                print(py_dir+"\\"+file) #
                file_dir=py_dir+"\\"+file
                globals()["tics_%s" %(num_button)].set(file_dir)
            
    ######## Finding_Image_TK() 主 #########
    small_win=tk.Toplevel(win) #建立子視窗
    small_win.geometry("440x200")
    smal_fram1=tk.Frame(small_win)
    smal_fram1.pack()
    text_dirname=tk.StringVar()
    entry_dirname=tk.Entry(smal_fram1,textvariable=text_dirname,width=60)
    text_dirname.set(alldir_lis[0][0])
    #entry_dirname.config(state=tk.DISABLED)
    entry_dirname.grid(row=0)
    
    listbox_subfil=tk.Listbox(smal_fram1,width=60)
    listbox_subfil.grid(row=1)
    Building_dir_listbox(0)
    listbox_subfil.bind("<Double-Button-1>",Running_listbox) #點擊 listbox 兩下
    
    small_win.mainloop()

def Building_alldir_lis(): #建立 alldir串列
    global alldir_lis
    cur_path=os.path.dirname(__file__) #程式所在路徑
    small_tree=os.walk(cur_path)
    for all in small_tree:
        alldir_lis.append(all)
    
################### 主程式 ###################################################
import tkinter as tk
import pyautogui,os,time

alldir_lis=[]
K=0 #主要用在Finding_Image_TK()
num_button=-5 #所選取的按鈕編號
Building_alldir_lis() #建立 alldir串列
picture_steps=[] #圖片步驟串列
picture_time_steps=[] #搜圖額外時間串列
click_pos_steps=[] #點擊位置串列
click_pos_steps_time=[] #幾秒後點擊位置時間串列
while_cot_num=0 # While 可迴圈數

win=tk.Tk()
win.geometry("600x300")

frame1=tk.Frame(win)
frame1.pack()
label_title=tk.Label(frame1,text="遊戲刷經外掛")
label_title.grid()

frame2=tk.Frame(win)
frame2.pack()
text_imagenum=tk.IntVar()
entry_imagenum=tk.Entry(frame2,textvariable=text_imagenum)
entry_imagenum.grid(row=0,column=0)
button_creatimgchose=tk.Button(frame2,text="創建",command=Building_Entry)
button_creatimgchose.grid(row=0,column=1)

frame3=tk.Frame(win)
frame3.pack()
text_warn=tk.StringVar()
text_warn2=tk.StringVar()
label_warn=tk.Label(frame3,textvariable=text_warn,fg="red")
label_warn.grid(row=0)
label_warn2=tk.Label(frame3,textvariable=text_warn2,fg="red")
label_warn2.grid(row=1)

frame4=tk.LabelFrame(win)
frame4.pack()
text_imagetime=tk.IntVar() #圖片間隔時間
choice_while=tk.StringVar() # While 迴圈數


win.mainloop()