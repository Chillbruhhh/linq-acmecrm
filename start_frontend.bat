@echo off
echo Starting Linq-AcmeCRM Frontend Demo...
echo Opening frontend at: http://localhost:8080
echo.
echo To use the API:
echo 1. Frontend: Open frontend/index.html in your browser
echo 2. Swagger UI: http://localhost:8200/docs
echo.
echo Press any key to open the frontend HTML file...
pause
start "" "%CD%\frontend\index.html"
echo Frontend opened! Use the dropdown to select JWT tokens.
echo.
echo Backend API running at: http://localhost:8200
pause
