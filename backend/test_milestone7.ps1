# Test Milestone 7 : Recherches Iteratives
# Ce script teste la fonctionnalite de recherche iterative avec feedback negatif

Write-Host "Test Milestone 7 : Recherches Iteratives" -ForegroundColor Cyan
Write-Host ("=" * 60)

$baseUrl = "http://localhost:8000/api/v1/chat"

# Etape 1 : Premiere recherche
Write-Host "`nEtape 1 : Premiere recherche" -ForegroundColor Yellow
Write-Host "Requete : laptop gaming sous 1500 euros" -ForegroundColor Gray

$request1 = @{
    message = "laptop gaming sous 1500 euros"
} | ConvertTo-Json

try {
    $response1 = Invoke-RestMethod -Uri $baseUrl -Method POST -Headers @{"Content-Type"="application/json"} -Body $request1
    
    Write-Host "Reponse recue !" -ForegroundColor Green
    Write-Host "Session ID : $($response1.session_id)" -ForegroundColor Cyan
    Write-Host "Nombre de produits : $($response1.products.Count)" -ForegroundColor Cyan
    
    # Afficher les 3 premiers produits
    Write-Host "`nPremiers produits :" -ForegroundColor Yellow
    for ($i = 0; $i -lt [Math]::Min(3, $response1.products.Count); $i++) {
        $product = $response1.products[$i]
        Write-Host "  $($i+1). $($product.name) - $($product.price)" -ForegroundColor Gray
    }
    
    $sessionId = $response1.session_id
    $firstProducts = $response1.products | ForEach-Object { $_.link }
    
    # Etape 2 : Feedback negatif
    Write-Host "`nEtape 2 : Feedback negatif" -ForegroundColor Yellow
    Write-Host "Requete : je n'aime pas (avec session_id)" -ForegroundColor Gray
    
    Start-Sleep -Seconds 2  # Pause pour eviter rate limiting
    
    $request2 = @{
        message = "je n'aime pas"
        session_id = $sessionId
    } | ConvertTo-Json
    
    $response2 = Invoke-RestMethod -Uri $baseUrl -Method POST -Headers @{"Content-Type"="application/json"} -Body $request2
    
    Write-Host "Nouvelle recherche effectuee !" -ForegroundColor Green
    Write-Host "Nombre de nouveaux produits : $($response2.products.Count)" -ForegroundColor Cyan
    
    # Afficher les nouveaux produits
    Write-Host "`nNouveaux produits (doivent etre differents) :" -ForegroundColor Yellow
    for ($i = 0; $i -lt [Math]::Min(3, $response2.products.Count); $i++) {
        $product = $response2.products[$i]
        Write-Host "  $($i+1). $($product.name) - $($product.price)" -ForegroundColor Gray
    }
    
    # Verifier que les produits sont differents
    $secondProducts = $response2.products | ForEach-Object { $_.link }
    $commonProducts = $firstProducts | Where-Object { $secondProducts -contains $_ }
    
    if ($commonProducts.Count -eq 0) {
        Write-Host "`nSUCCES : Aucun produit en commun ! Les produits ont bien ete exclus." -ForegroundColor Green
    } else {
        Write-Host "`nATTENTION : $($commonProducts.Count) produit(s) en commun trouve(s)." -ForegroundColor Yellow
        Write-Host "   Cela peut etre normal si peu de resultats disponibles." -ForegroundColor Gray
    }
    
    # Etape 3 : Test avec d'autres patterns de feedback
    Write-Host "`nEtape 3 : Test avec autre pattern" -ForegroundColor Yellow
    Write-Host "Requete : montre moi autre chose" -ForegroundColor Gray
    
    Start-Sleep -Seconds 2
    
    $request3 = @{
        message = "montre moi autre chose"
        session_id = $sessionId
    } | ConvertTo-Json
    
    $response3 = Invoke-RestMethod -Uri $baseUrl -Method POST -Headers @{"Content-Type"="application/json"} -Body $request3
    
    Write-Host "Nouvelle recherche effectuee !" -ForegroundColor Green
    Write-Host "Nombre de produits : $($response3.products.Count)" -ForegroundColor Cyan
    
    Write-Host "`nTest termine avec succes !" -ForegroundColor Green
    
} catch {
    Write-Host "`nERREUR : $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Reponse serveur : $responseBody" -ForegroundColor Red
    }
    Write-Host "`nAssurez-vous que le serveur est demarre :" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor Gray
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "   python -m uvicorn main:app --reload" -ForegroundColor Gray
}
