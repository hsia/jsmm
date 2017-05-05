net stop "Apache CouchDB"
echo D | xcopy /E /Y /D d:\CouchDB\data d:\backup\%date:~0,4%%date:~5,2%%date:~8,2%\data
net start "Apache CouchDB"