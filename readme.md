Taken older project of Customer resource management platform.

changes made accounts app :

1. changes made on models.py 
 ---- added django User model with Customer.
 ---- new profile_pic field.
 ---- made email unique for find match between customer and user.

2. changes made templates :
 --- customer profile to User profile.
 --- different dashboard user and admin.
 --- customer get deleted as user.

3. fixed Dark/light mode.

********* important thing to add *********

1. db.sqlite3 is need for re-run as it contains user auth files.
2. didn't staged static/images and this will throw error as models have default pic mentioned in it.
3. there is loophole in customer create.

========= That's it =========