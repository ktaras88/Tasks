import sys, os
import imaplib, email

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Enter name of program and 2 arguments: mail and pass")
    elif sys.argv[1] == '-h':
        print (''' 
        Цей додаток для роботи із поштою ukr.net. Для успішної роботи, потрібно 
        у налаштуваннях поштової скриньки вибрати закладку «Керування IMAP-доступом» і поставити 
        галочку «Доступ до зовнішніх програм». Для початку роботи у консолі введіть через пробіл 
        назву додатку, логін і пароль ukr.net: <program_name>.py <user_name@ukr.net> <password>.

        1 - Показує список папок в акаунті
        2 - показу список листів у вибраній папці. (ввести через пробіл 2 і назву папки)
        3 - Загружає файл із вибраного листа. (ввести через пробіл 3, номер повідомлення, назву файлу під яким він буде збережений )
        x - вийти
        ''')
    elif len(sys.argv) > 3:
        print ("Enter name of program and 2 arguments: mail and pass")

   
    elif len (sys.argv) == 3:
        print ("Press number: \n 1 - Show Folders \n 2 - Show Mails in Folder \n 3 - Download email \n x - exit")

        try:
            mail = imaplib.IMAP4_SSL('imap.ukr.net')
            mail.login(sys.argv[1], sys.argv[2])
            mailbox = mail.list()
        except :
            print('Email or password is incorrect')
            sys.exit()
        
        while True:
            number = input('Number: ')
            num = number.split()
            if num[0] == 'x':
                sys.exit()

            if num[0] == '1':
                if mailbox[0] == 'OK':
                    for folder in mailbox[1]:
                        end = folder.decode("utf-8").index(')')
                        boxes = bytes.decode(folder[2:end], "utf-8")
                        print('-', boxes)
                
            elif num[0] == '2' and len(num) == 2:
                try:
                    mail.select(num[1].capitalize())
                    result, data = mail.uid('search', None, "ALL")
                    for item_list in data[0].split():
                        result2, email_data = mail.uid('fetch', item_list, '(RFC822)')
                        email_message = email.message_from_bytes(email_data[0][1]) 
                        p_from = email_message['From']
                        p_date = email_message["Date"]
                        p_subject = email_message["Subject"]
                        print(f'{item_list} : {p_from} : {p_date} : {p_subject}')
                except:
                    print('Enter correct name of folder')
            elif num[0] == '2':
                print('After number 2 enter name of folder')

            elif num[0] == '3' and len(num) == 3:
                detach_dir = 'c:/downloads'
                letter = num[1].encode('UTF-8')

                for box in mailbox[1]:
                    end = box.decode("utf-8").index(')')
                    boxes = bytes.decode(box[2:end], "utf-8")
                    mail.select(boxes)
                    result, data = mail.uid('search', None, "ALL")  
                    if letter in data[0].split():
                        mail.select(boxes)
                        result2, email_data = mail.uid('fetch', letter, '(RFC822)')
                        email_message = email.message_from_bytes(email_data[0][1])

                        if email_message.get_content_maintype() != 'multipart':
                            continue
                        p_from = email_message['From']
                        p_date = email_message["Date"]
                        print(f'{letter} : {p_from} : {p_date}')

                        for part in email_message.walk():
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get('Content-Disposition') is None:
                                continue
                            att_path = os.path.join(detach_dir, num[2])
                            if not os.path.isfile(att_path) :
                                with open(att_path, 'wb') as fp:
                                    fp.write(part.get_payload(decode=True))
            elif len(num) < 3 or len(num) > 3:
                print('After number 3 enter number of message and name of file')