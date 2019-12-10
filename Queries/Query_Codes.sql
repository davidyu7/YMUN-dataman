/* Lists */

    /* Delegations*/
SELECT Delegations.school_name, Advisors.name, Advisors.email, Delegations.delegate_count, Delegations.advisor_count FROM Delegations JOIN Advisors ON Delegations.school_name
= Advisors.school WHERE Advisors.point_of_contact = '1';

    /* Committees */
SELECT Committees.organ, Committees.comms_name, Committees.size, Staffers.name, Staffers.phone_number FROM Committees JOIN Staffers ON Committees.comms_name =
Staffers.committee WHERE Staffers.head_chair = '1';

    /* Schedule */
SELECT comms_name, day1, day2, day3, day4 FROM Committees;

    /* Rooming - Only works when all rooms are entered into the table */
SELECT Rooming.building, Rooming.room_id, (SELECT Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day1 ORDER BY
Rooming.building), (SELECT Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day2 ORDER BY Rooming.building), (SELECT
Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day3 ORDER BY Rooming.building), (SELECT Committees.comms_name FROM
Rooming JOIN Committees ON Rooming.room_id = Committees.day4 ORDER BY Rooming.building) FROM Rooming ORDER BY building;

/* SELECT Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day2 ORDER BY Rooming.building;
SELECT Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day3 ORDER BY Rooming.building;
SELECT Committees.comms_name FROM Rooming JOIN Committees ON Rooming.room_id = Committees.day4 ORDER BY Rooming.building;

Alternative, if the above does not work once the table is full */

/* Dropdown Searches */

    /* Committees */
SELECT Delegates.position_name, Delegates.name, Delegates.school FROM Delegates WHERE committee.name =

    /* Buildings */

    /* Delegations */

/* Search for person by name */
    /* gives all information for any term you input that is in the system */