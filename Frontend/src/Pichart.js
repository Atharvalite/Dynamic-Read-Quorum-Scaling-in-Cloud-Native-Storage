import React from "react";
import { Pie, Doughnut } from "react-chartjs-2";
import { Box } from "@chakra-ui/react";
import Chart from "chart.js/auto";

function Pichart(){
    const data = {
    labels: ['Freezed Replicas', 'Unfreezed replicas',],
    datasets: [
        {
        data: [80,20],
        backgroundColor: ['#FF6384', '#36A2EB',],
        hoverBackgroundColor: ['#FF6384', '#36A2EB'],
        },
    ],
};
const options = {
  maintainAspectRatio: false,
  responsive: true,
};
    return <Doughnut data={data} options={options} />;
};

export default Pichart;