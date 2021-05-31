from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import pytesseract
from googletrans import Translator
from playsound import playsound
from gtts import gTTS
from PIL import Image
app = Flask(__name__)
img_new=0
x=0
#y=""
lang1=0
lang2=0
langy1=0
langy2=0
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

text1=''
text2=''
text3=''

@app.route('/inter1', methods=['GET','POST'])
def dropdown():
    colours1 = ['English', 'Chinese', 'Hindi', 'Telugu', 'Bengali', 'German', 'Russian']
    colours2 = ['English', 'Chinese', 'Hindi', 'Telugu', 'Bengali', 'German', 'Russian']
    global lang1
    global lang2
    global langy1
    global langy2
    if request.method == 'POST':
        if request.form['coloursa']== 'English':
            lang1='eng'
            langy1="English"
        elif request.form['coloursa']== 'Chinese':
            lang1='chi_sim'
            langy1="Chinese"
        elif request.form['coloursa']== 'Hindi':
            lang1='hin'
            langy1="Hindi"
        elif request.form['coloursa']== 'Telugu':
            lang1='tel'
            langy1="Telugu"
        elif request.form['coloursa']== 'Bengali':
            lang1='ben'
            langy1="Bengali"
        elif request.form['coloursa']== 'German':
            lang1='deu'
            langy1="German"
        elif request.form['coloursa']== 'Russian':
            lang1='rus'
            langy1="Russian"
        else:
            pass
        if request.form['coloursb']== 'English':
            lang2='en'
            langy2="English"
        elif request.form['coloursb']== 'Chinese':
            lang2='zh-cn'
            langy2="Chinese"
        elif request.form['coloursb']== 'Hindi':
            lang2='hi'
            langy2="Hindi"
        elif request.form['coloursb']== 'Telugu':
            lang2='te'
            langy2="Telugu"
        elif request.form['coloursb']== 'Bengali':
            lang2='bn'
            langy2="Bengali"
        elif request.form['coloursb']== 'German':
            lang2='de'
            langy2="German"
        elif request.form['coloursb']== 'Russian':
            lang2='ru'
            langy2="Russian"
        else:
            pass
        global text1
        global text2
        global text3
        img_new = cv2.imread(r'C:\Users\dwara\Downloads\MintyPaper.png')
        #img_new = Image.open(r'C:\Users\dwara\Downloads\MintyPaper.png')
        gray = get_grayscale(img_new)
        thresh = thresholding(gray)
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, thresh)
        text1= pytesseract.image_to_string(Image.open(filename), lang=lang1)
        os.remove(filename)
        translator = Translator()
        text2=translator.translate(text=text1, dest=lang2)
        text3=str(text2.text)
        text3=text3.strip()
        if text3 == "":
            file = 'MintyPaper.png'
            location =r"C:\Users\dwara\Downloads"
            path = os.path.join(location, file)
            os.remove(path)
            #return redirect(url_for('output2'))
            #global y
            #y="THIS IMAGE DOES NOT CONTAIN ANY TEXT. PLEASE UPLOAD ANOTHER IMAGE"
            global x
            x=1
            return redirect(url_for('dropdown'))
        file = 'MintyPaper.png'
        location =r"C:\Users\dwara\Downloads"
        path = os.path.join(location, file)
        os.remove(path)
        
        return redirect(url_for('output'))
    return render_template('inter1.html', colours1=colours1, colours2=colours2, x=x)

@app.route('/inter2', methods=['GET', 'POST'])
def output():
    global text1
    global text2
    global text3
    global langy1
    global langy2
    
    #if request.method == 'POST':
    #    fname='tempv.mp3'
    #    loc=r"C:\Users\dwara\Desktop\dj\projnew2"
    #    myobj = gTTS(text=text1, lang='en', slow=False)
    #    myobj.save(fname)
    #    playsound(fname)
    #    pt=os.path.join(loc, fname)
    #    os.remove(pt)
    if request.method == 'POST':
        fname='tempc.mp3'
        loc=r"C:\Users\dwara\Desktop\dj\projnew2"
        myobj = gTTS(text=text3, lang='en', slow=False)
        myobj.save(fname)
        playsound(fname)
        pt=os.path.join(loc, fname)
        os.remove(pt)
    return render_template('inter2.html', text1=text1, text2=text3, langy1=langy1, langy2=langy2)
#@app.route('/inter3')
#def output2():
#    return render_template('inter3.html')

if __name__ == "__main__":
    app.debug = False
    app.run()