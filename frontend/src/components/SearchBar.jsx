import React, { useState } from 'react';
import { Search, Sparkles } from 'lucide-react';

const SUGGESTED_QUERIES = [
    "Sales by Region",
    "Brand-wise Sales",
    "Top Performing Employees",
    "Monthly Growth Trend",
    "Sales by Product Type"
];

const SearchBar = ({ onSearch, isLoading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
        }
    };

    const handleSuggestedClick = (suggested) => {
        setQuery(suggested);
        onSearch(suggested);
    };

    return (
        <div className="search-dashboard-card">
            <div className="search-header">
                <Sparkles size={18} className="accent-icon" color="var(--primary)" />
                <h2>Ask Nova Analytics</h2>
            </div>

            <form className="search-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    className="premium-input"
                    placeholder="Ask your data anything (e.g., 'Show me sales performance by region for Q3')..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                />
                <button type="submit" className="btn btn-primary" disabled={isLoading}>
                    {isLoading ? 'Processing...' : 'Generate'}
                </button>
            </form>

            <div className="suggested-section">
                <span className="label-suggested">Suggested:</span>
                {SUGGESTED_QUERIES.map((q) => (
                    <button
                        key={q}
                        className="tag"
                        onClick={() => handleSuggestedClick(q)}
                        disabled={isLoading}
                        type="button"
                    >
                        {q}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default SearchBar;
