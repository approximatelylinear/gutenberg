import {
  Outlet,
  Link,
  useLoaderData,
  NavLink,
  useNavigation,
  useSubmit
} from "react-router-dom";


const fetchIndices = async () => {
  try {
      const response = await fetch('http://localhost:8000/indices');
      const data = await response.json();
      return data.indices || [];
  } catch (error) {
      console.error('Error fetching search indices:', error);
      return [];
  }
};


export async function loader({}) {
  const searchIndices = await fetchIndices();
  return { searchIndices };
}


export default function Root() {
  const { searchIndices } = useLoaderData();
  const navigation = useNavigation();
  const submit = useSubmit();

    return (
      <>
        <div id="sidebar">
          <nav>
            {searchIndices.length ? (
              <ul>
                {searchIndices.map((searchIndex) => (
                  <li key={searchIndex.name}>
                    <NavLink
                      to={`search/${searchIndex.name}`}
                    >
                      {/* <Link to={`search/${searchIndex.name}`}> */}
                        {searchIndex.name}
                      {/* </Link> */}
                    </NavLink>
                  </li>
                ))}
              </ul>
            ) : (
              <p>
                <i>No search indexes</i>
              </p>
            )}
          </nav>
        </div>
        {/* useNavigation returns the current navigation state: it can be one of "idle" | "submitting" | "loading". */}
        <div id="detail" className="detail"
          // className={
          //   navigation.state === "loading" ? "loading" : ""
          // }
        >
          <Outlet />
        </div>
      </>
    );
  }
