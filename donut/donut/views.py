from django.http import HttpResponse
from django.core import mail
from django.core.mail import send_mail
import pandas as pd
from donut.models import ConnectedPair, Donut_Group
import random
from django.core.mail import EmailMessage



def get_ids(group_num):
    group_obj = Donut_Group.objects.get(id=group_num)
    csv_name = group_obj.csv_name
    print(csv_name)
    users = pd.read_csv(csv_name)
    ids = users['id']
    emails = users['email']
    return ids

def get_constraint_dict(group_num,ids):
    
    #get all pairs that have been done before
    pairs = ConnectedPair.objects.filter(connected_group=group_num)
    #count the number of the constraints there are for each ID
    constraint_dict = {}
    for id in ids:
        constraint_dict[id] = []
    
    for pair in pairs:
        constraint_dict[pair.userid1].append(pair.userid2)
        constraint_dict[pair.userid2].append(pair.userid1)

    return constraint_dict

def check_for_total_collisions(ids,constraint_dict):
    for id1 in ids:
        constraints = constraint_dict[id1]
        for id2 in ids:
            if(id2 == id1):
                continue
            if(id2 not in constraints):
                break
        else:
            # if we reached the end of that for loop
            # without breaking
            # we have a node that colides with every other node
            print("TOTAL COLLISION ON USER", id1)
            print("TODO: email this user and restart them in the service")
            # currently we will just remove all colissions for this user
            # as though they opted in for another round
            constraint_dict[id1] = []
    return constraint_dict


def log_connection(user1,user2,group_num):
    print("we logged",user1,"and",user2,"as making a connection in our database")
    group_obj = Donut_Group.objects.get(id=group_num)
    new_pair = ConnectedPair(userid1=user1,userid2=user2,connected_group=group_obj)
    new_pair.save()




def send_email(user1,user2,group_num):
    #connection = mail.get_connection()
    #connection.open()
    print("wooosh we sent an email to",user1,"and",user2)

    message =  'Hello '+ str(user1) + " and "+str(user2)+"\n"
    message += "I'm your friendly pairing bot and both of you belong to the group: "+str(group_num)+"\n"
    message += "I suggest you two go get some bagles or coffee somewhere\n"
    message += "you are both cc'd in this email so feel free to organize here\n"
    user1_email = "alaird@uci.edu"
    user2_email = "lairdandrew11@gmail.com"
    email = EmailMessage(
        'Hello',
        message,
        user1_email,
        [user1_email],
        [],
        reply_to=[user1_email],
        headers={'Message-ID': 'foo'},
        #connection=connection,
    )
    email.send()
    #connection.close()

def create_pairs(group_num):
    ids = get_ids(group_num)

    constraint_dict = get_constraint_dict(group_num,ids)
    #check to make sure that no one can't match with anyone
    constraint_dict = check_for_total_collisions(ids,constraint_dict)
    print(constraint_dict)

    # sort the id's so that we remove the ones with the most 
    # constraints first
    ordered_ids = sorted(ids,key=lambda x: len(constraint_dict[x]),reverse=True)

    # going in order select at random and check if they conflict
    # retry if they do
    # This can be implemented better
    selected_pairs = []
    while(len(ordered_ids)>0):
        #first person is popped the front
        user1 = ordered_ids.pop(0)

        #get the second one by randomly selecting
        random_index = random.randint(0,len(ordered_ids)-1)
        print(random_index)
        print(ordered_ids)
        ### TODO make sure that the user hasn't been matched with everyone
        while(ordered_ids[random_index] in constraint_dict[user1]):
            random_index = random.randint(0,len(ordered_ids)-1)
        # after that while loop we have a sucessful index
        # we pop it so it is not reused
        user2 = ordered_ids.pop(random_index)

        log_connection(user1,user2,group_num)

        send_email(user1,user2,group_num)

        if(len(ordered_ids)==1):
            print("one left what do we do????")
            break

    print("we matched everyone")

        

    
    

    

    
    

def test(request):
    create_pairs(1)
    return HttpResponse("working yay")

