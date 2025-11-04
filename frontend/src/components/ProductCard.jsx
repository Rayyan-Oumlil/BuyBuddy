import { ExternalLink } from 'lucide-react'

function ProductCard({ product }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
      {product.image && (
        <div className="aspect-video bg-gray-100 overflow-hidden">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
        </div>
      )}
      <div className="p-4 space-y-2">
        <h3 className="font-semibold text-gray-900 line-clamp-2 text-sm">
          {product.name}
        </h3>
        {product.description && (
          <p className="text-xs text-gray-600 line-clamp-2">
            {product.description}
          </p>
        )}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-2">
            {product.price && (
              <span className="text-lg font-bold text-blue-600">
                {product.price}
              </span>
            )}
            {product.platform && (
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {product.platform}
              </span>
            )}
          </div>
          <a
            href={product.link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            Voir
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  )
}

export default ProductCard

