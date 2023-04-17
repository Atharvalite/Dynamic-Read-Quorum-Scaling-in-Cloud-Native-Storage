import React from "react";
import Epoch from "./Epoch";
import ComparisonChart from "./ComparisonChart";
import "./Home.css";
import Videobg from "./Gifs/circuit-27725.mp4";
import Header from "./Header";
import Slide from "./Slide";

function Home(){
    return (
      <div>
        <video autoPlay loop muted>
          <source src={Videobg} type="video/mp4" />
        </video>
          <Header
            first={"Dynamic Read Quorum Scaling"}
            second={"Dynamic Read Quorum Scaling"}
          />
          <Slide/>
          <Epoch />
          <ComparisonChart />
      </div>
    );
}

export default Home;