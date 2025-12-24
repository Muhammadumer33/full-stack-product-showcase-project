'use client';

import React from 'react';
import { Star, Edit, Trash2, Package } from 'lucide-react';
import { Product } from '@/services/api';

interface ProductCardProps {
    product: Product;
    onEdit: (product: Product) => void;
    onDelete: (id: number) => void;
}

export default function ProductCard({ product, onEdit, onDelete }: ProductCardProps) {
    const imageUrl = product.image_path
        ? `http://localhost:8000${product.image_path}`
        : null;

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
            {/* Image */}
            <div className="h-48 bg-gray-200 relative">
                {imageUrl ? (
                    <img
                        src={imageUrl}
                        alt={product.name}
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="w-full h-full flex items-center justify-center">
                        <Package className="w-16 h-16 text-gray-400" />
                    </div>
                )}

                {/* Stock Badge */}
                <div className={`absolute top-2 right-2 px-2 py-1 rounded text-xs font-semibold ${product.stock > 0 ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    }`}>
                    {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
                </div>
            </div>

            {/* Content */}
            <div className="p-4">
                {/* Category Badge */}
                <span className="inline-block px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-800 rounded mb-2">
                    {product.category}
                </span>

                {/* Title */}
                <h3 className="text-lg font-semibold text-gray-800 mb-1 truncate">
                    {product.name}
                </h3>

                {/* Brand */}
                <p className="text-sm text-gray-500 mb-2">{product.brand}</p>

                {/* Description */}
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {product.description}
                </p>

                {/* Rating */}
                <div className="flex items-center mb-3">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="ml-1 text-sm font-medium text-gray-700">
                        {product.rating?.toFixed(1) || '0.0'}
                    </span>
                </div>

                {/* Price and Actions */}
                <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-green-600">
                        ${product.price.toFixed(2)}
                    </span>

                    <div className="flex gap-2">
                        <button
                            onClick={() => onEdit(product)}
                            className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                        >
                            <Edit className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => onDelete(product.id!)}
                            className="p-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}