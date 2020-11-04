import dbcreds
import mariadb


def getOption():
    print("Select your option")
    print("1) write a new post")
    print("2) See all posts")
    print("3) enter any other key to exit")
    option = input("Enter you option: ")
    return option

def showposts(conn,cursor):
    cursor.execute("SELECT * FROM blog_post")
    posts =cursor.fetchall()
    for post in posts:
        print("Username :" + post[0])
        print("Blog Content :" + post[1])
        print("------------------------------------------------------------------")
    return

def addPost(conn,cursor,user):
    blogContent = input("Enter the blog content: ")
    try:
        cursor.execute("INSERT INTO blog.blog_post(username, content, id)VALUES(?, ? , NULL)",[user,blogContent])
        conn.commit()
    except:
        print("Sorry, Something went wong")
    return 
    


print("Welcome to blog post console")
user = input("Enter your username: ")
password = input ("Enter your password: ")


try:
    conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
except mariadb.Error as e:
    print("Error connecting to MariaDB Platform: {e}")


cursor = conn.cursor()
#user table includes username, password and id and the username is unique. so query will return either 0 or 1 row   
cursor.execute("SELECT password FROM user WHERE user.username=?",[user])
temppass = cursor.fetchall()
if len(temppass)> 0:
    if password == temppass[0][0]:
        option = getOption()
        while option in ["1","2"]:
            if option == "1" :
                addPost(conn,cursor,user)
            elif option == "2":
                showposts(conn,cursor)
            option = getOption()
    else:
        print("the password is not correct")
else:
    print("the user name you entered doesn't exist") 



print("Thank you, goodbye")


cursor.close()
conn.close()

