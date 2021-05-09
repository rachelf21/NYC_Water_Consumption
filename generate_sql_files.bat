echo on
echo Generating SQL files

REM set mydate=%date:~10,4%-%date:~4,2%-%date:~7,2%-backup


cd C:\Users\Rachel\OneDrive\Brooklyn College\6-Bklyn College Spring 2021\CISC 3810 Database\NYC_Water_Consumption\sql_files

pg_dump --username=postgres --password=postgres --table=bills --column-inserts water_consumption > bills.sql
pg_dump --username=postgres --password=postgres --table=borough --column-inserts water_consumption > borough.sql
pg_dump --username=postgres --password=postgres --table=building --column-inserts water_consumption > building.sql
pg_dump --username=postgres --password=postgres --table=cost --column-inserts water_consumption > cost.sql
pg_dump --username=postgres --password=postgres --table=development --column-inserts water_consumption > development.sql
pg_dump --username=postgres --password=postgres --table=meter --column-inserts water_consumption > meter.sql
pg_dump --username=postgres --password=postgres --table=meters_in_bldg --column-inserts water_consumption > meters_in_bldg.sql
pg_dump --username=postgres --password=postgres --table=rate --column-inserts water_consumption > rate.sql
pg_dump --username=postgres --password=postgres --table=service --column-inserts water_consumption > service.sql
pg_dump --username=postgres --password=postgres --table=vendor --column-inserts water_consumption > vendor.sql
pg_dump --username=postgres --password=postgres --table=users --column-inserts water_consumption > users.sql


pause
