import React from "react";
import { Link } from "react-router-dom";
import {
  Flex,
  Heading,
  Spacer,
<<<<<<< Updated upstream
  IconButton,
=======
  // IconButton,
>>>>>>> Stashed changes
  useColorMode,
  Button
} from "@chakra-ui/react";
 import { Menu, MenuButton, MenuList, MenuItem } from "@chakra-ui/react";
import { MoonIcon, SunIcon, ChevronDownIcon } from "@chakra-ui/icons";


function Navbar() {

  function handleButtonClick() {
    window.location.href =
      "https://github.com/Atharvalite/Dynamic-Read-Quorum-Scaling-in-Cloud-Native-Storage";
  }

  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Flex bgGradient="linear(to-l, #18122B,#19376D)" pos="fixed" width="100%">
      <Heading as="h2" mt={5} p={3} size="lg" noOfLines={1}>
        <Link to="/">DQRS System</Link>
      </Heading>
      <Spacer />
      <Button m={2} mr={4} bgColor="#146C94" onClick={handleButtonClick}>
        Learn More
      </Button>
      {/* <IconButton
        m={2}
        mr={4}
        onClick={toggleColorMode}
        _hover={colorMode === "light" ? "#E15FED"  : "#77ACF1" }
        bg={colorMode === "light" ? "#D09CFA" : "#143F6B"}
        icon={colorMode === "light" ? <MoonIcon /> : <SunIcon />}
      /> */}
    </Flex>
  );
}

export default Navbar;


