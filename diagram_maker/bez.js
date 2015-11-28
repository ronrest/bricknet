

// Function for drawing bezier curve between two points
// d = How far the control point should stick out relative to the starting
//     position.
// d2 = as per d, but relative to the end point.
function bez(context, x, y, x2, y2, size=3, color="#333333", d=50, d2=50){
      var ct1_x = x + d;
      var ct1_y = y;
      var ct2_x = x2 - d2;
      var ct2_y = y2;


      context.beginPath();
      context.moveTo(x, y);
      context.bezierCurveTo(ct1_x, ct1_y, ct2_x, ct2_y, x2, y2);
      context.lineWidth = size;

      // line color
      context.strokeStyle = color;
      context.stroke();
      }

