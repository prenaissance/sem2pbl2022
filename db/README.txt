The database runs on localhost, but MongoDB stores
and allows literally all the data from the table to
be transferred in .json format, which I am attaching
in one of the folders.

If you have a MongoDB server and client on your machine,
you can even do the .json reading yourself. Only for this
you will need to change the URL of the database server
inside the code, and drop the .py files and .json into one
folder. Next, we just run main.py to update posts by category
(at least that's how it should work in theory).