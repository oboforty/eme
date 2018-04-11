import bcrypt


password = "super secret password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())




hash2 = hashed.decode('utf-8')
if bcrypt.checkpw(password.encode('utf-8'), hash2.encode('utf-8')):
    print("It Matches!")
else:
    print("It Does not Match :(")
