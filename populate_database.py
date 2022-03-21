from faker import Faker
import random
from datetime import date, timedelta
from pymongo import MongoClient

Faker.seed(1234) # set seed for reproducibility

faker = Faker() # create Faker object

# create users dict
users = {'account_number':[],
         'account_name':[],
         'account_date':[],
         'account_type':[],
         'account_class':[],
         'dob':[],
         'customer_id':[],
         'bvn':[],
         'account_balance':[],
         'account_status':[]}

# variables that determine the data in the collections
number_of_users = 10 # set number of users
number_of_transfers = 300 # set number of transfers
number_of_days = 7 # set the number of days transfers should date back to

# values for creating user data for account type, class and status respectively
a_types = ['current', 'savings']
a_classes = ['corporate', 'personal']
a_stats = ['active', 'dormant', 'frozen']

# populate users dict with fake data
for i in range(number_of_users):
    users['account_number'].append(faker.random_int(1000000000,9999999999))
    users['account_name'].append(faker.name())
    users['account_date'].append(faker.date_object())
    users['account_type'].append(a_types[random.randint(0,1)])
    users['account_class'].append(a_classes[random.randint(0,1)])
    users['dob'].append(faker.date_of_birth(minimum_age=18, maximum_age=97))
    users['customer_id'].append(faker.md5())
    users['bvn'].append(faker.random_int(10000000000,99999999999)) # generate 11 digits
    users['account_balance'].append(faker.random_int(10,9999999))
    users['account_status'].append(a_stats[random.randint(0,2)]) #switch btw 3 statuses
print(number_of_users + ' user(s) added!')

customer_id = users['customer_id'].values # create a list of valid id's

transfers = {
    'date': [],
    'sender_id':[],
    'recipient_id':[],
    'amount':[],
    'current_balance':[],
    'narration':[]
}

#calculate start date for transfers
start_date = date.today() - timedelta(days=number_of_days) 

for i in range(300):
    transfers['date'].append(faker.date_between(start_date))
    transfers['sender_id'].append(customer_id[random.randint(0, number_of_users-1)])
    transfers['recipient_id'].append(customer_id[random.randint(0, number_of_users-1)]) # fix this later
    transfers['amount'].append(random.randint(50,500000))
    transfers['current_balance'].append(random.randint(100,999999))
    transfers['narration'].append(faker.sentence())

#create connection to mongodb
client = MongoClient('localhost', 27017)
db = client['Accountapi'] # use 'Accountapi' database
users_col = db['users'] # create collection 'users'
users_col.insert(users) # dump users dictionary into db as collection

trans_col = db['transfers'] #create collection 'transfers'
trans_col.insert(transfers) # dump transfers dictionary into db as collection