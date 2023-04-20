import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ChakraProvider, Image } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Home from "./Home";
import { extendTheme } from "@chakra-ui/react";
import "@fontsource/source-code-pro/800.css";
import Preloader from "./Preloader";
// import { Fonts } from "./Fonts";
const theme = extendTheme({
  fonts: {
    body: "Source Code Pro,monospace",
    heading: "Source Code Pro,monospace",
  },
});
function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Delay state update to remove preloader
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2500);

    // Clear timeout on unmount
    return () => clearTimeout(timer);
  }, []);

  return (
    <ChakraProvider theme={theme}>
      <Router>
        <Navbar />
        {loading && <Preloader />}
        {!loading && (
          <Routes>
            <Route path="/" exact element={<Home />} />
          </Routes>
        )}
      </Router>
    </ChakraProvider>
  );
}
export default App;
