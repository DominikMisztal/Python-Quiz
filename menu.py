import PySimpleGUI as sg
import requests
import json
import pprint
import random
import html.parser as htmlparser

url_easy = "https://opentdb.com/api.php?amount=1&category=15&difficulty=easy&type=multiple"
url_medium = "https://opentdb.com/api.php?amount=1&category=15&difficulty=medium&type=multiple"
url_hard = "https://opentdb.com/api.php?amount=1&category=15&difficulty=hard&type=multiple"

def main():
    questions_amount = 0
    points = 0
    column_to_be_centered = [  [sg.Text('Welcome to video games knowledge quiz.\nFirst, you select the difficulty.', key='-MAIN_TEXT-')],
                [sg.Text(size=(12,1), key='-OUT-')],
                [sg.Button('Easy', button_color=('white', 'dark blue')), sg.Button('Medium', button_color=('white', 'dark blue')), sg.Button('Hard', button_color=('white', 'dark blue'))],
                [sg.Text(size=(12,1), key='-OUT-')],
                [sg.Button('Exit', button_color=('white', 'dark blue'))]  ]

    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0,0),key='-EXPAND2-'),              # the thing that expands from left
               sg.Column(column_to_be_centered, vertical_alignment='center', justification='center',  k='-C-')]]

    window = sg.Window('Video game quiz', layout, resizable=True,finalize=True)
    


    while True:             # Event Loop
        event, values = window.read()
        if(event == 'Easy'):
            difficulty = 'easy'
            break
        elif(event == 'Medium'):
            difficulty = 'medium'
            break
        elif(event == 'Hard'):
            difficulty = 'hard'
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    if(event == sg.WIN_CLOSED or event == 'Exit'):
        quit()


    window_created = False
    while(True):
        if(difficulty.lower() == "easy"):
            request = requests.get(url_easy)
            if(request.status_code != 200):
                window.Element('-MAIN_TEXT-').update('Failed to recover questions')
                print("Failed to recover questions")
                quit()
        elif(difficulty.lower() == "medium"): 
            request = requests.get(url_medium)
            if(request.status_code != 200):
                print("Failed to recover questions")
                quit()  
        else:
            request = requests.get(url_hard)
            if(request.status_code != 200):
                print("Failed to recover questions")
                quit()
                
        question = json.loads(request.text) 

        answers = []
        answers.append(htmlparser.unescape(question['results'][0]['correct_answer']))
        correct_answer = answers[0]
        answers.append(htmlparser.unescape(question['results'][0]['incorrect_answers'][0]))
        answers.append(htmlparser.unescape(question['results'][0]['incorrect_answers'][1]))
        answers.append(htmlparser.unescape(question['results'][0]['incorrect_answers'][2]))
        random.shuffle(answers)

        question_text = "Question: " + htmlparser.unescape(question['results'][0]['question'])

        window.hide()
        if(window_created == False):  
            column_to_be_centered = [  [sg.Text(question_text, key='MAIN_TEXT')],
                    #[sg.Text(size=(12,1), key='-OUT-')],
                    [sg.Button(answers[0], button_color=('white', 'dark blue'), key='A'), sg.Button(answers[1],button_color=('white', 'dark blue'), key='B'), sg.Button(answers[2], button_color=('white', 'dark blue'), key='C'), sg.Button(answers[3],button_color=('white', 'dark blue'), key='D') ],
                    [sg.Text('Current points: 0', key='points')],
                    [sg.Text(size=(12,1), key='-OUT-')],
                    [sg.Button('Exit',button_color=('white', 'dark blue')), sg.Button('Next', button_color=('white', 'dark blue'), visible=False)] ]

            layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
                [sg.Text('', pad=(0,0),key='-EXPAND2-'),              # the thing that expands from left
                sg.Column(column_to_be_centered, vertical_alignment='center', justification='center',  k='-C-')]] 

            window_created = True
            window2 = sg.Window('Video game quiz', layout, resizable=True,finalize=True)

        else:
            window2.Element('MAIN_TEXT').update(question_text)
            window2.Element('A').update(answers[0])
            window2.Element('B').update(answers[1])
            window2.Element('C').update(answers[2])
            window2.Element('D').update(answers[3])
  
        selected = False
        points_updated = False
        while True:             # Event Loop
            event, values = window2.read()
            if(event == 'A' and selected == False):
                selected = True
                final_answer = answers[0]
                selected_answer = 'A'
            elif(event == 'B' and selected == False):
                selected = True
                final_answer = answers[1]
                selected_answer = 'B'
            elif(event == 'C' and selected == False):
                selected = True
                final_answer = answers[2]
                selected_answer = 'C'
            elif(event == 'D' and selected == False):
                selected = True
                final_answer = answers[3]
                selected_answer = 'D'
            if(selected == True):
                window2.Element('Next').update(visible=True)
                if(final_answer == correct_answer):
                    if points_updated == False:
                        points = points + 1
                        points_updated = True
                    window2.Element('points').update('Current points: %d' % points)
                    window2.Element(selected_answer).update(button_color=('white', 'green'))
                else:
                    if(answers[0] == correct_answer):
                        window2.Element('A').update(button_color=('white', 'green'))
                    elif(answers[1] == correct_answer):
                        window2.Element('B').update(button_color=('white', 'green'))
                    elif(answers[2] == correct_answer):
                        window2.Element('C').update(button_color=('white', 'green'))
                    elif(answers[3] == correct_answer):
                        window2.Element('D').update(button_color=('white', 'green'))
                    window2.Element(selected_answer).update(button_color=('white', 'red'))
            if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Next':
                break
        if(event == 'Next'):
            window2.Element('Next').update(visible=False)
            window2.Element('A').update(button_color=('white', 'dark blue'))
            window2.Element('B').update(button_color=('white', 'dark blue'))
            window2.Element('C').update(button_color=('white', 'dark blue'))
            window2.Element('D').update(button_color=('white', 'dark blue'))
            continue
        if(event == sg.WIN_CLOSED or event == 'Exit'):
            break
    window2.close()
    window.close()

if __name__ == '__main__':
    main()