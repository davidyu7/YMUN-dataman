

Document Structure:


1. Heroku Website Implementation

While the IDE runs the program on a Cloud platform provided by the IDE, running the program on Heroku will allow us to run the program on an
external computer or system/platform that will allow us to be able to access the website, even when no one is logged into the IDE. Having our
program on Heroku allows the website to run independently without having the code open in any space. Heroku is our chosen hosting platform through
which we will be able to access our website in order to actively use it.
In order to implement Heroku, we needed to make some slight changes to our code, one of which was to change the database identifier, from a
database file (containied in IDE folder) to a postgres database hosted on Heroku. Since the dialect of the query language is different between
postgres and CS50 IDE's implementation of SQL, we needed to change our queries to account for postgres' case sensitivity.
We did this by converting both input queres and target values to lowercase.

We also felt that we needed a distinctive domain name, making it clear that we owned and created the application for YMUN's use. We thus connected
the Karoku web application to data.ymun.org, a subdomain under a domain that we already owned.


2. Search Bar

The search engine has the main goal of speeding up the user's access to important information.



3. Data Displays and Table Generating




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
but because we decided to focus on implementing other features first, and to implement this a little later.


2. Add an edit function to all Data

In the future, we would also like to implement an edit function that would allow us to edit the information on the website for all users.
However, this was not our main priority, and we decided that it should simply be something to implement in the future, as we continue to develop
the website.


