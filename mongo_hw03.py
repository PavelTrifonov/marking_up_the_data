from pymongo import MongoClient
import json
from pprint import pprint

# создание экземпляра клиента
client = MongoClient('localhost', 27017)
# подключение к базе данных и коллекции
db = client['library']
collection = db['books']
# Чтение файла JSON
with open('library.json', 'r') as file:
    data = json.load(file)
# Вставка фрагмента в коллекцию MongoDB,
# для этого изменим формат словаря и сделаем запись в коллекцию
# каждой книги как отдельного объекта
count = 0
info_list = list(data.keys())
print(len(data[info_list[0]]))
while True:
    if count < len(data[info_list[0]]):
        book_dict = {}
        for i in info_list:
            book_dict[i] = (data[i][str(count)])
        collection.insert_one(book_dict)
        count += 1
    else:
        print("запись закончена")
        break

# вывод первой записи в коллекции
all_docs = collection.find()

first_doc = all_docs[0]
print(first_doc)

# фильтрация документов по критериям
query = {"presence": 'In stock'}
print(f"Количество книг со статусом в наличии:\
      {collection.count_documents(query)}")

# Использование проекции
query = {'rating': 5}
projection = {'titles': 1, 'links': 1, "_id": 0}
proj_docs = collection.find(query, projection)
for doc in proj_docs:
    pprint(doc)

# Использование оператора $lt и $gte
query = {'rating': {"$lt": 2}}
print(f"Количество книг с рейтингом меньше 2:\
    {collection.count_documents(query)}")
query = {'rating': {"$gte": 4}}
print(f"Количество книг с рейтингом больше или равно 4:\
    {collection.count_documents(query)}")

# Использование оператора $regex
# $options установлен в "i", что означает регистронезависимый поиск
query = {'titles': {"$regex": "[T,t]he", "$options": "i"}}
print(f"Количество документов, содержащих 'The':\
    {collection.count_documents(query)}")

# Использование оператора $in
query = {"rating": {"$in": [2, 4]}}
print(f"Количество книг с оценкой 2 и 4: {collection.count_documents(query)}")

# Использование оператора $ne
query = {"presence": {"$ne": "In stock"}}
print(f"Количество книг не в наличие: {collection.count_documents(query)}")
