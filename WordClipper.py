#WordClipper.py
'''
ボタンを押すとクリップボードに指定した文字列をコピーするアプリ
tkinterとpyperclipを使用
'''

import tkinter
import pyperclip

class WordClip(tkinter.LabelFrame):
    '''
    tkinterのラベルフレームオブジェクトを生成
    word_list:
        クラス変数 ボタンの表示名と押したときにコピーされる文字列を指定
        word_list = [ ['ボタンの表示名', 'クリップボードにコピーする文字列'], …　]
    create_widget:
        ボタンを生成するメソッド
    word_clip:
        ボタンが押したときに実行されるメソッド
    '''

    #ボタンの表示名とクリップボードにコピーする文字列のタプルを登録
    word_list = [
        ['aaa', 'aaa'],
        ['bbb', 'bbb'],
        ['ccc', 'ccc'],
        ]
    
    def __init__(self, master=None):
        '''
        オブジェクト生成時に実行
        '''
        super().__init__(master)
        self.create_widgets()
    
    def create_widgets(self):
        '''
        ボタンウィジェットを生成
        ボタンを押すと、word_clipメソッドを実行
        '''
        for word in self.word_list:
            b = tkinter.Button(self, text=word[0])
            b.bind("<ButtonRelease-1>", self.word_clip)
            b.pack()

    def word_clip(self, event):
        '''
        ボタンのタイトルをword_list内から検索し、対応する文字列をクリップボードにコピー
        '''
        for title in self.word_list:
            if title[0] == event.widget["text"]:
                pyperclip.copy(title[1])

if __name__ == '__main__':
    root = tkinter.Tk()
    app = WordClip(master=root)
    app.pack()
    root.mainloop()