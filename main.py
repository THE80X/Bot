from datetime import datetime
import vk_api
import pypyodbc
import os
import time
import sqlite3

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import main_token, group_token, name_by_id
vk_session = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, group_token)
#longpoll = VkLongPoll(vk_session)
#цифирки отвечают за id группы

spec_symbol='"'
vk_admin_permission = ['593644570', '404872983', '678212445', '655707464 ', '457933399']
counter_messages = 0

def make_camp (msg,msg_id_sender,id,hero_name):
    sender(id, hero_name+" разбил лагерь")

def take_a_rest (msg,msg_id_sender,id,hero_name):
    sender(id, hero_name+" отдыхает")

def using_item(msg, msg_id_sender, id, hero_name, item_name,item_target):
    s=''
    hero_name_for_check = (hero_name.replace(' ', '')).lower()
    item_target_for_check = (item_target.replace(' ', '')).lower()
    counter_comma = item_target.count(',')
    if (hero_name_for_check != item_target_for_check):
        if counter_comma == 0:
            sender(id, hero_name + " использует " + item_name + " на" + item_target)
        else:
            for i in range(counter_comma+1):
                person_target = item_target.split(',')
                if person_target[i][0:1] == ' ':
                    person_target[i] = person_target[i][1:]
                    print(person_target[i])
                    if counter_comma > i:
                        if person_target[i] == hero_name:
                            s= s + "на себе,"
                        else:
                            s= s + " на " + person_target[i] + ','
                    else:
                        if person_target[i] == hero_name:
                            s= s + "на себе"
                        else:
                            s= s + " на " + person_target[i]
            sender(id,hero_name + " использует "+item_name +' '+ s)
    if (hero_name_for_check == item_target_for_check):
        sender(id, hero_name + " использует " + item_name + " на себе")
# абилити надо будет тоже обязательно поправить

def using_ability(msg,msg_id_sender,id,hero_name,ability_name,ability_target):
    hero_name_for_check = (hero_name.replace(' ', '')).lower()
    ability_target_for_check = (ability_target.replace(' ', '')).lower()

    if (hero_name_for_check != ability_target_for_check):
        sender(id, hero_name + " использует " + ability_name + " на" + ability_target)


    if (hero_name_for_check == ability_target_for_check):
        sender(id, hero_name + " использует " + ability_name + " на себе")

def end_of_the_journey(msg,msg_id_sender,id,hero_name,target):
    hero_name_for_check = (hero_name.replace(' ', '')).lower()
    target_for_check = (target.replace(' ', '')).lower()

    if (hero_name_for_check != target_for_check):
        sender(id, hero_name + " закончил путешествие " + target + ". " +'"'+ "Cпи спокойно друг мой"+'"')

    if (hero_name_for_check == target_for_check):
        sender(id, hero_name + " закончил своё путешествие. " + spec_symbol + "Конец неминуем, и ты отдохнёшь" + spec_symbol)

def add_item_in_inventory(msg,msg_id_sender,id,hero_name,target,list_of_items):
    print(hero_name)
    print(target)
    hero_name_for_check = (hero_name.replace(' ','')).lower()
    target_for_check = (target.replace(' ','')).lower()
    if (hero_name_for_check != target_for_check):
        s=''
        counter_comma = list_of_items.count(',') + 1
        if list_of_items.count(',') != 0:
            items = list_of_items.split(',')
            for i in range(counter_comma):
                item = items[i].replace(' ', '')
                counter_dash = items[i].count('-')
                if counter_dash > 0:
                    dash_position = int(str(item).find('-'))
                    print("dash_position: "+ str(dash_position))
                    print(str(item)[:dash_position])
                    if (str(item)[:dash_position]).isdigit():
                        amount = int(str(item)[:dash_position])
                        print("amount: "+ str(amount))
                        item_name = str(items[i])[(str(items[i]).find('-'))+1:]
                        if counter_comma >= i:
                            s = s + str(amount) + ' ' + item_name + '\n'
                        else:
                            s = s + str(amount) + ' ' + item_name
                else:
                    if counter_comma >= i:
                        s = s + str(items[i]) + '\n'
                    else:
                        s = s + str(items[i])


        if list_of_items.count(',') == 0:
            print(list_of_items.count(','))
            item = list_of_items.replace(' ', '')
            counter_dash = item.count('-')

            if counter_dash > 0:
                print("counter_dash: " + str(counter_dash))
                dash_position = int(str(item).find('-'))
                print("dash_position: " + str(dash_position))
                if str(item)[:dash_position].isdigit():
                    amount = int(str(item)[:(str(item).find('-'))])
                    item_name = str(list_of_items)[(str(list_of_items).find('-')) + 1:]
                    print(amount)
                    s = s + str(amount) + ' ' + item_name
                else:
                    sender(id, "У вас ошибка в колличестве предметов, исправьтесь!")
            else:
                s = s + str(item)
        sender(id, hero_name + " наградил " + target + " предеметами:" +'\n' + s)
    else:
        sender(id, "А зачем самому себе предметы передавать?")


def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})
    counter_some = vk_session.method('messages.getHistory', {'count': 1, 'peer_id': '-'+group_token, 'group_id':group_token})
    print(counter_some)

def admin_check(vk_admin_permission,msg_id_sender):
    x = False
    for i in vk_admin_permission:
        #print(i)
        if int(i) == msg_id_sender:
            x = True
    #print(x)
    return x

def replacer(msg):
    msg = msg.replace('“', '"')
    msg = msg.replace('”', '"')
    msg = msg.replace('«', '"')
    msg = msg.replace('»', '"')
    msg = msg.replace('–', '-')
    return msg

for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                msg = event.object.message['text']
                replacer(msg)
                msg_all_info = event.message
                msg_id = event.object.message['conversation_message_id']                                #айдишник сообщения в чатах, где пребывает бот
                msg_id_sender = event.object.message['from_id']                                         #айдишник отправителя сообщений, где пребывает бот
                id = event.chat_id                                                                      #айдишник чата
                msg_time_send = datetime.now()
                user = vk_session.method('users.get', {'user_ids': msg_id_sender, 'name_case': 'nom'})
                msg_fullname_sender = user[0]['first_name'] + ' '+user[0]['last_name']
                counter = msg.count('|')


                print('\n'+"сообщение: " + msg)
                print("кол-во палок: " + str(counter))
                print("кол-во черток: " + str(msg.count(spec_symbol)))
                print("кол-во обращений к людям: " + str(msg.count("[")))
                print("id сообщения: " + str(msg_id))
                print("id беседы: " + str(id))
                print("Название беседы: " + str(name_by_id[id]))
                print("id собеседника: " + str(msg_id_sender))
                print("имя и фамилия собеседника: " + str(msg_fullname_sender))
                print("Время отправки сообщения: " + str(msg_time_send))


                if id == 3:
                    if msg.count('|')>=2:
                        massive = msg.split('|')
                        person_name = massive[1]
                        if os.path.exists("персонажи/посты/" + person_name.lower() + ".rtf"):
                            f = open("персонажи/посты/" + person_name.lower() + ".rtf", 'r')
                            text_old = f.read()
                            f.close()
                            f = open("персонажи/посты/" + person_name.lower() + ".rtf", 'w')
                            print("Старое текст: " + text_old)
                            f.write(text_old + msg + '\n')
                            f.close()
                        else:
                            vk_session.method('messages.delete', {'spam': 0, 'delete_for_all': 1, 'peer_id': 2000000000 + id,'cmids':msg_id})
                    else:
                        vk_session.method('messages.delete', {'spam': 0, 'delete_for_all': 1, 'peer_id': 2000000000 + id,'cmids':msg_id})


                if id == 1:
                    if ((msg.count('|') - msg.count("["))) == 4:
                        massive = msg.split("|")
                        if massive[0]== "!Имя ":
                            name_old = massive[1].lower()
                            name_new = massive[3].lower()
                            if os.path.exists("персонажи/посты/"+name_old+".rtf"):
                                f = open("персонажи/посты/"+name_old+".rtf")
                                Owner_line = f.readline()
                                Owner_data = Owner_line.split("|")
                                Owner = Owner_data[1]
                                print("Владелец: " + Owner)
                                f.close()
                                if (int(Owner) == int(msg_id_sender)):
                                    f_old = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Посты", name_old + ".rtf")
                                    f_new = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Посты", name_new + ".rtf")
                                    os.rename(f_old,f_new)
                                    f_old = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Владельцы", name_old + ".rtf")
                                    f_new = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Владельцы", name_new + ".rtf")
                                    os.rename(f_old, f_new)
                                    f_old = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Инвентарь", name_old + ".rtf")
                                    f_new = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Инвентарь", name_new + ".rtf")
                                    os.rename(f_old, f_new)
                                    f_old = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Статистики", name_old + ".rtf")
                                    f_new = os.path.join("D:\\Pythonchick\\Bot\\Персонажи\\Статистики", name_new + ".rtf")
                                    os.rename(f_old, f_new)
                                    sender(id, "Имя персонажа было успешно изменено")
                                else:
                                    sender(id, "У вас нет такого персонажа")
                            else:
                                sender(id, "Нет такого персонажа")
                                print("Старое имя: "+name_old)

                    if ((msg.count('|') - msg.count("["))) == 2 | msg.count(spec_symbol) == 0:
                        massive = msg.split("|")
                        print(massive[0])
                        print(massive[1])
                        #Бан
                        if ((massive[0]== "!Смерть ") or (massive[0]== "!Казнь ")):
                            if admin_check(vk_admin_permission, msg_id_sender):
                                #print("ВРЕМЯ УБИВАТЬ!")
                                #vk_session.method('messages.delete', {'spam': 0, 'delete_for_all': 1, 'peer_id': 2000000000 + id, 'cmids': msg_id})
                                sender(id, "Казнил " + massive[1])
                        #Создание персонажа в списках
                        if ((massive[0] =="!Создать ") or (massive[0]=="!создать ")):
                            if admin_check(vk_admin_permission, msg_id_sender):
                                massive[1]=massive[1].lower()
                                print("создаётся " + str(massive[1]))
                                my_file = open( "Персонажи/Посты/" + str(massive[1])+".txt", "w+")
                                my_file.close()
                                my_file = open("Персонажи/Инвентарь/"+str(massive[1])+".txt", "w+")
                                my_file.write("|Артефакты|"+"\n\n"+"|Расходники|")
                                my_file.close()
                                my_file = open("Персонажи/Владельцы/"+str(massive[1])+".txt", "w+")
                                my_file.write("|Владельцы|" + str(massive[2]) + "\n" + "|Совладельцы|"+str(massive[2]))
                                my_file.close()
                                my_file = open("Персонажи/Статистики/"+str(massive[1])+".txt", "w+")
                                my_file.write("НРИ СТАТУС|0" + "\n" + "Статистики|SP|MP|IP|PP|AP|FP|LP|CP|BP"+"\n" +"Здоровье|0"+"\n" + "Рассудок|0"+"\n" +"Стамина|0"+"\n" + "Мана|0"+"\n" + "Локация|"+"\n"+"Статус боя|0"+"\n" +"Репутация|0")
                                my_file.close()
       #то что ниже потом перенести в перечень команд на ролевой
                    #if msg.count(spec_symbol) == 0 and ((msg.count('|') - msg.count("["))) == 4:


                    if (msg.count('|') - msg.count("[")) == 4:
                        massive = msg.split('|')
                        if ((str(massive[3]) == "Разбить лагерь") or (str(massive[3]) == "разбить лагерь")):
                            hero_name = massive[1]
                            make_camp(msg,msg_id_sender,id,hero_name)
                        if ((str(massive[3]) =="отдыхать") or (str(massive[3]) == "Отдыхать")):
                            hero_name = massive[1]
                            take_a_rest(msg,msg_id_sender,id,hero_name)

                    if (msg.count('|') - msg.count("[")) == 4:
                        massive = msg.split('|')
                        action = str(massive[3])[0:massive[3].find(' ', 0)]
                        action = action.strip(' ')
                        print(action)
                        if action == "Использовать" or action == "использовать":
                            hero_name = massive[1]
                            item_name = action[1]
                            item_target = action[2]

                            using_item(msg,msg_id_sender,id,hero_name,item_name,item_target)
                        if action == "Умение" or action == "умение":
                            db = sqlite3.connect('db/database.db')

                            hero_name = massive[1]
                            ability_name = str(massive[3])[massive[3].find('"', 0)+1:massive[3].rfind('"', 0)]
                            ability_target = str(massive[3])[massive[3].rfind('"', 0)+1:]

                            db.close()
                            using_ability(msg,msg_id_sender,id,hero_name,ability_name,ability_target)
                        if action == "Закопать" or action == "закопать":
                            hero_name = massive[1]
                            target = str(massive[3])[massive[3].find(' ', 0)+1:]

                            end_of_the_journey(msg,msg_id_sender,id,hero_name,target)
                        if action == "Отдать" or action == "отдать":
                            hero_name = massive[1]
                            target = str(massive[3])[massive[3].find(' ', 0)+1:massive[3].find('"', 0)]
                            target = target.strip(' ')
                            print(target)
                            list_of_items = str(massive[3])[massive[3].find('"', 0)+1:massive[3].rfind('"', 0)]
                            print(list_of_items)

                            add_item_in_inventory(msg, msg_id_sender, id, hero_name, target, list_of_items)
                        #if action == "Переместиться" or action == "переместиться":
