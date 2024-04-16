import React, { useState } from 'react';


const PassageList = ({ passages }) => {
    // Extract the list of passages from the provided structure
    const passageList = passages.hits.hits.map(hit => {
        // if (
        //     hit.highlight &&
        //     hit.highlight["passages.text"] &&
        //     hit.highlight["passages.text"].length > 0
        // ) {
        //     return hit.highlight['passages.text'][0];
        // }
        return hit._source.text;
    });

    return (
      <div className='passage-list'>
        <h4>Passages:</h4>
        <ul>
          {passageList.map((passage, index) => (
            <li key={index}>
                <span dangerouslySetInnerHTML={{ __html: passage }} />
            </li>
          ))}
        </ul>
      </div>
    );
  };


const SearchExplanation = ({ score, terms }) => {
    return (
        <div className="explanation">
            <hline />
            <span>Score: {score}</span>
            {terms.map((result, index) => (
                <span key={index}>
                    <span style={{ fontSize: 'small' }}>{result.field}:</span>
                    <span style={{ color: `rgba(0, 0, 0, ${Math.max(.25, result.weight)})` }}>{` ${result.term} (${result.weight})`}</span>
                </span>
            ))
            }
            <hline />
        </div>
    );
};


const SearchResult = ({ title, content, author, explanation, score, inner_hits }) => {
    const [expanded, setExpanded] = useState(false);

    const handleContentClick = () => {
        setExpanded(!expanded);
    };

    const passages = inner_hits?.passages;

    return (
        <div className="search-result">
            <h3 onClick={handleContentClick}>{title}</h3>
            <p><em>Author: {author}</em></p>
            <p><em>Content: </em>{expanded ? `${content.substr(0, 1000)}` : `${content.substr(0, 100)}${content.length > 100 ? '...' : ''}`}</p>
            { passages && <PassageList passages={passages} /> }
            { explanation && <SearchExplanation score={score} terms={explanation} /> }
        </div>
    );
};

export default SearchResult;
