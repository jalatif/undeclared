__author__ = 'abhinav'

from sets import Set
from pprint import pprint
from copy import copy

N = "N"
H = "H"

def make_need_requirements(book_world):
    dsy = {N : {}, H : {}}
    for user in book_world.keys():
        for book in book_world[user][N]:
            if book not in dsy[N].keys():
                dsy[N][book] = [user]
            else:
                if user not in dsy[N][book]:
                    dsy[N][book].append(user)
                else:
                    pass
        for book in book_world[user][H]:
            if book not in dsy[H].keys():
                dsy[H][book] = [user]
            else:
                if user not in dsy[H][book]:
                    dsy[H][book].append(user)
                else:
                    pass
    return dsy

def make_graph(table_hash):
    book_graph = {}
    for trans in table_hash.keys():
        h_user = trans[0]
        n_user = trans[1]
        book = trans[2]
        if h_user in book_graph:
            if "H" in book_graph[h_user]:
                book_graph[h_user]["H"].append(book)
            else:
                book_graph[h_user]["H"] = [book]
        else:
            book_graph[h_user] = {"H": [book], "N" : []}

        if n_user in book_graph:
            if "N" in book_graph[n_user]:
                book_graph[n_user]["N"].append(book)
            else:
                book_graph[n_user]["N"] = [book]
        else:
            book_graph[n_user] = {"N": [book], "H" : []}

    return book_graph

book_world = {
    "U1" : { N : ["B3"], H : ["B1", "B2"]},
    "U2" : { N : ["B1"], H : ["B3", "B4"]},
    "U3" : { N : ["B4"], H : ["B3"]},
    "U4" : { N : ["B2"], H : ["B5"]},
    "U5" : { N : ["B1"], H : ["B6"]},
}

book_world1 = {
    "U1" : { H : ["B1"], N : ["B2"]},
    "U2" : { H : ["B2"], N : ["B1"]},
}

book_world2 = {
    "U1" : { H : ["B1"], N : ["B3"]},
    "U2" : { H : ["B2"], N : ["B1"]},
    "U3" : { H : ["B3"], N : ["B2"]},
}

book_world3 = {
    "U1" : { H : ["B1", "B2"], N : ["B4"]},
    "U2" : { H : ["B3"], N : ["B1"]},
    "U3" : { H : ["B4"], N : ["B3"]},
    "U4" : { H : [], N : ["B2"]},
}

trans1 = {
    ('U1', 'U2', 'B1') : 1,
    ('U2', 'U1', 'B2') : 2,
}

trans2 = {
    ('U1', 'U2', 'B1') : 1,
    ('U2', 'U3', 'B2') : 2,
    ('U3', 'U1', 'B3') : 3,
}

trans3 = {
    ('U1', 'U2', 'B1') : 1,
    ('U1', 'U4', 'B2') : 2,
    ('U2', 'U3', 'B3') : 3,
    ('U3', 'U1', 'B4') : 4,
}

trans4 = {
    ('U1', 'U2', 'B1') : 1,
    ('U2', 'U3', 'B2') : 2,
    ('U1', 'U5', 'B5') : 3,
    ('U3', 'U5', 'B6') : 4,
    ('U5', 'U6', 'B7') : 5,
    ('U3', 'U1', 'B3') : 6,
}

trans5 = {
    ('U1', 'U2', 'B1') : 1,
    ('U2', 'U3', 'B2') : 2,
    ('U1', 'U5', 'B5') : 3,
    ('U3', 'U7', 'B6') : 4,
    ('U5', 'U6', 'B7') : 5,
    ('U3', 'U1', 'B3') : 6,
    ('U6', 'U1', 'B8') : 7,
}

trans = {
    ('U1', 'U2', 'B1') : 1,
    ('U2', 'U3', 'B2') : 2,
    ('U1', 'U5', 'B5') : 3,
    ('U3', 'U5', 'B6') : 4,
    ('U5', 'U6', 'B7') : 5,
    ('U3', 'U1', 'B3') : 6,
    ('U6', 'U1', 'B8') : 7,
}

trans7 = {
    ('U3', 'U1', 'B3') : 1,
    ('U2', 'U1', 'B3') : 2,
    ('U1', 'U2', 'B1') : 3,
    ('U2', 'U3', 'B4') : 4,
    ('U1', 'U4', 'B2') : 5,
    ('U1', 'U5', 'B1') : 6
}

book_world = make_graph(trans)

dsy = make_need_requirements(book_world)

def contains (l1, l2):
    match = 0
    for elem in l1:
        if l2[match] == elem:
            match += 1
            if match == len(l2):
                return True
        else:
            if match != 0:
                match = 0
    return match == len(l2)

def check_transaction():
    global dsy
    global trans
    gtrans = []
    rtrans = [[]]
    for book in dsy[N].keys():
        if book:
            result = meet_nsy(book, Set(), Set(), [], [])
            if result not in gtrans and result != []:
                gtrans.append(result)
                for tras in result:
                    #print tras
                    if tras == ['-', '-', '-']:
                        #print rtrans
                        for rid in range(0, len(rtrans) - 1):
                            rtr = rtrans[rid]
                            if contains(rtr * 2, rtrans[-1]):
                                rtrans.pop()
                                break
                        rtrans.append([])
                        continue
                    if tras[-1] == 'done':
                        tras = tras[:-1]
                    rs = tuple(tras)
                    if rs in trans and trans[rs] not in rtrans[-1]:
                        rtrans[-1].append(trans[rs])
    return rtrans[:-1], gtrans

def meet_nsy(book, used_books, used_users, transactions, guser):
    global dsy
    global book_world
    if guser != []:
        need_users = guser
    else:
        need_users = dsy[N][book]
    for n_user in need_users:
        used_books |= Set(book_world[n_user][H])
        if n_user in used_users:
            return transactions
        used_users.add(n_user)
        if book not in dsy[H].keys():
            transactions = [None]
            return transactions
        else:
            have_users = dsy[H][book]
        for h_user in have_users:
            mbook = Set(book_world[h_user][N]) & used_books
            if bool(mbook):
                for bk in mbook:
                    if transactions == [] and len(used_users) == 1:
                        #transactions.append([n_user, '<-', h_user, 'done'])
                        transactions.append([h_user, n_user, book])
                        transactions.append([n_user, h_user, bk])
                        transactions.append(['-','-','-'])
                        return transactions
                    for ti in range(0, len(transactions)):
                        transaction = transactions[ti]
                        #print transaction[1]
                        if bool(Set([transaction[1]]) & Set(dsy[H][bk])):
                        #if transactions != [] and bool(Set([transactions[0][0]]) & Set(dsy[H][book])):
                            if bk in used_books:
                                used_books.remove(bk)
                            if book in used_books:
                                used_books.remove(book)
                            #transactions.append([n_user, '<-', h_user, 'done'])
                            transactions.append([h_user, n_user, book])
                            transactions.append([transaction[1], h_user, bk, 'done'])
                            return transactions[ti:]
                        else:
                            continue
            for bk in book_world[h_user][N]:
                if book in used_books:
                    used_books.remove(book)
                trs = transactions[:]
                ubs = copy(used_books)
                usu = copy(used_users)
                #transactions.append([n_user, '<-', h_user])
                transactions.append([h_user, n_user, book])
                transactions = meet_nsy(bk, used_books, used_users, transactions, [h_user])
                try:
                    if transactions[-1][-1] == "done":
                        transactions.append(['-','-','-'])
                        used_books = ubs
                        used_users = usu
                    else:
                        transactions = trs
                        used_books = ubs
                        used_users = usu
                except:
                    pass
    return transactions


print book_world
print make_need_requirements(book_world)
pprint(check_transaction())
