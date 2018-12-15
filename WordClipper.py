#python3.6.6
'''
ボタンを押すとクリップボードに指定した文字列をコピーするアプリ
リンク先を登録しておくと、クリックと同時にブラウザでリンク先を開く
tkinter, pyperclip, webbrowser, os, csvを使用
'''

import tkinter
import pyperclip
import webbrowser
import os
import csv
import tkinter.simpledialog

class WordClip(tkinter.LabelFrame):
    '''
    tkinterのラベルフレームオブジェクトを生成
    create_widget:
        ボタンを生成するメソッド
    word_clip:
        ボタンが押したときに実行されるメソッド
    get_word_list:
        同じフォルダ内のword_list.csvを開き、文字列を読み出すメソッド
    create_new:
        新規のボタンを登録するメソッド
    button_widget:
        ボタンを生成するメソッド
    '''

    '''
    ボタンの表示名とクリップボードにコピーする文字列のリストを登録
    3番目にボタンクリック時にブラウザで開くアドレスを登録。
    但し、nolinkの場合はクリップボードへのコピーのみ。
    ここでは空のクラス変数を宣言しておき、get_word_listメソッドで
    同じフォルダにあるcsvファイルからデータを読み込む。
    ウィジェットの生成、破壊のために、ウィジェットのリストを追加
    　→インスタンス変数に変更
    '''

    def __init__(self, master=None):
        '''
        オブジェクト生成時に実行
        '''
        super().__init__(master, text='clip words', padx=5)
        self.create_widgets()
    
    def create_widgets(self):
        '''
        ボタンウィジェットを生成
        ボタンを押すと、word_clipメソッドを実行
        '''
        self.word_list = []
        self.widget_list = []
        self.get_word_list()

        #word_listに登録されたボタンを生成
        for word in self.word_list:
            self.button_widget(word[0])
        
        #create_newボタンを生成
        self.button_widget('create new', bg='lightyellow')

        #deleteチェックボタンを生成
        self.var = tkinter.BooleanVar()
        self.delete_check = tkinter.Checkbutton(self, text='delete button', variable=self.var)
        self.widget_list.append(self.delete_check)
        self.delete_check.pack(anchor=tkinter.W, padx=5)

        #swapチェックボタンを生成
        self.var_s = tkinter.BooleanVar()
        self.swap_check= tkinter.Checkbutton(self, text='swap button', var=self.var_s, command=self.swap_checked)
        self.swap_check.bind("<ButtonRelease-1>")
        self.widget_list.append(self.swap_check)
        self.swap_check.pack(anchor=tkinter.W, padx=5)

    def swap_checked(self):
        self.swap_list=[]
        self.var.set(False)
        if self.var_s.get() == True:
            self.delete_check.config(state='disable')
        else:
            self.delete_check.config(state='active')

    def swap_buttons(self, text):
        if text == 'create new':
            return
        
        self.swap_list.append(text)
        if len(self.swap_list) == 2:
            for i, word in enumerate(self.word_list):
                if word[0] == self.swap_list[0]:
                    swap1 = i
                if word[0] == self.swap_list[1]:
                    swap2 = i
            self.word_list[swap1], self.word_list[swap2] =self.word_list[swap2], self.word_list[swap1]
            self.delete_check.config(state='active')
            self.renew_CSV()
            self.destroy_widgets()
            self.create_widgets()

    def word_clip(self, event):
        '''
        ボタンのタイトルをword_list内から検索し、
        対応する文字列をクリップボードにコピー
        アドレスがnolinkではない場合、ブラウザで開く
        crate newボタンを押した場合はcreate_newメソッドを実行
        deleteチェックボックスにチェックがある場合は
        delete_clip_buttonを実行して押したボタンを削除
        '''

        #deleteチェックボタンにチェックが入っている場合
        if self.var.get() == True:
            self.delete_clip_button(event.widget["text"])
            return

        #swapチェックボタンにチェックが入っている場合
        if self.var_s.get() == True:
            self.swap_buttons(event.widget["text"])
            return

        #create newボタンを押した場合
        if event.widget["text"] == 'create new':
            self.create_new()
            return
        
        #クリップボタンを押した場合
        for title in self.word_list:
            if title[0] == event.widget["text"]:
                pyperclip.copy(title[1])
                #nolink以外のとき、アドレスをブラウザで開く
                if title[2] != 'nolink':
                    webbrowser.open(title[2])
    
    def get_word_list(self):
        '''
        同じフォルダにあるword_list.csvから文字列を読み出し、クラス変数word_listに格納する。
        '''
        filename = os.path.join(os.getcwd(), 'word_list.csv')
        if os.path.exists(filename):
            open_file = open(filename)
            file_reader = csv.reader(open_file)
            for row in file_reader:
                self.word_list.append(row)

    def create_new(self):
        '''
        新規にword_listに追記するメソッド
        タイトル、コピーする文字列、リンク先を入力し、CSVファイルを更新
        最後に、ボタンウィジェットを破壊&再生成する
        '''

        #タイトルを入力
        title = tkinter.simpledialog.askstring('input title', 'please input title')
        if(title == ''):
            return

        #コピーする文字列を入力
        clip_word = tkinter.simpledialog.askstring('input clipword', 'please input clipword')
        if(clip_word == ''):
            return
        
        #リンク先を入力
        link = tkinter.simpledialog.askstring('input URL', 'please input URL')
        if(link == None or link == ''):
            link = 'nolink'
        
        #CSVファイルを更新
        self.word_list.append([title, clip_word, link])
        self.renew_CSV()

        #すべてのボタンウィジェットを削除
        self.destroy_widgets()

        #create_widgetsを実行してボタンウィジェットを再生成
        self.create_widgets()
    
    def button_widget(self, title, bg='lightblue'):
        '''
        ボタンウィジェットを生成するメソッド
        '''
        b = tkinter.Button(self, text=title, bg=bg, width=15)
        b.bind("<ButtonRelease-1>", self.word_clip)
        b.pack()
        self.widget_list.append(b)
    
    def delete_clip_button(self, title):
        '''
        CSVファイルからtitleと一致する行を削除しするメソッド
        '''
        for i, word in enumerate(self.word_list):
            if word[0] == title:
                del self.word_list[i]
                break
        self.renew_CSV()
        self.destroy_widgets()
        self.create_widgets()

    def renew_CSV(self):
        '''
        word_listをCSVファイルに保存するメソッド
        ファイルの存在確認を追加
        '''
        filename = os.path.join(os.getcwd(), 'word_list.csv')
        open_file = open(filename, 'w', newline='')
        output_writer = csv.writer(open_file)
        for words in self.word_list:
            output_writer.writerow(words)

    def destroy_widgets(self):
        for d in self.widget_list:
            d.destroy()
        self.widget_list = []

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('WordClipper')
    x = 155
    w = root.winfo_screenwidth()
    root.geometry('+%d+%d' % (w-x, 0))
    app = WordClip(master=root)
    app.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
    root.mainloop()