import pandas as pd
from datetime import datetime
import re
import os 

def get_chat_dataframe(file):
    data = []
    stream_name = file[7:-4]

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')
        for line in lines:
            try:
                time_logged = line.split('—')[0].strip()
                time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                username_message = '—'.join(username_message).strip()

                username, channel, message = re.search(
                        ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
                ).groups()

                d = {
                    'dt': time_logged,
                    'channel': channel,
                    'username': username,
                    'message': message
                }

                data.append(d)

            except Exception:
                pass
    
    
    df =  pd.DataFrame().from_records(data)

    df.to_csv("./csv/" + stream_name + ".csv")
    #return df

def main():


    try: 
        os.mkdir("./csv")
    except FileExistsError:
        pass

    for filename in os.listdir("./logs/"):
        print(filename)
        if filename.endswith(".log"):
            get_chat_dataframe("./logs/" + filename)
        else:
            continue

if __name__ == '__main__':
    main()
