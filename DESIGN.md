Flask

We used Python, HTML, and CSS for our website, Roomies. Flask, a Python library, is a web framework allowing us to utilize the Jinja template in our HTML code and create a working website. The underlying code is organized under the Flask conventions with the following main components:
templates/, app.py, static/, and requirements.txt.

“templates/” is a folder with the HTML files that create our website pages. “app.py” is a Python file where functions are defined for our web server, including login.html, quiz.html, match.html, and register.html. “static/” is a folder with our CSS file and images used in the website. The CSS file supplements the styling components with specified background color, font size, etc for various tags and HTML classes. We wanted to customize the design of our page so we included a CSS file. The “requirements.txt” document notes the libraries that are required in our application. 

We chose to use Flask because of our own familiarity with Flask after completing Problem Set 9 in the CS50 course. We also think that the structure with Flask is suitable for our website which includes forms and storing information in a database. Python allows us to access an SQL database and Flask enables us to interact with the server side of our website, as the methods in app.py can lead to different actions depending on whether the request is GET or POST. 

Login page

The first page that the user is shown when entering our site is the login page. The user getting directed to the login page occurs because the app.py file has home() defined under @app.route("/"). We designed the login page to come first so that the user is properly logged in before we make attempts to save information in a database. We want to make sure that the user’s profile is saved alongside specification of who the user is so that during data retrieval from the SQL database later, we can easily identify which information corresponds to each user. 

The function home() renders the template “login.html.” In the “login.html,” there is a form with two text field components: the username and password. In app.py, we have a login() function under @app.route("/login", methods=["GET", "POST"]). When a user submits a form, a POST request is sent. We have a series of if conditionals to ensure that the user submitted values for each text field. Then we check that the password corresponding to the username in our SQL database matches with the password that the user inputted. We update the session["user_id"] variable to keep track of the current user, allowing us to then use session["user_id"] in other methods as well. When the user sends a GET request, we want to render the login.html page.

Register page
Similar to login, the register page is created with an html page, register.html, and a method in app.py. In register(), we check that the username has not been used before. We want the usernames to be unique so that we can use the username to identify each user. If two people had the same username, we may accidentally pull the wrong data from the database. We also check that the password confirmation worked correctly. Then we have a database execute call to insert the data into our users table in SQL. We are creating a row in the table for each user/

Index page

After the user logs in, we didn’t want to send the user directly to the quiz page. If the user already took a quiz, there would be no reason for them to fill out the quiz again. So, we decided to create an index page where the user can see a button to go to the quiz and a button to see their matches. This general landing page gives the user a clearer idea of how to use Roomies. In our index.html page, we include an image to add aesthetics, and we also include alternative text in case a website has difficulty loading the image, the user would still understand what was supposed to be there. The source of the image is "../static/roomiesremovebg.png" because we put our image in the static folder.

Quiz page

Our quiz.html page consists of a form. We used radio input buttons to showcase multiple choice answers to each question. The information we collect for each user is their: name, gender, year, personality type (introvert, extrovert, or ambivert), and sleep habit (night owl or early bird). We chose the information based on what is important for compatibility between roommates. Someone who wakes up very early would likely dislike living with roommates who stay up very late. Instead of having text fields, we decided to have multiple choice answers so that we can easily retrieve the user’s answers in the backend.

In the quiz() method, there is a series of request.form.get() calls which takes in the user’s form responses. We store the value in variables so that there is readability in our code when we later use the values in our SQL query. Our SQL query uses “UPDATE users SET” instead of “INSERT” because the row for a current user already exists. In the database, a row was created with the user’s username and password. We want to modify the row to include the new values from the form. 

Match page

Let’s delve into the match() method in app.py. The SQL call “SELECT COUNT(username) FROM users" will return a list with the count for the number of rows in the username column. To retrieve the actual number, we must index into the first value of the list and then get the value corresponding to the key “COUNT(username)”. Thus, the numOfUsers variable is populated with db.execute("SELECT COUNT(username) FROM users")[0]['COUNT(username)']. The variable currentUser stores the row of the SQL database that corresponds to the user who is logged in. 

We have a for loop going through all the rows in the SQL database. Each row corresponds to one user. We want to check how compatible each user is with the current user. Therefore, we compare the quiz answers and keep track of the number of same selections. Whichever user has the most number of the same answers as our current user is the best roommate for our current user. Since we kept track of numOfUsers, we can use range(numOfUsers) in our Python for loop to iterate through the rows of the SQL table. We check selectedUser[0]["ID"] != currentUser[0]["ID"] so that the user’s row is not being compared to itself. There would always be a perfect match between a row and itself, and then the best roommate would be the user him/herself which would not be a helpful output. 

The variable maxMatches keeps track of the largest number of matches a user has had with our current user. We update maxMatches when a value in sameAnswers is greater than the value in maxMatches. Our match page is then rendered with match.html. We display not only the name, but the entire profile of the match, because having information about their match would be helpful to the roommate. In app.py, we specify values for matchName, matchGender, matchYear, matchPers, matchSleep in the match() return statement. Then, in the HTML page we can call on the values with Jinja syntax that looks like: {{matchName}}.

Navigation bar

We coded a navigation bar in layout.html. There is an <a> tag with the text “Home” that shows up on the top left of the navigation bar on all pages. We wanted the user to be able to directly get to the starting login in page at any point of navigation. Since all other HTML pages extend layout.html, the navigation bar shows up in all pages. When the user is not logged in, there are also buttons to the registration and login pages. When the user is logged in, there is a button to log out.
