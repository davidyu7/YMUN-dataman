Users's Guide to YMUN Data Management Project



The YMUN Registration and Data Management Platform is a website and applicatioin created by David Yu, Emily Mayo, and Claire Calkins in CS50, as a
practical program to be used during the Yale Model United Nations Conference, a MUN conference that attracts and hosts about 200 high school
teachers and students every year. This application/website will serve as a data management and organization system for that conference.


Structure of the README.md file:

1. Project Background and Motivation
2. Data and Data Structure Information
3. Project Features and Website Design
4. Final Remarks



1. Background:

As stated in the Introduction, this website has the goal of serving as a data management tool for the Yale Model United Nations conference, a MUN
conference that takes place in January every year, at Yale. Historically, the YMUN team has used google sheets (or excel sheets) to manage and
keep track of necessary data. However, this system has proven to often be unorganized, subject to human error, and difficult to use. During the
conference, the team usually has one excel sheet to track each of the 39 committees at the conference, one excel sheet to track registration
and advisor information, another excel sheet to track room locations for each committee for each of the four days of the conference, etc. Creating
a website for integrated data management of the information previously located in many different places will allow for optimization of efficiency
during the conference, allowing us to keep better track of our data, and allowing for easier access and use of essential information for the YMUN
team.



2. Data and Data Structure Information:

Our website has four main data structures, all linked together through embedded links. There are 5 different pages that present a table with
either completely different information, or information that is restructured in a different manner. To find specific iniformation within the data
tables on the website, you can either click on the page that applies the most, or use the search bar function (to be specified in the "features"
section of the user's guide).

*** add in rooms and attendance here8 ***

    a. Data Source
    The website is based on data that is uploaded through CSV reading. All CSVs are derived and uploaded from Google Sheets as they are filled
    out. Once more information is recieved, more can thus easily be read into the website through CSV upload both in the IDE and on the Heroku
    website creator that we are using.

    b. Data Privacy
    All data on the website is to only be used by the YMUN Secretariat members. The website contains confidential information about both teachers
    and students in high school, and volunteer students at Yale. The website is created for the sole purpose of data organization and management,
    and not for data sharing and access purposes.

    c. Data Structure
    The data loaded into the website has been divided into four main categories: delegation, committee, room, and attendance. Each page on the
    website presents data structured around the specific criteria listed in the title, and links to more specific information about any given
    item in the table. For example, the "Delegations" page gives a table with a list of all the delegations attending the conference. However,
    you can click on the name of nay delegation and recieve information on that specific delegation (including advisors, contact information,
    student names, etc.).



3. Project Features and Website Design


    a. Search Bar
    The homepage presents one of our main features, a search bar that allows you to type in information, and search by room, delegation,
    committee, delegate, or advisor. That way, you can type any information that you would like to find, and search through the type of result
    you would like. For example, you can serach for "the" by delegation, and recieve information about every delegation if their title contains
    the characters "the" in it. Through the search bar, you can immiediately find any information that you are searching for, so long as it is
    contained in the website.

    b. Website Design
    The website is designed so that all information is easily accessible to the user. The only users of the website will be YMUN Secretariat
    members who know the vocabulary used on the website, and thus, use of the website should be straitforward, and the information presented will
    be very accessible to those users, and no training should be required.



    c. Attendance
    The attendance tab on the website has the goal of listing out all delegates that have been listed as "absent" for any committee session during
    the conference. When delegates are missing, the Secretariat is required to call their advisor to let them know. Listing out absent delegates
    will allow the Secreatriat to save time and more easily have access to phone numbers and email addresses, which will speed up this process
    after attendance in each committee is taken. At the moment that the website is being submitted for the CS50 project, no data will appear in the
    attendance sheet, because attendance will only be actually taken when the conference takes place in January 2020.



4. Final Remarks







