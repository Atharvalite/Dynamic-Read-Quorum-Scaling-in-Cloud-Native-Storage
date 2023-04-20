import { Center, Image } from "@chakra-ui/react";
import pl from "./Gifs/NewPreloader2.mp4";

const Preloader = () => {
  return (
    <Center height="100vh">
      <video
        style={{ filter: "brightness(130%)" }}
        src={pl}
        autoPlay
        muted
      ></video>
    </Center>
  );
};

export default Preloader;
