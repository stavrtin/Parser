currentEmployee = {'one': 'Инокент', 2: "Саша", 3: "Андрей"}
formerEmployee = 'Марина-Алина'


# def merge_dicts(dictOne, dictTwo):
#     dictThree = dictOne.copy()
#     dictThree.update(dictTwo)
#     return dictThree


# print(merge_dicts(currentEmployee, formerEmployee))
dic3 = { **{'_id': formerEmployee}, **currentEmployee}

print(dic3)