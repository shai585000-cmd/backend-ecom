# Script pour remplir la base de donnees distante
# Executer avec: .\run_populate.ps1

$env:DATABASE_URL="postgresql://ecommerce_gf50_user:eyefaetl2KIbxAZJ2EemVaCzLLzVD8Yg@dpg-d4kvo8v5r7bs73clpe9g-a.oregon-postgres.render.com/ecommerce_gf50"

Write-Host "Connexion a la base de donnees distante..."
Write-Host "Execution du script de population..."

python populate_database.py

Write-Host ""
Write-Host "Termine!"
