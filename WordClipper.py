#WordClipper.py
'''
ボタンを押すとクリップボードに指定した文字列をコピーするアプリ
tkinterとpyperclipを使用
'''

import tkinter
import pyperclip
import webbrowser

class WordClip(tkinter.LabelFrame):
    '''
    tkinterのラベルフレームオブジェクトを生成
    create_widget:
        ボタンを生成するメソッド
    word_clip:
        ボタンが押したときに実行されるメソッド
    '''

    #ボタンの表示名とクリップボードにコピーする文字列のタプルを登録
    #3番目にボタンクリック時にブラウザで開くアドレスを登録。但し、nolinkの場合はクリップボードへのコピーのみ。
    word_list = [
        ['Google', 'Google!Google!Google!', 'https://www.google.com'],
        ['Yahoo', 'Yahoo!Yahoo!Yahoo!', 'https://www.yahoo.com'],
        ['nolink', 'nolink!nolink!nolink!', 'nolink'],
        ]
    
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
        for word in self.word_list:
            b = tkinter.Button(self, text=word[0], width=20)
            b.bind("<ButtonRelease-1>", self.word_clip)
            b.pack()

    def word_clip(self, event):
        '''
        ボタンのタイトルをword_list内から検索し、
        対応する文字列をクリップボードにコピー
        アドレス
        '''
        for title in self.word_list:
            if title[0] == event.widget["text"]:
                pyperclip.copy(title[1])
                if title[2] != 'nolink':
                    webbrowser.open(title[2])

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('WordClipper')
    app = WordClip(master=root)
    app.pack()
    root.mainloop()