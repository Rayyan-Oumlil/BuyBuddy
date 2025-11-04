function PriceComparison({ comparison }) {
  if (!comparison) return null

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 space-y-3">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
          <span className="text-white text-sm font-bold">🏆</span>
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 mb-1">
            Meilleur prix trouvé
          </h4>
          {comparison.best_deal && (
            <div className="space-y-1">
              <p className="text-sm text-gray-700">
                <span className="font-semibold">{comparison.best_deal.name}</span>
              </p>
              <p className="text-lg font-bold text-blue-600">
                {comparison.best_deal.price}
              </p>
              {comparison.best_deal.platform && (
                <p className="text-xs text-gray-600">
                  sur {comparison.best_deal.platform}
                </p>
              )}
            </div>
          )}
          {comparison.price_range && (
            <div className="mt-2 pt-2 border-t border-blue-200">
              <p className="text-xs text-gray-600">
                Comparé {comparison.total_compared} produits • 
                Prix de {comparison.price_range.min?.toFixed(2)}€ à {comparison.price_range.max?.toFixed(2)}€
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PriceComparison

