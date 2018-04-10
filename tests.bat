cls
:RES
cd game
set /p cmd="#TestCase:" %=%
python tests.py %cmd%
goto:RES
