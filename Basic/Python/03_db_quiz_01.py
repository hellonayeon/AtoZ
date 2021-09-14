from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 매트릭스 평점 가져오기
matrix_star = db.movies.find_one({'title':'매트릭스'})['star']
print(matrix_star)

# 매트릭스 평정과 같은 평점의 영화 제목들 가져오기
same_movies = list(db.movies.find({'star': matrix_star}))
for movie in same_movies:
    if movie['star'] == matrix_star:
        print(movie['title'])

# 매트릭스 영화 평점을 0점으로 만들기
# 자료형 통일하기
db.movies.update_one({'title':'매트릭스'}, {'$set': {'star':'0'}})