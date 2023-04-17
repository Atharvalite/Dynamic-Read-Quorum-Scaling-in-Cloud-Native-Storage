import React from "react";
import {
  Flex,
  Heading,
  Spacer,
  useColorMode,
  Button
} from "@chakra-ui/react";
import { Link } from "react-router-dom";

function Navbar() {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Flex bgGradient="linear(to-l, #18122B,#19376D)">
      <Heading as="h2" p={3} size="lg" noOfLines={1}>
        <Link to="/">DQRS System</Link>
      </Heading>
      <Spacer />
      <Button m={2} mr={4} bgColor="#146C94">
        <Link to="/learnmore">Learn More</Link>
      </Button>
    </Flex>
  );
}

export default Navbar;
