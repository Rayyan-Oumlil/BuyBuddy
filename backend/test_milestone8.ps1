# Test Milestone 8 : Price Comparator Agent
# Ce script teste la comparaison automatique des prix

Write-Host "Test Milestone 8 : Price Comparator Agent" -ForegroundColor Cyan
Write-Host ("=" * 60)

$baseUrl = "http://localhost:8000/api/v1/chat"

# Test : Recherche avec comparaison de prix
Write-Host "`nTest : Recherche avec comparaison de prix" -ForegroundColor Yellow
Write-Host "Requete : laptop gaming sous 1500 euros" -ForegroundColor Gray

$request = @{
    message = "laptop gaming sous 1500 euros"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $baseUrl -Method POST -Headers @{"Content-Type"="application/json"} -Body $request
    
    Write-Host "Reponse recue !" -ForegroundColor Green
    Write-Host "Nombre de produits : $($response.products.Count)" -ForegroundColor Cyan
    
    # Afficher la comparaison de prix
    if ($response.price_comparison) {
        Write-Host "`nComparaison de prix :" -ForegroundColor Yellow
        Write-Host "  Recommendation : $($response.price_comparison.recommendation)" -ForegroundColor Green
        
        if ($response.price_comparison.best_deal) {
            $best = $response.price_comparison.best_deal
            Write-Host "`n  Meilleur prix :" -ForegroundColor Cyan
            Write-Host "    Produit : $($best.name)" -ForegroundColor Gray
            Write-Host "    Prix : $($best.price)" -ForegroundColor Gray
            Write-Host "    Plateforme : $($best.platform)" -ForegroundColor Gray
        }
        
        if ($response.price_comparison.price_range) {
            $range = $response.price_comparison.price_range
            Write-Host "`n  Plage de prix :" -ForegroundColor Cyan
            Write-Host "    Min : $($range.min)" -ForegroundColor Gray
            Write-Host "    Max : $($range.max)" -ForegroundColor Gray
        }
        
        Write-Host "`n  Produits compares : $($response.price_comparison.total_compared)" -ForegroundColor Cyan
        
        # Afficher les 3 premiers produits (triés par prix)
        Write-Host "`n  Top 3 produits (par prix) :" -ForegroundColor Yellow
        $sortedProducts = $response.price_comparison.price_comparison
        for ($i = 0; $i -lt [Math]::Min(3, $sortedProducts.Count); $i++) {
            $product = $sortedProducts[$i]
            Write-Host "    $($i+1). $($product.name) - $($product.price) ($($product.platform))" -ForegroundColor Gray
        }
        
        Write-Host "`nSUCCES : Comparaison de prix fonctionnelle !" -ForegroundColor Green
    } else {
        Write-Host "`nATTENTION : Aucune comparaison de prix disponible" -ForegroundColor Yellow
    }
    
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

