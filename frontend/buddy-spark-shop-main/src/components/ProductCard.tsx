import { ExternalLink, ShoppingCart } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ProductCardProps {
  name: string;
  price: number;
  link: string;
  platform: string;
  image?: string;
  description?: string;
}

export const ProductCard = ({
  name,
  price,
  link,
  platform,
  image,
  description,
}: ProductCardProps) => {
  return (
    <div className="group bg-product-card rounded-xl shadow-card hover:shadow-hover transition-all duration-300 overflow-hidden hover:bg-product-card-hover border border-border">
      <div className="aspect-square bg-muted relative overflow-hidden">
        {image ? (
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <ShoppingCart className="w-16 h-16 text-muted-foreground/30" />
          </div>
        )}
        <div className="absolute top-2 right-2 px-2 py-1 bg-background/90 backdrop-blur-sm rounded-md text-xs font-medium">
          {platform}
        </div>
      </div>
      <div className="p-4 space-y-3">
        <h3 className="font-semibold text-sm line-clamp-2 leading-snug">{name}</h3>
        {description && (
          <p className="text-xs text-muted-foreground line-clamp-2">{description}</p>
        )}
        <div className="flex items-center justify-between gap-2">
          <div className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            {price.toFixed(2)}€
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
  );
};
