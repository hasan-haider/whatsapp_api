import csv
import os

import flask
from flask import request
#from config import Config

application = flask.Flask(__name__)
#application.config.from_object(Config)

questions=['Start?','Reply to start feedback:\n\nPlease respond answers in range 1 to 5']
with open('questions.csv','r') as file:
    reader=csv.reader(file)
    lst=[col for row in reader for col in row]
    #print(lst,questions,'before')
    questions.extend(lst)
    #print(questions,'after')
#print(questions)

@application.route('/')
@application.route('/home')
def home():
    return "Nothing here"


from helperfunction.waSendMessage import sendMessage,addFeedback


@application.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    print(request.get_data())
    message = request.form['Body']
    senderId = request.form['From'].split('+')[1]
    filled_flag=0
    #print(message, 'whatsapp')
    curr_q=questions[0]
    next_q=questions[1]
    with open('stud_feedback.csv', 'r', newline='\n') as f:
        reader=csv.reader(f)
        maxdate = ''
        for lines in reversed(list(reader)):
            print(maxdate)
            #try:
            if senderId in lines[2]:
                if lines[3]<maxdate:
                    break
                else:
                    maxdate=lines[3]
                    print(lines)

                    if questions[len(questions)-1] in lines[0]:
                        filled_flag=1
                        print('filled',filled_flag)
                        break
                    elif questions[len(questions)-2] in lines[0]:
                        curr_q = questions[questions.index(lines[0]) + 1]
                        next_q = 'Completed all questions. Thanks'
                    elif lines[0] in questions:
                        curr_q=questions[questions.index(lines[0])+1]
                        next_q=questions[questions.index(lines[0])+2]
                    '''for i in range(len(questions)-2):#[0,1,2,3]
                        if questions[i-1] in lines[0]:
                            curr_q = questions[i]
                            next_q=questions[i+1]'''
                    print(lines,next_q,'next_q',curr_q)

            '''except:
                print('No lines')
                curr_q = questions[1]
                next_q = questions[2]'''
    if filled_flag==1:
        message='You have already filled your feedback. Thank you'
    else:
        if message.isnumeric() and curr_q not in questions[:2]:
            if int(message) in range(6):
                feedback = addFeedback(senderId, message,curr_q)
                print('Feedback submit number')
                if feedback=='Feedback submitted successfully':
                    message=next_q
                    print('submitted next msg',message)
            else:
                message = curr_q
                print('wrong number return current', curr_q)
        elif curr_q==questions[0] or curr_q==questions[1]:
            feedback = addFeedback(senderId, message, curr_q)
            print('Feedback submit')
            if feedback == 'Feedback submitted successfully':
                message = next_q
                print('start submitted next msg', message)
        else:
            message=curr_q
            print('msg current',curr_q)
            '''if msgs_in.count(senderId)<4:
            message=addFeedback(senderId,message)
            msgs_in.append(senderId)
        if message!='Feedback submitted successfully':
            print('else response')
            message=response_msg'''

    print(f'Response Message --> {message}')
    print(f'Sender id --> {senderId}')
    res = sendMessage(senderId=senderId, message=message)
    #print(f'This is the response --> {res}')

    return '200'


if __name__ == "__main__":
    application.run(port=5000, debug=True)
