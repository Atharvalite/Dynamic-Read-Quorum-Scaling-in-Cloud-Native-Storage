import { Box } from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { useColorModeValue } from "@chakra-ui/react";
import { useTheme } from "@emotion/react";
import Chart from "chart.js/auto";


const chartData = {
  labels: ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
  datasets: [
    {
      label: "Traditional",
      data: [0, 10, 15, 20, 28, 36, 48, 65, 71, 84],
      fill: false,
      borderColor: "rgb(255, 99, 132)", // Set color for first line
      tension: 0.1,
    },
    {
      label: "DQRS System",
      data: [0, 6, 11, 16, 20,24,38,52,60,67],
      fill: false,
      borderColor: "rgb(54, 162, 235)", // Set color for second line
      tension: 0.1,
    },
  ],
};

function ComparisonChart() {
  const theme = useTheme();
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

  // const [chartData, setChartData] = useState({});
  return (
    <Box
      mt={100}
      maxH="500px"
      width="600px"
      pos="fixed"
      top="350"
      left="800"
      bgColor="#000000"
    >
      <Line data={chartData} options={options} />
    </Box>
  );
}

export default ComparisonChart;
