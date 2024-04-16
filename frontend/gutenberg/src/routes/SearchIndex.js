import { useEffect } from "react";

import {
    Outlet,
    Link,
    useLoaderData,
    Form,
    redirect,
    NavLink,
    useNavigation,
    useSubmit
} from "react-router-dom";

import SearchResults from '../SearchResults';


const fetchData = async (selectedIndex, query) => {
    try {
        console.log('fetching search data...')
        const response = await fetch(`http://localhost:8000/search?index=${selectedIndex}&query=${query}`);
        console.log('response:', response);
        if (!response.ok) {
            console.error('Error fetching search results:', response.statusText);
            return [];
        }
        const data = await response.json();
        return data.current_page;
    } catch (error) {
        console.error('Error fetching search results:', error);
        return [];
    }
};

// Search loader
export async function loader({request, params}) {
    const url = new URL(request.url);
    const q = url.searchParams.get("q");
    const results = await fetchData(params.searchIndex, q);
    // const results = []
    return { results, q };
}

// Search action

export default function SearchIndex() {
    const { results, q } = useLoaderData();
    const navigation = useNavigation();
    const submit = useSubmit();

    const searching =
    navigation.location &&
    new URLSearchParams(navigation.location.search).has(
      "q"
    );

    useEffect(() => {
        document.getElementById("q").value = q;
    }, [q]);

    return (
        <>
          <div>
            {/* The default method is "get".  */}
            <Form id="search-form" role="search" className="search-container">
              <input
                id="q"
                className={
                    "search-input " +
                    searching ? "loading" : ""
                }
                aria-label="Search contacts"
                placeholder="Search"
                type="search"
                name="q"
                defaultValue={q}
                // onChange={(event) => {
                //   const isFirstSearch = q == null;
                //   submit(event.currentTarget.form, {
                //     replace: !isFirstSearch,
                //   });
                // }}
              />
              <div
                className="sr-only"
                aria-live="polite"
              >
              </div>
              <button
                type="submit"
                className="search-button"
              >
                <i className="fas fa-search"></i>
              </button>
            </Form>
          </div>
          <div
                id="search-spinner"
                aria-hidden
                hidden={!searching}
          />
          <SearchResults searchQuery={q} results={results} />
        </>
    );
}

