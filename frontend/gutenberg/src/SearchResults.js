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
                        key={result._id}
                        title={result._source.title.substr(0, 50)}
                        content={result._source.text}
                        author={result._source.author}
                        score={result._score}
                        explanation={result.parsed_explanation}
                        inner_hits={result.inner_hits}
                    />
                ))
            ) : (
                <NoResults />
            )}
        </div>
    );
};

export default SearchResults;
