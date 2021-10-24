"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// Team Overview Demo
// =============================================================
var TeamOverviewDemo =
/*#__PURE__*/
function () {
  function TeamOverviewDemo() {
    _classCallCheck(this, TeamOverviewDemo);

    this.init();
  }

  _createClass(TeamOverviewDemo, [{
    key: "init",
    value: function init() {
      // event handlers
      this.progressChart();
    }
  }, {
    key: "randomScalingFactor",
    value: function randomScalingFactor() {
      return (Math.random() > 0.5 ? 1.0 : 1.0) * Math.round(Math.random() * 10);
    }
  }, {
    key: "progressChart",
    value: function progressChart() {
      var data = {
        labels: ['WW09', 'WW10', 'WW11', 'WW12', 'WW13', 'WW14'],
        datasets: [{
          label: 'Pass',
          backgroundColor: Looper.colors.brand.green,
          data: [6,7,7,10,11]
        }, {
          label: 'Fail',
          backgroundColor: Looper.colors.brand.red,
          data: [0, 0, 0,0,0,0]
        }, {
          label: 'In Progress',
          backgroundColor: Looper.colors.brand.pink,
          data: [1,2,5,2,0]
        }, {
          label: 'Blocked',
          backgroundColor: Looper.colors.brand.orange,
          data: [7,5,3,3,3]
        }, {
          label: 'Not Tested',
          backgroundColor: Looper.colors.brand.yellow,
          data: [7,7,6,6,6]
        }] // init progress chart

      };
      var canvas = $('#canvas-progress')[0].getContext('2d');
      var chart = new Chart(canvas, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          legend: {
            display: true
          },
          title: {
            display: true,
            text: "Test Progress"
          },
          tooltips: {
            mode: 'index',
            intersect: false
          },
          scales: {
            xAxes: [{
              stacked: true
            }],
            yAxes: [{
              stacked: true
            }]
          }
        }
      });
    }
  }]);

  return TeamOverviewDemo;
}();
/**
 * Keep in mind that your scripts may not always be executed after the theme is completely ready,
 * you might need to observe the `theme:load` event to make sure your scripts are executed after the theme is ready.
 */


$(document).on('theme:init', function () {
  new TeamOverviewDemo();
});