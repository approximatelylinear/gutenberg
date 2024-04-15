import React, { useState } from 'react';
import SearchInput from './SearchInput';
import SearchResults from './SearchResults';

const Search = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
    };

    const fetchSearchResults = async (query) => {
        // TODO - allow user to select index
        try {
            const response = await fetch(`http://localhost:8000/search?index=gutenberg_0&query=${query}`);
            const data = await response.json();
            setResults(data.current_page || []);
        } catch (error) {
            console.error('Error fetching search results:', error);
            setResults([]);
        }
    };

    const handleSearch = (query) => {
        setSearchQuery(query);
        fetchSearchResults(query);
    };

    return (
        <div>
            <SearchInput
                searchQuery={searchQuery}
                handleSearch={handleSearch}
                handleInputChange={handleSearchChange}
            />
            <SearchResults searchQuery={searchQuery} results={results} />
        </div>
    );
};

export default Search;
