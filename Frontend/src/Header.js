import React from "react";
import Typewriter from "typewriter-effect";
import { Box, Heading } from "@chakra-ui/react";

function Header(props) {
  return (
    <Box maxW={700}>
      <Heading pos='relative' top={37} p={5} as="h1" size="3xl">
        <Typewriter
          onInit={(typewriter) => {
            typewriter.loop = true;
            typewriter
              .typeString(props.second)
              .start();
          }}
        />
      </Heading>
    </Box>
  );
}

export default Header;
