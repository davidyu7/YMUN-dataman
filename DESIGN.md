

Document Structure:


1. Heroku Website Implementation

While the IDE runs the program on a Cloud platform provided by the IDE, running the program on Heroku will allow us to run the program on an
external computer or system/platform that will allow us to be able to access the website, even when no one is logged into the IDE. Having our
program on Heroku allows the website to run independently without having the code open in any space. Heroku is our chosen hosting platform through
which we will be able to access our website in order to actively use it.
In order to implement Heroku, we needed to make some slight changes to our code, one of which was to change the database identifier, from a
database file (containied in IDE folder) to a postgres database hosted on Heroku. Since the dialect of the query language is different between
Postgres and CS50 IDE's implementation of SQL, we needed to change our queries to account for postgres' case sensitivity.
We did this by converting both input queries and target values to lowercase.

We also felt that we needed a distinctive domain name, making it clear that we owned and created the application for YMUN's use. We thus connected
the Heroku web application to data.ymun.org, a subdomain under a domain that we already owned - ymun.org.


2. Search Bar

The search engine has the main goal of speeding up the user's access to important information. Instead of going to the Committees page or the
Delegations page and browsing through the entirety of those tables, the user now only needs to input a single query in one location. This is
particularly useful if the user wants to find pertinent information for a specific delegate, since it would be unfeasible to look through the
table of all 1,800 delegates. The search bar has two main features: a "Search All" function and a specific search-by-category function. The
"Search All" function can be accessed by typing a query and pressing the "Search All" button, or by simply hitting the enter key. This works by
generating a SQL query for each of the 5 categories that it is possible to search through. The results from these queries are then rendered in a
template, which displays the results from each category in a separate table. Returning to the search bar, one can narrow down their search to a
specific category by clicking the drop down menu adjacent to the "Search All" button. By doing so, only the SQL query that searches in the specified
category will be run, and only one table of results will be displayed.

3. Data Displays and Table Generation

The primary recurring functionality of our application is the display of SQL query information into a formatted HTML table. We accomplish this by
using dictionaries - any time there is a table displayed on any page of our application, you can be sure that there is a dictionary containing those
values. These dictionaries are populated by the relevant SQL requests, and then iterated through in the Jinja templates to return a formatted table.
One important feature that goes beyond the standard display of SQL query results is the creation of customized links that enable the user to easily
jump between tables. For example, in the committees view, each committee name table value is a link that, when clicked, opens a page that displays
details for that specific committee. This is accomplished by using HTTP GET request parameters. When iterating through the values of each row, the
committee/delegation ID is plugged into a custom link as a request parameter using the "?" notation. This is then used by the Flask application to
populate the details page with information about the specified item. This feature can occur recursively, so that each details page can also contain
more tables that are linked to other details page.


4. Attendance

Attendance is a feature that will display the delegates at the conference that are marked as "absent" on the attendance sheet of every committee.
On the attendance page, the names of absent delegates will appear, along with information about their advisors and supervisors, and their phone
numbers. This feature reads in data from each of the 39 committee attendance sheets (that are downloaded once attendance is taken in each
committee, at the end of every committee session), and uploads the names of students that are marked as absent from each committee file in the
database, based on which committee session is being considered.
Once the absense has been taken care of, the student can be marked as present, and the database can be updated to reflect new present and absent
students.




Next Steps for Design and Implementation:

1. Login and Email Protection System

Our first priority for continuing the project would be including a login and email protection system, so that only members of the YMUN team
with login emails under the YMUN domain name would be able to access the website. This way, access to the data presented at the link is
restricted, and the contents of the website are protected. While creating the current version of the website, we created a beta version of this,
but because we decided to focus on implementing other features first, we placed that project on hold, for now.


2. Add an edit function to all Data

In the future, we would also like to implement an edit function that would allow us to edit the information on the website for all users.
Having the framework to edit and update the backend database will open up the possibility of conducting registration on the same platform,
where advisors and delegates would be able to submit information directly to the database, skipping the middle step of collecting information
in excel sheets before importing them into the database.
However, this was not our main priority as we have already finalized all of the information that we will import into the database.
We decided that it should simply be something to implement in the future, as we continue to develop the website.
