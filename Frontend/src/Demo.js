import React from "react";
import { Heading, Center, Flex, Box, Spacer } from "@chakra-ui/react";
import Pichart from "./Pichart";
import ComparisonChart from "./ComparisonChart";
import Videobg from "./Gifs/circuit-27725.mp4";

function Demo() {
    return (
        <div>
            <video autoPlay loop muted>
                <source src={Videobg} type="video/mp4" />
            </video>
            <Center pos="fixed" top={70} left={600}>
                <Heading size="3xl" color="#00D7FF">
                    Demo
                </Heading>
            </Center>
            <Center pos="fixed" top={90} width={1200} height={600}>
                <Flex>
                    <ComparisonChart />
                    <Spacer />
                    <Box width={400} height={350}>
                        <Pichart />
                    </Box>
                </Flex>
            </Center>
        </div>
    );
}

export default Demo;

// 127.0.0.1:5000  -our result
// 127.0.0.1:4001  -Traditional result