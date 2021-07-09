import datetime

import db.DBWork
import db.DBWork as bd
from db import DBWork
from db.DBHolder import DBHolder as holder
from models.dataclasses.Params import Params
from models.dataclasses.Person import Person
from models.dataclasses.Relation import Relation
from models.dataclasses.Req import Req
from models.dataclasses.User import User
from models.enums.Genre import Genre
from models.enums.Position import Position
from models.enums.UserType import UserType

bd.start_bd()

db.DBWork.delete_all_tables_values()

holder.add_user_type(UserType.plain_user.name)
holder.add_user_type(UserType.admin.name)

us1 = User(20, 'AF',  '07.07.2021 1:00','07.07.2021 1:11', UserType.plain_user.name)
us2 = User(10, 'THF', '06.07.2021 14:00','07.07.2021 16:16', UserType.plain_user.name)
holder.add_user(us1)
holder.add_user(us2)

R = Person(700, 'SAM', 'dafsgdfhasd')
K = Person(450, 'BEN', '1234567wsadf')
M = Person(100, 'LLL', 'dafsgdfhasd')
Z = Person(345, 'KKK', 'dafsgdfhasd')

holder.add_genre('мелодрама')
holder.add_genre('криминал')

holder.add_person(R)
holder.add_person(K)
holder.add_person(M)
holder.add_person(Z)

a = Params(R, 1990, 2015, ['мелодрама', 'криминал'], 1, 3, True, False, '9999', 1)
c = Params(K, 1990, 2015, ['мелодрама', 'криминал'], 3, 5, True, False, '9999', 1)
b = Params(M, 1990, 2015, ['мелодрама', 'криминал'], 1, 3, True, False, '9999', 1)
f = Params(Z, 1990, 2015, ['мелодрама', 'криминал'], 3, 5, True, False, '9999', 1)
part = Params(K, 1990, 2015, ['мелодрама', 'криминал'], 7, 5, True, False, '9999', 1)

holder.add_params(a)
holder.add_params(c)
holder.add_params(b)
holder.add_params(f)
holder.add_params(part)

holder.add_relation(Relation(R, K, 7, a))
holder.add_relation(Relation(M, Z, 8, c))
holder.add_relation(Relation(K, Z, 9, c))

holder.add_req(Req(20, a, '23122000'))
holder.add_req(Req(20, b, '12.12.46'))
holder.add_fav(Req(20, a, '23122000'))
holder.add_fav(Req(20, b, '12.12.46'))

holder.remove_fav(Req(20, a, '23122000'))
print(holder.has_params(Params(R, 1990, 2015, ['мелодрама', 'криминал'], 1, 3, True, False, '9999', 1)))
print(holder.is_part(part))
print(holder.get_min_threshold(a))

for p in holder.get_part(part):
    print(p.first)
    print(p.second)
    print(p.weight)
    print(p.params)
print(holder.show_reqs(us1))
print(holder.show_favs(us1))
print(holder.show_favs(us1))

DBWork.show_all_tables_values()
