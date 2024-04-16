import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import SearchInput from './SearchInput';
import SearchResults from './SearchResults';
import SearchIndexSelector from './SearchIndexSelector';

const Search = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [results, setResults] = useState([]);
    const [index, setIndex] = useState(null);
    const location = useLocation();

    useEffect(() => {
        const path = location.pathname;
        const pathParts = path.split('/');
        const currentPathIndex = pathParts[1];

        if (currentPathIndex) {
            setIndex(currentPathIndex);
            fetchData(searchQuery, currentPathIndex);
        } else {
            // Handle case where index is not present in the path
            // You can ask the user to select an index here
            // For now, setting a default index as 'gutenberg_0'
            setIndex('gutenberg_0');
            fetchData(searchQuery, 'gutenberg_0');
        }
    }, [location.pathname, searchQuery]);

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
    };

    const fetchData = async (query, selectedIndex) => {
        try {
            const response = await fetch(`http://localhost:8000/search?index=${selectedIndex}&query=${query}`);
            const data = await response.json();
            setResults(data.current_page || []);
        } catch (error) {
            console.error('Error fetching search results:', error);
            setResults([]);
        }
    };

    const handleSearch = (query) => {
        setSearchQuery(query);
        fetchData(query, index);
    };

    return (
        <div>
            <SearchIndexSelector />
            { index ?
                (
                    <div>
                    <h1>Search Index: {index}</h1>
                    <SearchInput
                    searchQuery={searchQuery}
                    handleSearch={handleSearch}
                    handleInputChange={handleSearchChange}
                    />
                    <SearchResults searchQuery={searchQuery} results={results} />
                    </div>
                )
                : (
                    <h1>Select a search index</h1>
                )
        }
        </div>
    );
};

export default Search;
