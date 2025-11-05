import { TrendingDown, DollarSign } from "lucide-react";

interface PriceComparisonProps {
  bestDeal: {
    name: string;
    price: number;
    platform: string;
  };
  priceRange: {
    min: number;
    max: number;
  };
  totalCompared: number;
}

export const PriceComparison = ({
  bestDeal,
  priceRange,
  totalCompared,
}: PriceComparisonProps) => {
  const savings = priceRange.max - priceRange.min;
  const savingsPercent = ((savings / priceRange.max) * 100).toFixed(0);

  return (
    <div className="bg-price-best-bg border border-price-best/20 rounded-xl p-4 space-y-3 animate-fade-in shadow-card">
      <div className="flex items-center gap-2">
        <div className="p-2 bg-price-best rounded-lg">
          <TrendingDown className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="font-semibold text-sm text-price-best">Meilleure offre trouvée</h3>
          <p className="text-xs text-muted-foreground">{totalCompared} produits comparés</p>
        </div>
      </div>

      <div className="bg-background/50 rounded-lg p-3 space-y-2">
        <div className="flex items-baseline justify-between">
          <span className="text-sm font-medium">{bestDeal.name}</span>
          <span className="text-xs text-muted-foreground">{bestDeal.platform}</span>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-price-best">{bestDeal.price.toFixed(2)}€</span>
          {savings > 0 && (
            <span className="text-sm text-price-best font-medium">
              Économisez {savingsPercent}%
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-1 text-muted-foreground">
          <DollarSign className="w-3 h-3" />
          <span>Fourchette de prix</span>
        </div>
        <span className="font-medium">
          {priceRange.min.toFixed(2)}€ - {priceRange.max.toFixed(2)}€
        </span>
      </div>
    </div>
  );
};
