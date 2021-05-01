def a():
    global by
    by = 1+3

a()
print (by)





# from navycut.datastructures import NCObject

# data = {"na me": "John Smith","title":"engineer", "id":1, "hometown": {"city": "New York", "id": 123}}
# a = NCObject(data)

# # print (a.name)
# print('aniket')

# print (a.title)
# a.hometown.update(city="kolkata")
# print (a.hometown.city)
# # print (a.id)
# # a.update({'id':3})
# # print (a.hometown.__dict__)
# # a.update({'hometown':{"city": "Kolkata", "id":2}})
# # # a.hometown.update('city', 'Kolkata')
# # print (a.hometown)
# # print (a.id)
# # print (a.hometown.__dict__)
# print (a.to_dict())
# # print (dir(a))

# # print (a.get("na me"))

# # a.an = "name"

# # print (a.__dict__)

# # from types import SimpleNamespace
# # from json import loads, dumps
# # sn_obj = loads(data, object_hook=lambda d: SimpleNamespace(**d))
# # print (sn_obj.hometown)












# # import json


# # data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

# # # Parse JSON into an object with attributes corresponding to dict keys.
# # x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# # print(x.name, x.hometown.name, x.hometown.id)

# # x.name = "Aniket"

# # print (x.name)