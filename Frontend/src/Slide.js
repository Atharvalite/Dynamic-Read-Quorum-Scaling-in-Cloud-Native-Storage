import { Heading,Box } from "@chakra-ui/react";
import { motion } from "framer-motion";
import Solutions from "./Solution";

const Slide = () => {
  return (
    <motion.div
      transition={{
        ease: "easeOut",
        duration: 2,
        x: { duration: 1 },
      }}
    >
      <Box pos="fixed" top="200" left="5" p={5}>
        <Heading size="md">Novel Cloud Native Storage Approach</Heading>
        <Solutions />
      </Box>
    </motion.div>
  );
};

export default Slide;