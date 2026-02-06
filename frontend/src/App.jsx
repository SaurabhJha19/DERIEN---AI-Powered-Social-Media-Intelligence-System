import { useState } from "react";
import Preloader from "./components/Preloader";
import Landing from "./pages/Landing";

function App() {
  const [ready, setReady] = useState(false);

  if (!ready) {
    return <Preloader onReady={() => setReady(true)} />;
  }

  return <Landing />;
}

export default App;
