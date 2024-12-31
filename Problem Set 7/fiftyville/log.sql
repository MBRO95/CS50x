-- Keep a log of any SQL queries you execute as you solve the mystery.
-- List the tables of the database
.tables
-- List the schema of each database table
.schema airports
.schema crime_scene_reports
.schema people
.schema atm_transactions
.schema flights
.schema phone_calls
.schema bakery_security_logs
.schema interviews
.schema bank_accounts
.schema passengers
-- Identify crime scene report id(s)
select id from crime_scene_reports where day = 28 AND month = 07 AND year = 2023 AND street = "Humphrey Street";
-- Got back two results: ID 295 and ID 297
-- Get description of ID 295
select description from crime_scene_reports where id = 295;
-- "Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery."
-- Get description of ID 297
select description from crime_scene_reports where id = 297;
-- "Littering took place at 16:36. No known witnesses."
-- Disregarding ID 297 and focusing on ID 295, which mentions the bakery and the time of 10:15 AM
-- Investigate the witness accounts further
select transcript from interviews where year = 2023 and month = 07 and day = 28;
-- Within ten minutes of the theft, the car left
-- Thief was seen earlier that morning withdrawing from the ATM on Leggett
-- Planning to take the earliest flight out of Fiftyville on 07/29
-- Person on the other end of the phone with thief purchased the flight ticket; call was less than one minute; thief was the caller

-- Search ATM transactions
select * from atm_transactions where atm_location like "Leggett%" and transaction_type = "withdraw" and year = 2023 and month = 07 and day = 28;
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
-- | 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
-- | 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
-- | 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
-- | 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
-- | 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+

-- ID people from bank accounts
select * from people where id in (select person_id from bank_accounts where account_number in (select account_number from atm_transactions where atm_location like "Leggett%" and transaction_type = "withdraw" and year = 2023 and month = 07 and day = 28));
-- +--------+---------+----------------+-----------------+---------------+
-- |   id   |  name   |  phone_number  | passport_number | license_plate |
-- +--------+---------+----------------+-----------------+---------------+
-- | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+---------+----------------+-----------------+---------------+

-- Search for bakery security logs around 10 AM on July 28th 2023
select activity, hour, minute, license_plate from bakery_security_logs where year = 2023 and month = 07 and day = 28 and (hour = 9 or hour = 10) order by hour asc, minute asc;
-- +----------+------+--------+---------------+
-- | activity | hour | minute | license_plate |
-- +----------+------+--------+---------------+
-- | entrance | 9    | 14     | 4328GD8       |
-- | entrance | 9    | 15     | 5P2BI95       |
-- | entrance | 9    | 20     | 6P58WS2       |
-- | entrance | 9    | 28     | G412CB7       |
-- | entrance | 10   | 8      | R3G7486       |
-- | entrance | 10   | 14     | 13FNH73       |
-- | exit     | 10   | 16     | 5P2BI95       |
-- | exit     | 10   | 18     | 94KL13X       |
-- | exit     | 10   | 18     | 6P58WS2       |
-- | exit     | 10   | 19     | 4328GD8       |
-- | exit     | 10   | 20     | G412CB7       |
-- | exit     | 10   | 21     | L93JTIZ       |
-- | exit     | 10   | 23     | 322W7JE       |
-- | exit     | 10   | 23     | 0NTHK55       |
-- | exit     | 10   | 35     | 1106N58       |
-- | entrance | 10   | 42     | NRYN856       |
-- | entrance | 10   | 44     | WD5M8I6       |
-- | entrance | 10   | 55     | V47T75I       |
-- +----------+------+--------+---------------+

-- Cross reference the identified bank account owners with the bakery departure times within 10 minutes of theft
select * from people where license_plate in (select license_plate from people where id in (select person_id from bank_accounts where account_number in (select account_number from atm_transactions where atm_location like "Leggett%" and transaction_type = "withdraw" and year = 2023 and month = 07 and day = 28)) INTERSECT select license_plate from bakery_security_logs where year = 2023 and month = 07 and day = 28 and hour = 10 and minute >= 15 and minute <= 25);
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 396669 | Iman  | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+

-- Cross reference calls logs
select * from phone_calls where caller in (select phone_number from people where license_plate in (select license_plate from people where id in (select person_id from bank_accounts where account_number in (select account_number from atm_transactions where atm_location like "Leggett%" and transaction_type = "withdraw" and year = 2023 and month = 07 and day = 28)) INTERSECT select license_plate from bakery_security_logs where year = 2023 and month = 07 and day = 28 and hour = 10 and minute >= 15 and minute <= 25)
) and year = 2023 and month = 07 and day = 28 and duration <= 60;
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | id  |     caller     |    receiver    | year | month | day | duration |
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 233 | (367) 555-5533 | (375) 555-8161 | 2023 | 7     | 28  | 45       |
-- | 255 | (770) 555-1861 | (725) 555-3243 | 2023 | 7     | 28  | 49       |
-- +-----+----------------+----------------+------+-------+-----+----------+

-- Check flights for earliest flight tomorrow
select * from flights where origin_airport_id = (select id from airports where city = "Fiftyville") and year = 2023 and month = 07 and day = 29 order by hour asc, minute asc limit 1;
-- +----+-------------------+------------------------+------+-------+-----+------+--------+
-- | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
-- +----+-------------------+------------------------+------+-------+-----+------+--------+
-- | 36 | 8                 | 4                      | 2023 | 7     | 29  | 8    | 20     |
-- +----+-------------------+------------------------+------+-------+-----+------+--------+

-- Check passengers for flight 36
select * from passengers where flight_id = 36;
-- Lookup person details for each passenger
select * from passengers inner join people on passengers.passport_number=people.passport_number where passengers.flight_id = 36;
-- +-----------+-----------------+------+--------+--------+----------------+-----------------+---------------+
-- | flight_id | passport_number | seat |   id   |  name  |  phone_number  | passport_number | license_plate |
-- +-----------+-----------------+------+--------+--------+----------------+-----------------+---------------+
-- | 36        | 7214083635      | 2A   | 953679 | Doris  | (066) 555-9701 | 7214083635      | M51FA04       |
-- | 36        | 1695452385      | 3B   | 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
-- | 36        | 5773159633      | 4A   | 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 36        | 1540955065      | 5C   | 651714 | Edward | (328) 555-1152 | 1540955065      | 130LD9Z       |
-- | 36        | 8294398571      | 6C   | 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- | 36        | 1988161715      | 6D   | 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 36        | 9878712108      | 7A   | 395717 | Kenny  | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | 36        | 8496433585      | 7B   | 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
-- +-----------+-----------------+------+--------+--------+----------------+-----------------+---------------+

-- So it was Bruce.
-- Figure out who Bruce called
select * from people where phone_number = "(375) 555-8161";
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
-- +--------+-------+----------------+-----------------+---------------+

-- Robin purchased the plane ticket.
-- Figure out where Bruce is traveling
select * from airports where id = 4;
-- +----+--------------+-------------------+---------------+
-- | id | abbreviation |     full_name     |     city      |
-- +----+--------------+-------------------+---------------+
-- | 4  | LGA          | LaGuardia Airport | New York City |
-- +----+--------------+-------------------+---------------+

-- Bruce is escaping to New York City
