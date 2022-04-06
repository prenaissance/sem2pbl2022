run npm install in the folder "app" to install dependencies
the project is set up for server-side modular rendering of webpages,
which can be used with res.render in the router.

If that feature is not needed delete the views folder and use
res.sendFile() with the html file instead.

js and css from the public folder will be served to the client
stuff in app.js probably needs no editing, default file form template