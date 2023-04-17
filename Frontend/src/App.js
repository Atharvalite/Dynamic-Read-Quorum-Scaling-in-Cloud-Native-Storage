import * as React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ChakraProvider, Image } from "@chakra-ui/react";
import Navbar from "./Navbar";
import Home from "./Home";
import Demo from "./Demo";
import { extendTheme } from "@chakra-ui/react";
import "@fontsource/source-code-pro/800.css";
// import { Fonts } from "./Fonts";
const theme = extendTheme({
  fonts: {
    body: "Source Code Pro,monospace",
    heading: "Source Code Pro,monospace"
  },
});
function App() {
  return (
    <Router>
      <ChakraProvider theme={theme}>
        <Navbar />
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/demo" exact element={<Demo />} />
        </Routes>
      </ChakraProvider>
    </Router>
  );
}
export default App;
