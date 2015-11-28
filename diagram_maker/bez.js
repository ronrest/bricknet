

// Function for drawing bezier curve between two points
// d = How far the control point should stick out relative to the starting
//     position.
// d2 = as per d, but relative to the end point.
function bez(context, x, y, x2, y2, size=3, color="#AAAAAA", d=50, d2=50, alpha=0.3){
      // -----------------------------------------------------------------------
      // Set the Control Points for the Bezier Curves
      // -----------------------------------------------------------------------
      var ct1_x = x + d;
      var ct1_y = y;
      var ct2_x = x2 - d2;
      var ct2_y = y2;

      // -----------------------------------------------------------------------
      // Create the Bezier Curves
      // -----------------------------------------------------------------------
      context.beginPath();
      context.moveTo(x, y);
      context.bezierCurveTo(ct1_x, ct1_y, ct2_x, ct2_y, x2, y2);
      context.lineWidth = size;

      // -----------------------------------------------------------------------
      // Set Aesthetics and Draw on page
      // -----------------------------------------------------------------------
      // line color
      var BU_Alpha = context.globalAlpha; // backs up the current alpha setting
      context.globalAlpha = alpha;        // Change the alpha
      context.strokeStyle = color;
      context.stroke();
      context.globalAlpha = BU_Alpha;     // Restores the original alpha setting
      }


