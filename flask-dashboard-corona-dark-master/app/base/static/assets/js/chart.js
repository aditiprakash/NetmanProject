$(function () {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';
  var data = {
    labels: ["0", "20", "40", "60", "80", "100"],
    datasets: [{
      label: '# of Votes',
    //   data: [{% for item in info %}
    //   {{item}}
    // {% endfor %}] ,
      data: info,
      // data: info,
      // data: [1, 1, 0, 0, 2, 0, 4, 0, 5, 0, 0, 6, 0, 3, 0, 3, 2, 1],
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
      fill: true
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

  
  var doughnutPieData = {
    datasets: [{
      data: [30, 40, 30],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
      'Pink',
      'Blue',
      'Yellow',
    ]
  };
  // var doughnutPieOptions = {
  //   responsive: true,
  //   animation: {
  //     animateScale: true,
  //     animateRotate: true
  //   }
  // };
  var areaData = {
    labels:  ["0", "20", "40", "60", "80", "100"],
    datasets: [{
      label: '# of Votes',
      // data: [{% for item in info %}
      //   {{item}}
      // {% endfor %}] ,
      data: info,
      // data: info,
      // data: [1, 1, 0, 0, 2, 0, 4, 0, 5, 0, 0, 6, 0, 3, 0, 3, 2, 1],
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
      fill: true, // 3: no fill
    }]
  };

  var areaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    scales: {
      yAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }],
      xAxes: [{
        gridLines: {
          color: "rgba(204, 204, 204,0.1)"
        }
      }]
    }
  }


  if ($("#lineChart").length) {
    var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
    // var temp = {{  info  }};
    // console.log(temp);

    var lineChart = new Chart(lineChartCanvas, {
      type: 'line',
      data: data,
      options: options
    });
    console.log(data);
  }

 
});
