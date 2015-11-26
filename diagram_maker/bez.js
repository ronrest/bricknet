

// Function for drawing bezier curve between two points
function bez(context, x, y, x2, y2, size=3, d=50){
//      var canvas = document.getElementById('myCanvas');
//      var context = canvas.getContext('2d');

      var ct1_x = x + d;
      var ct1_y = y;

      var ct2_x = x2 - d;
      var ct2_y = y2;


      context.beginPath();
      context.moveTo(x, y);
      context.bezierCurveTo(ct1_x, ct1_y, ct2_x, ct2_y, x2, y2);
      context.lineWidth = size;

      // line color
      context.strokeStyle = 'black';
      context.stroke();
      }