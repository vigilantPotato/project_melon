#WordClipper.py
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
import tkinter.simpledialog #new

class WordClip(tkinter.LabelFrame):
    '''
    tkinterのラベルフレームオブジェクトを生成
    create_widget:
        ボタンを生成するメソッド
    word_clip:
        ボタンが押したときに実行されるメソッド
    get_word_list:
        同じフォルダ内のword_list.csvを開き、文字列を読み出すメソッド
    '''

    '''
    ボタンの表示名とクリップボードにコピーする文字列のリストを登録
    3番目にボタンクリック時にブラウザで開くアドレスを登録。
    但し、nolinkの場合はクリップボードへのコピーのみ。
    ここでは空のクラス変数を宣言しておき、get_word_listメソッドで
    同じフォルダにあるcsvファイルからデータを読み込む。
    ウィジェットの生成、破壊のために、ウィジェットのリストを追加
    '''
    word_list = []
    widget_list = [] #new
    
    def __init__(self, master=None):
        '''
        オブジェクト生成時に実行
        '''
        super().__init__(master, text='clip words', padx=5)
        self.get_word_list()
        self.create_widgets()
    
    def create_widgets(self):
        '''
        ボタンウィジェットを生成
        ボタンを押すと、word_clipメソッドを実行
        '''
        #word_listに登録されたボタンを生成
        for word in self.word_list:
            self.button_widget(word[0])
        
        #create_newボタンを生成
        self.button_widget('create new', bg='lightyellow')

    def word_clip(self, event):
        '''
        ボタンのタイトルをword_list内から検索し、
        対応する文字列をクリップボードにコピー
        アドレスがnolinkではない場合、ブラウザで開く
        crate newボタンを押した場合はcreate_newメソッドを実行
        '''

        if event.widget["text"] == 'create new':
            self.create_new()
        else:
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
        filename = os.path.join(os.getcwd(), 'word_list.csv')
        open_file = open(filename, 'w', newline='')
        output_writer = csv.writer(open_file)
        for words in self.word_list:
            output_writer.writerow(words)
        open_file.close()

        #すべてのボタンウィジェットを削除
        for d in self.widget_list:
            d.destroy()

        #create_widgetsを実行してボタンウィジェットを再生成
        self.create_widgets()
    
    def button_widget(self, title, bg='lightblue'):
        '''
        ボタンウィジェットを生成するメソッド
        '''
        b = tkinter.Button(self, text=title, width=20, bg=bg)
        b.bind("<ButtonRelease-1>", self.word_clip)
        b.pack()
        self.widget_list.append(b)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('WordClipper')
    app = WordClip(master=root)
    app.pack()
    root.mainloop()