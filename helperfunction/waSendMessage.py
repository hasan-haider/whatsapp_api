import csv
import os
import datetime
from twilio.rest import Client
import snowflake.connector


ACCOUNT_SID = 'AC5ce8925b35bf141b043e368fcd90cf7a'
AUTH_TOKEN = 'c4e0eaceee7c4f6312b532652f268aad'
FROM = 'whatsapp:+14155238886'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

ctx = snowflake.connector.connect(
    user='Hasan',
    password='Hasan@12345',
    account='xk13894.ap-southeast-1'
)


def sendMessage(senderId, message):
    res = client.messages.create(
        body=message,
        from_=FROM,
        to=f'whatsapp:+{senderId}'
    )
    return res


def addFeedback(senderId, message, curr_q):
    print(message, 'addfeedbackmsg')
    questions=['Start?','Reply to start feedback:\n\nPlease respond answers in range 1 to 5']
    # print(messages,'addfeedback')
    if curr_q not in questions:
        cs = ctx.cursor()
        try:
            q = curr_q
            feedback = message
            cs.execute("USE WAREHOUSE ingestion_wh")
            values = "('" + q + "','" + feedback + "','" + senderId + "','" + str(datetime.datetime.now()) + "')"
            insert_stat = "insert into TRUSTED_ADVISOR_DEV.landing.STG_STUD_FEEDBACK_SEED values " + values
            print(insert_stat)
            cs.execute(insert_stat)
            # one = cs.fetchone()
            # print(one[0])
            print('Feedback submitted to snowflake successfully')
            '''except:
                print('Error in snowflake')'''
        finally:
            cs.close()

    try:
        q = curr_q
        feedback = message

        with open('stud_feedback.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            # writer.writerow(header)  # header
            writer.writerow([q, feedback, senderId, datetime.datetime.now()])
        return 'Feedback submitted successfully'
    except:
        print('Error')
