import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Root, {
  loader as rootLoader,
} from "./routes/Root";

import SearchIndex, {
  loader as searchIndexLoader,
} from "./routes/SearchIndex";

import Index from "./routes/Index";

import ErrorPage from "./ErrorPage";

import Contact, {
  loader as contactLoader,
  action as contactAction,
} from "./routes/Contact";

import EditContact, {
  action as editAction,
} from "./routes/Edit";

import { action as destroyAction } from "./routes/Destroy";


import logo from './logo.svg';
import './App.css';
// import Search from './Search';

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
      {
        path: "contacts/:contactId",
        element: <Contact />,
        loader: contactLoader,
        action: contactAction,
      },
      {
        path: "contacts/:contactId/edit",
        element: <EditContact />,
        loader: contactLoader,
        action: editAction,
      },
      {
        path: "contacts/:contactId/destroy",
        action: destroyAction,
      },
    ],
  },
]);


function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
      {/* <Router>
        <Switch>
          <Route path="/:index" component={Search} />
          <Route path="/" component={Search} />
        </Switch>
      </Router> */}
    </div>
  );
}


// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <Search />
//       </header>
//     </div>
//   );
// }

export default App;
