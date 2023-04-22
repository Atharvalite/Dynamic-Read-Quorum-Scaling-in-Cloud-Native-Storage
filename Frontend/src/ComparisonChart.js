import { Box, Center, Heading } from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { useColorModeValue } from "@chakra-ui/react";
import { useTheme } from "@emotion/react";
import Chart from "chart.js/auto";
import axios from "axios";
import Typewriter from "typewriter-effect";



function ComparisonChart() {
    const [chartData, setChartData] = useState({});
     const theme = useTheme();
   useEffect(() => {
     const fetchData = async () => {
       try {
         const [response1, response2] = await Promise.all([
           axios.get("http://127.0.0.1:5000/"),
           axios.get("http://127.0.0.1:4001/"),
         ]);

         const data1 = await response1.data;
         const data2 = await response2.data;
         console.log(data1);
         console.log(data2); 
         const formattedData = {
           labels: [
             "0",
             "20",
             "40",
             "60",
             "80",
             "100",
           ],
           datasets: [
             {
               label: "DRQS",
               data: data1,
               fill: false,
               borderColor: "rgb(75, 192, 192)",
               tension: 0.1,
             },
             {
               label: "Traditional",
               data: data2,
               fill: false,
               borderColor: "rgb(192, 75, 192)",
               tension: 0.1,
             },
           ],
         };
         setChartData(formattedData);
       } catch (error) {
         console.error(error);
       }
     };

     fetchData();
   }, []);

  const textColor = useColorModeValue(
    theme.colors.gray[700],
    theme.colors.white
  );
  const backgroundColor = useColorModeValue(
    theme.colors.white,
    theme.colors.gray[700]
  );

  const options = {
    responsive: true,
    scales: {
      x: {
        grid: {
          color: textColor,
          borderColor: backgroundColor,
        },
        ticks: {
          color: textColor,
        },
      },
      y: {
        grid: {
          color: textColor,
          borderColor: backgroundColor,
        },
        ticks: {
          color: textColor,
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
  };
  if (!chartData || !chartData.datasets || !chartData.datasets[0].data) {
    return (<Box width={600} height={300}>
        <Center>
          <Heading size="2xl">
            <Typewriter
              onInit={(typewriter) => {
                typewriter.loop = true;
                typewriter.typeString("LOADING...").start();
              }}
            />
            <Heading size="sm">Processing the input</Heading>
          </Heading>
        </Center>
      </Box>);
  }
  return (
    <Box  width={600} height={300} bgColor='#000000' opacity={0.7}>
      <Line data={chartData} options={options} />
    </Box>
  );
}

export default ComparisonChart;
