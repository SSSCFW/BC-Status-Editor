import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import traceback
import codecs

json_file = open("data/language.json", "r", encoding="utf-8_sig")
setting_file = open("data/setting.json", "r", encoding="utf-8_sig")

setting = json.load(setting_file)
lang = setting["lang"]
lang_file = json.load(json_file)[lang]


status = lang_file[0]

status_form = [[],[],[]]

idir = setting["path"]
idir2 = setting["path2"]

def file_select():
    global idir
    global status_form
    filetype = [("CSV","unit*.csv"), (lang_file[1],"*")]
    file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
    if not file_path:
        return
    input_box.delete(0, tk.END)
    input_box.insert(tk.END, file_path)
    idir = file_path
    status_form = [[],[],[]]
    with open(idir, encoding="utf-8") as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            if i > 2: break # 4行目以降は無視
            status_form[i] = list(filter(None, l.rstrip("\n").replace(" ", "").replace("", "").replace("", "").replace("", "").split("/")[0].split(",")))
    tree.delete(*tree.get_children())
    for i, v in enumerate(max(status_form[0],status_form[1],status_form[2])): # 3つの形態の中の最大値を取得
        add_item(i)

def add_item(i):
    if len(status) > i: st = status[i]
    else: st = "None"
    st_form = []
    for cs in range(3):
        if len(status_form[cs]) > i:
            st_form.append(status_form[cs][i])
        else:
            st_form.append(0)
            if i in [55,57,66]: st_form[cs] = -1  # 初期値が-1の部分
            if i in [63]: st_form[cs] = 1  # 初期値が1の部分
    tree.insert(parent="", index="end",values=(i+1, st, st_form[0], st_form[1], st_form[2]))

def remove_item():
    tree.delete(tree.get_children()[-1])

def select_item():
    selected = tree.focus()
    temp = tree.item(selected, "values")
    input_f1.delete(0, tk.END)
    input_f2.delete(0, tk.END)
    input_f3.delete(0, tk.END)
    input_f1.insert(tk.END, temp[2])
    input_f2.insert(tk.END, temp[3])
    input_f3.insert(tk.END, temp[4])

def update_item():
    selected = tree.focus()
    temp = tree.item(selected, "values")
    try: tree.item(selected, values=(temp[0], temp[1], input_f1.get(), input_f2.get(), input_f3.get()))
    except: return

def save():
    status1 = []
    status2 = []
    status3 = []
    for i in tree.get_children():
        temp = tree.item(i, "values")
        status1.append(temp[2])
        status2.append(temp[3])
        status3.append(temp[4])
    try:
        status1 = str(list(map(int, status1))).strip("[]").replace(" ", "")
        status2 = str(list(map(int, status2))).strip("[]").replace(" ", "")
        status3 = str(list(map(int, status3))).strip("[]").replace(" ", "")
    except:
        return print("エラー: intに変換できない文字が含まれています。")
    msg = status1+"\n"+status2+"\n"+status3+"\n"
    need = 16-(len(msg)+3)%16
    if need != 16:
        msg += " "*need
    with open(idir, mode="w") as f:
        f.write(msg)
    if idir2:
        path2 = idir2+"/"+idir.split("/")[-1]
        with open(path2, mode="w") as f:
            f.write(msg)

def range_converter():
    try:
        get_range = range_input.get().split("~")
        max_range = int(get_range[0])
        min_range = int(get_range[1])
        after_range = [max_range, min_range-max_range]
        range_input.delete(0, tk.END)
        range_input.insert(tk.END, f"min: {after_range[0]} max: {after_range[1]}")
    except:
        print(traceback.format_exc())

def change_language(lng):
    setting["lang"] = lng
    #言語設定部分。 json書き換え
    j_w = codecs.open("data/setting.json" , 'w', 'utf-8')
    json.dump(setting, j_w,indent=2, ensure_ascii=False)
    j_w.close()
    msg = "再起動してください。\nRestart the editor."
    messagebox.showinfo("info", msg)

root = tk.Tk()
root.geometry("800x500")
root.title(lang_file[2])

column = ("ID", lang_file[3], lang_file[4], lang_file[5], lang_file[6])
tree = ttk.Treeview(root, columns=column)
tree.column("#0",width=0, stretch="no")
tree.column("ID", anchor="w", width=30)
tree.column(lang_file[3], anchor="w", width=180)
tree.column(lang_file[4],anchor="center", width=80)
tree.column(lang_file[5],anchor="center", width=80)
tree.column(lang_file[6],anchor="center", width=80)
tree.heading("ID", text="ID",anchor="center")
tree.heading(lang_file[3], text=lang_file[3],anchor="center")
tree.heading(lang_file[4], text=lang_file[4], anchor="center")
tree.heading(lang_file[5], text=lang_file[5], anchor="center")
tree.heading(lang_file[6], text=lang_file[6], anchor="center")

tree.pack(pady=50)

input_box = tk.Entry(width=120)
input_box.place(x=50, y=10)

input_box2 = tk.Entry(width=120)
input_box2.place(x=50, y=25)
input_box2.insert(tk.END, idir2)

range_input = tk.Entry(width=50)
range_input.place(x=500, y=400)

range_label = tk.Label(text=lang_file[7])
range_label.place(x=500, y=360)

range_button = tk.Button(text=lang_file[8], command=range_converter)
range_button.place(x=430, y=400)

input_label = tk.Label(text=lang_file[9])
input_label.place(x=10, y=0)

button = tk.Button(text=lang_file[10],command=file_select)
button.place(x=10, y=50)

btn = tk.Button(text=lang_file[11], command=lambda: add_item(len(tree.get_children())))
btn.place(x=135, y=280)

btn2 = tk.Button(text=lang_file[12], command=remove_item)
btn2.place(x=135, y=310)

lng_label = tk.Label(text="Language")
lng_label.place(x=700, y=60)

lng_eng = tk.Button(text="English", command=lambda: change_language("English"))
lng_eng.place(x=700, y=80)

lng_jpn = tk.Button(text="日本語", command=lambda: change_language("日本語"))
lng_jpn.place(x=700, y=110)

select = tk.Button(text=lang_file[13], command=select_item)
select.place(x=220, y=280)

select2 = tk.Button(text=lang_file[14], command=update_item)
select2.place(x=220, y=310)

savebtn = tk.Button(text=lang_file[15], command=save)
savebtn.place(x=530, y=295)

#input_label = tk.Label(text="遠方範囲:\n開始(最小射程)\n終わり(開始+入力値=最大射程)\n例: 500~700->開:500 終:200\n全方範囲:\n開始(最大射程)\n終わり(最小射程-最大射程=最小射程)\n例: -320~500->開:500 終:-820")
#input_label.place(x=500, y=350)

input_f1 = tk.Entry(width=40)
input_f1.place(x=280, y=280)

input_f2 = tk.Entry(width=40)
input_f2.place(x=280, y=300)

input_f3 = tk.Entry(width=40)
input_f3.place(x=280, y=320)

root.mainloop()

