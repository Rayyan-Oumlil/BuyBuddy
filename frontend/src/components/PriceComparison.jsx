import { TrendingDown, DollarSign } from "lucide-react"

export const PriceComparison = ({
  bestDeal,
  priceRange,
  totalCompared,
}) => {
  if (!bestDeal || !priceRange) return null

  const savings = priceRange.max - priceRange.min
  const savingsPercent = priceRange.max > 0 ? ((savings / priceRange.max) * 100).toFixed(0) : 0

  // Ensure values are numbers
  const bestPrice = typeof bestDeal.price === "number" ? bestDeal.price : parseFloat(String(bestDeal.price).replace(/[€$,\s]/g, "").replace(",", ".")) || 0
  const minPrice = typeof priceRange.min === "number" ? priceRange.min : parseFloat(String(priceRange.min).replace(/[€$,\s]/g, "").replace(",", ".")) || 0
  const maxPrice = typeof priceRange.max === "number" ? priceRange.max : parseFloat(String(priceRange.max).replace(/[€$,\s]/g, "").replace(",", ".")) || 0

  return (
    <div className="bg-price-best-bg border border-price-best/20 rounded-xl p-4 space-y-3 animate-fade-in shadow-card dark:bg-[#3a3a3a] dark:border-[#4a4a4a] dark:text-white">
      <div className="flex items-center gap-2">
        <div className="p-2 bg-price-best rounded-lg">
          <TrendingDown className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="font-semibold text-sm text-price-best dark:text-white">Meilleure offre trouvée</h3>
          <p className="text-xs text-muted-foreground dark:text-gray-300">{totalCompared || 0} produits comparés</p>
        </div>
      </div>

      <div className="bg-background/50 dark:bg-[#4a4a4a] rounded-lg p-3 space-y-2">
        <div className="flex items-baseline justify-between">
          <span className="text-sm font-medium dark:text-white">{bestDeal.name || "Produit"}</span>
          <span className="text-xs text-muted-foreground dark:text-gray-300">{bestDeal.platform || ""}</span>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-price-best dark:text-white">{bestPrice.toFixed(2)}€</span>
          {savings > 0 && (
            <span className="text-sm text-price-best font-medium dark:text-white">
              Économisez {savingsPercent}%
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-1 text-muted-foreground dark:text-gray-300">
          <DollarSign className="w-3 h-3" />
          <span>Fourchette de prix</span>
        </div>
        <span className="font-medium dark:text-white">
          {minPrice.toFixed(2)}€ - {maxPrice.toFixed(2)}€
        </span>
      </div>
    </div>
  )
}
