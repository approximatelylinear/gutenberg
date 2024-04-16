import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Root, {
  loader as rootLoader,
} from "./routes/Root";

import SearchIndex, {
  loader as searchIndexLoader,
} from "./routes/SearchIndex";

import Index from "./routes/Index";

import ErrorPage from "./ErrorPage";

import './App.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    loader: rootLoader,
    children: [
      {
        path: "search/:searchIndex",
        element: <SearchIndex />,
        loader: searchIndexLoader,
      },
      { index: true, element: <Index /> },
    ],
  },
]);


function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}


export default App;
