from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# insert / find / update / delete
# 저장
doc = {'name':'bobby','age':21}
db.users.insert_one(doc)

# 한 개 찾기
user = db.users.find_one({'name':'bobby'})

# 여러개 찾기
same_ages = list(db.users.find({'age':21},{'_id':False}))

# 바꾸기
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# 지우기
db.users.delete_one({'name':'bobby'})


# '_id' 값은 나타내지 않기 (같은 값이 있을 경우 하나만 가져온다.)
# 모든 내용을 가져오고 싶을 때는 중괄호를 비어두기
same_ages = list(db.users.find({},{'_id':False}))
for person in same_ages:
    print(person)

# update_one, update_many
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# delete_one, delete_many
db.users.delete_one({'name':'bobby'})