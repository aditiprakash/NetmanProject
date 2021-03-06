$(function () {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';
  var dataset = {
    labels: labels,
    // labels: ["0", "20", "40", "60", "80", "100"],
    datasets: [{
      label: '# of Votes',
      data: info,
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1,
      fill: 
      {
        above: 'rgb(255,0,0)'
      }
      
    }]
  };
  // var multiLineData = {
  //   labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
  //   datasets: [{
  //       label: 'Dataset 1',
  //       data: [12, 19, 3, 5, 2, 3],
  //       borderColor: [
  //         '#587ce4'
  //       ],
  //       borderWidth: 2,
  //       fill: false
  //     },
  //     {
  //       label: 'Dataset 2',
  //       data: [5, 23, 7, 12, 42, 23],
  //       borderColor: [
  //         '#ede190'
  //       ],
  //       borderWidth: 2,
  //       fill: false
  //     },
  //     {
  //       label: 'Dataset 3',
  //       data: [15, 10, 21, 32, 12, 33],
  //       borderColor: [
  //         '#f44252'
  //       ],
  //       borderWidth: 2,
  //       fill: false
  //     }
  //   ]
  // };
  var options = {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        },
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }],
      xAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }]
    },
    legend: {
      display: false
    },
    elements: {
      point: {
        radius: 0
      }
    }
  };

  
  
  // var doughnutPieOptions = {
  //   responsive: true,
  //   animation: {
  //     animateScale: true,
  //     animateRotate: true
  //   }
  // };
  var areaData = {
    labels: labels,
    // labels:  ["0", "20", "40", "60", "80", "100"],
    datasets: [{
      label: 'CPU Utilization (%)',
      // data: [{% for item in info %}
      //   {{item}}
      // {% endfor %}] ,
      data: info,
      // data: info,
      // data: [1, 1, 0, 0, 2, 0, 4, 0, 5, 0, 0, 6, 0, 3, 0, 3, 2, 1],
      backgroundColor: [
        // 'rgba(255, 99, 132, 0.2)',
        // 'rgba(54, 162, 23  5, 0.2)',
        // 'rgba(255, 206, 86, 0.2)',
        // 'rgba(75, 192, 192, 0.2)',
        // 'rgba(153, 102, 255, 0.2)',    
        // 'rgba(255, 159, 64, 0.2)',
        // 'rgba(75, 192, 192, 0.2)',
        // 'rgba(153, 102, 255, 0.2)',
        // 'rgba(255, 159, 64, 0.2)',

        
      ],
      borderColor: [
        // 'rgba(255,99,132,1)',
        // 'rgba(54, 162, 235, 1)',
        // 'rgba(255, 206, 86, 1)',
        // 'rgba(75, 192, 192, 1)',
        // 'rgba(153, 102, 255, 1)',
        // 'rgba(255, 159, 64, 1)',
        // 'rgba(75, 192, 192, 1)',
        // 'rgba(153, 102, 255, 1)',
        // 'rgba(255, 159, 64, 1)'

      ],
      borderWidth: 0.8,
      fill: true, // 3: no fill
    }]
  };

  var areaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    legend: {
      labels: {
          fontColor: 'rgba(255, 159, 64, 0.4)',
          // fontSize: 18
      }
  },
    scales: {
      yAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        },
        ticks: {
          fontColor: "white",
          fontSize: 12
        }
      }],
      xAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        },
        ticks: {
          fontColor: "white",
          fontSize: 12
        },
        scaleLabel: {
          display: true,
          labelString: 'time (s)',
          fontColor: "white",
          fontSize: 12
      }
      }]
    }
  }


  if ($("#lineChart").length) {
    var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
    var lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });

  }

 
});
