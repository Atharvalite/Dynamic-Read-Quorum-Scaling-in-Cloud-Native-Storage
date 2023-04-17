import React from "react";
import { Card, CardHeader, CardBody,Text,Box,Stack,StackDivider,Heading, Center } from "@chakra-ui/react";
function Solutions(){
    return (
      <Card
        width="400px"
        mt={15}
        bg="transparent"
        boxShadow="white-lg"
        // borderWidth="2px"
      >
        <Center>
          <CardHeader mb={-5}>
            <Heading size="lg">Benefits</Heading>
          </CardHeader>
          <CardBody>
            <Stack divider={<StackDivider />} spacing="1">
              <Box>
                <Text fontSize="md">Improved Performance</Text>
              </Box>
              <Box>
                <Text fontSize="md">Scalability</Text>
              </Box>
              <Box>
                <Text color="whiteAlpha.900" fontSize="md">
                  Optimized Network Bandwidth Usage in Cloud
                </Text>
              </Box>
              <Box>
                <Text fontSize="md">Better resource utilization</Text>
              </Box>
            </Stack>
          </CardBody>
        </Center>
      </Card>
    );
}
export default Solutions;