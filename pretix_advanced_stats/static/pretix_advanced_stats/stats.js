// chart.js
var ctx = document.getElementById("bar-chart").getContext("2d");
var canvas = document.getElementById("bar-chart");
var data = JSON.parse(canvas.getAttribute("data-chart")); // Retrieve data
var datapoints = data.datasets[0].data.concat(data.datasets[1]?.data || []);
const maxValue = Math.max(...datapoints);
const padding = maxValue * 0.1; // Add 10% padding
var config = {
  type: "bar",
  data: data,
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
        },
      },
      y: {
        beginAtZero: true,
        max: maxValue + padding,
        title: {
          display: true,
          text: "Nr. of tickets",
        },
        ticks: {
          stepSize: 1, // Ensures steps of 1
          callback: function (value) {
            return Number.isInteger(value) ? value : ""; // Show only integers
          },
        },
      },
    },
    plugins: {
      legend: {
        position: "top",
      },
    },
    layout: { padding: 5 },
  },
};

chart = new Chart(ctx, config);
chart.canvas.parentNode.style.height = "500px";
chart.canvas.parentNode.style.width = "100%";
