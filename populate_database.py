from faker import Faker
import random
from datetime import date, datetime, timedelta
from pymongo import MongoClient

Faker.seed(1234) # set seed for reproducibility

faker = Faker() # create Faker object

# variables that determine the data in the collections
n_users = 10 # set number of users
n_transactions = 300 # set number of transactions
n_days = 7 # set the number of days transfers should date back to

# values for creating user data for account type, class and status respectively
a_types = ['current', 'savings']
a_classes = ['corporate', 'personal']
a_stats = ['active', 'dormant', 'frozen']

# populate users dict with fake data

# the code below creates a dictionary where each key is a field and the value is all the elements of that field
# this structure was perfect for a pandas dataframe, but we are not swinging that way anymore

# create users dict
# users = {'account_number':[],
#          'account_name':[],
#          'account_date':[],
#          'account_type':[],
#          'account_class':[],
#          'dob':[],
#          'customer_id':[],
#          'bvn':[],
#          'account_balance':[],
#          'account_status':[]}

# for i in range(n_users):
#     users['account_number'].append(faker.random_int(1000000000,9999999999))
#     users['account_name'].append(faker.name())
#     users['account_date'].append(faker.date_object())
#     users['account_type'].append(a_types[random.randint(0,1)])
#     users['account_class'].append(a_classes[random.randint(0,1)])
#     users['dob'].append(faker.date_of_birth(minimum_age=18, maximum_age=97))
#     users['customer_id'].append(faker.md5())
#     users['bvn'].append(faker.random_int(10000000000,99999999999)) # generate 11 digits
#     users['account_balance'].append(faker.random_int(10,9999999))
#     users['account_status'].append(a_stats[random.randint(0,2)]) #switch btw 3 statuses


users = [] # store users
id_list = [] # store the list of valid id's

# populate users list
for i in range(n_users):
    user_id = faker.md5() # create an id for this user
    id_list.append(user_id) # add the id to list for use later in generating sender/recipient id

    users.append({ 
        '_id':user_id, # set the value to the id generated earlier
        'account_number':faker.random_int(1000000000,9999999999),
        'account_name':faker.name(),
        'account_date':datetime.strftime(faker.date_object(), '%Y-%m-%d'),
        'account_type':a_types[random.randint(0,1)], # switch between the 3 types
        'account_class':a_classes[random.randint(0,1)], # switch btw 3 classes
        'dob':datetime.strftime(faker.date_of_birth(minimum_age=18, maximum_age=97), '%Y-%m-%d'),
        'bvn':faker.random_int(10000000000,99999999999), # generate 11 digits
        'account_balance':faker.random_int(10,9999999),
        'account_status':a_stats[random.randint(0,2)] # switch between the 3 statuses
    })

print(str(n_users) + ' user(s) added!')
print('First five users: ')
for i in users[:5]:
    print(i, '\n')


#calculate start date for transfers
start_date = date.today() - timedelta(days=n_days) 

transactions = [] # store the transactions between calculated date and current date

for i in range(n_transactions):
    transactions.append({
        '_id':faker.md5(), # create an id for this transaction
        'transaction_date':datetime.strftime(faker.date_between(start_date), '%Y-%m-%d'),
        'sender_id':id_list[random.randint(0, n_users-1)],
        'recipient_id':id_list[random.randint(0, n_users-1)], # fix this to exclude sender
        'amount':random.randint(50,500000), 
        'current_balance':random.randint(100,999999),
        'narration':faker.sentence(), 
    })
print(str(n_transactions) + ' transaction(s) added!')
print('First five transactions: ')
for i in transactions[:5]:
    print(i, '\n') 

# for i in range(300):
#     transactions['date'].append(faker.date_between(start_date))
#     transactions['sender_id'].append(id_list[random.randint(0, n_users-1)])
#     transfers['recipient_id'].append(id_list[random.randint(0, n_users-1)]) # fix this later
#     transfers['amount'].append(random.randint(50,500000))
#     transfers['current_balance'].append(random.randint(100,999999))
#     transfers['narration'].append(faker.sentence())
#     transfers['transaction_id'].append(faker.md5())

#create connection to mongodb
client = MongoClient('localhost', 27017)
db = client['Accountapi'] # use 'Accountapi' database


users_col = db['users'] # create collection 'users'
users_col.insert_many(users) # dump users dictionary into db as collection
print(users_col.inserted_ids)

trans_col = db['transfers'] #create collection 'transactions'
trans_col.insert_many(transactions) # dump transactions dictionary into db as collection

list_of_db = client.list_database_names() # print databases
print(list_of_db)