import { ExternalLink, ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"

export const ProductCard = ({
  name,
  price,
  link,
  platform,
  image,
  description,
}) => {
  // Format price - handle both number and string
  const priceValue = typeof price === "number" ? price : parseFloat(String(price).replace(/[€$,\s]/g, "").replace(",", ".")) || 0
  const formattedPrice = isNaN(priceValue) ? "N/A" : `${priceValue.toFixed(2)}€`

  return (
    <div className="group bg-product-card rounded-xl shadow-card hover:shadow-hover transition-all duration-300 overflow-hidden hover:bg-product-card-hover border border-border">
      <div className="aspect-square bg-muted relative overflow-hidden">
        {image ? (
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.style.display = "none"
            }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <ShoppingCart className="w-16 h-16 text-muted-foreground/30" />
          </div>
        )}
        <div className="absolute top-2 right-2 px-2 py-1 bg-background/90 backdrop-blur-sm rounded-md text-xs font-medium dark:text-white dark:bg-[#2a2a2a]/90">
          {platform}
        </div>
      </div>
      <div className="p-4 space-y-3">
        <h3 className="font-semibold text-sm line-clamp-2 leading-snug dark:text-white">{name}</h3>
        {description && (
          <p className="text-xs text-muted-foreground dark:text-gray-300 line-clamp-2">{description}</p>
        )}
        <div className="flex items-center justify-between gap-2">
          <div className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            {formattedPrice}
          </div>
          <Button
            size="sm"
            asChild
            className="group-hover:scale-105 transition-transform duration-200"
          >
            <a href={link} target="_blank" rel="noopener noreferrer">
              Voir
              <ExternalLink className="w-3 h-3 ml-1" />
            </a>
          </Button>
        </div>
      </div>
    </div>
  )
}
