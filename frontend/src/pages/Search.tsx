import React from 'react';
import { ProductSearch } from '../components/ProductSearch';

export function Search() {
    return (
        <div className="h-full bg-gray-50 min-h-[calc(100vh-64px)]">
            <ProductSearch />
        </div>
    );
}
