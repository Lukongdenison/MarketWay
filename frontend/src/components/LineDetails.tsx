import React from 'react';
import { useLineInfo } from '../hooks/useMarketApi';

interface LineDetailsProps {
    lineName: string;
}

export function LineDetails({ lineName }: LineDetailsProps) {
    const { data, loading, error } = useLineInfo(lineName);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!data) return null;

    return (
        <div className="line-details">
            <h2>{data.line_name}</h2>

            {data.image_url && (
                <img
                    src={`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}${data.image_url}`}
                    alt={data.line_name}
                    className="line-image"
                />
            )}

            <div className="location">
                <strong>Location:</strong> {data.layout.column} column, position {data.layout.order}
            </div>

            <div className="items">
                <strong>Items Sold:</strong>
                <ul>
                    {data.items_sold.map((item) => (
                        <li key={item}>{item}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
