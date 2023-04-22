import React, { useState } from "react";
import {
  Box,
  Button,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  SliderTrack,
  Flex,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  Heading,
} from "@chakra-ui/react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';


function Epoch() {
  const history=useNavigate();
  const [writeQ, setWriteQ] = useState(0);
  const [readQ, setReadQ] = useState(0);
  const handleChange1 = (value) => setWriteQ(value);
  const handleChange2 = (value) => setReadQ(value);
  const Quorum={
    "write":0,
    "read":0
}
  const Navigation = async() => {
     const [response1, response2] =await Promise.all([
           axios.post("http://127.0.0.1:5000/",Quorum),
           axios.post("http://127.0.0.1:4001/",Quorum),
         ]).catch((err)=>{
          console.log(err);
         });
         const res1=await response1.body;
         const res2=await response2.body;
         return [res1,res2];
  };
function submission(event){
  event.preventDefault();
    Quorum.write=writeQ;
    Quorum.read=readQ;
    console.log('Submitted...!!');
    Navigation().then(()=>history("/demo"));

}
  return (
    <Box ml={100} mb={100} width={350} pos="fixed" top="100" left="750">
      <form onSubmit={submission}>
        <Heading as="h3" size="md" p={2}>
          Enter Write request:
        </Heading>
        <Flex boxShadow="dark-lg" p={2} rounded="md" bgColor="#00337C">
          <NumberInput
            maxW="100px"
            mr="2rem"
            value={writeQ}
            onChange={handleChange1}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <Slider
            flex="1"
            focusThumbOnChange={false}
            value={writeQ}
            onChange={handleChange1}
          >
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb fontSize="sm" boxSize="20px" children={writeQ} />
          </Slider>
        </Flex>
        <Heading as="h3" size="md" p={3}>
          Enter Read request:
        </Heading>
        <Flex mt={0} boxShadow="dark-lg" p="2" rounded="md" bgColor="#00337C">
          <NumberInput
            maxW="100px"
            mr="2rem"
            value={readQ}
            onChange={handleChange2}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <Slider
            flex="1"
            focusThumbOnChange={false}
            value={readQ}
            onChange={handleChange2}
          >
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb fontSize="sm" boxSize="20px" children={readQ} />
          </Slider>
        </Flex>
        <Button type="submit" bgColor="#146C94" variant="solid" mt={10}>
          check demo
        </Button>
      </form>
    </Box>
  );
}

export default Epoch;
