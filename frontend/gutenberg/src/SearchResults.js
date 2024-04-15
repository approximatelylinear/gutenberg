import React from 'react';
import SearchResult from './SearchResult';
import NoResults from './NoResults';

const SearchResults = ({ searchQuery, results }) => {
    return (
        <div>
            <h2>Search Results for "{searchQuery}"</h2>
            {results.length > 0 ? (
                results.map(result => (
                    <SearchResult
                        key={result.id}
                        title={result.title.substr(0, 50)}
                        content={result.text}
                        author={result.author}
                    />
                ))
            ) : (
                <NoResults />
            )}
        </div>
    );
};

export default SearchResults;
