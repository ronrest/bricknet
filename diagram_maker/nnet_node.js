// Modified from code originally by Juan Mendes
// http://stackoverflow.com/a/3368118
/**
 * Draws a Node
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width_a The width of the pre-activation area
 * @param {Number} width_b The width of the post-activation area
 * @param {Number} height The height of the rectangle

 * @param {Boolean} [fill_a = "#6699FF"] Color of the pre-activation area.
 * @param {Boolean} [fill_b = "#ff9900"] Color of the post-activation area.
 * @param {Boolean} [stroke_col = "#333333"] Color of the border.
 * @param {Boolean} [stroke_size = 3] Width of the line to use for the border.
 * @param {Number} [radius = 10] The radius of the corners;
 */
function nnet_node(ctx, x, y, width_a=60, width_b=75, height=50, fill_a, fill_b, stroke_col, stroke_size=5, radius=15) {
  if (typeof stroke_col === 'undefined') {
    stroke_col= "#333333";
  }
  if (typeof fill_a === 'undefined') {
    fill_a = "#6699FF";
  }
  if (typeof fill_b === 'undefined') {
    fill_b = "#ff9900";
  }

  mid = x + width_a
  // ---------------------------------------------------------------------------
  //                                                            DRAW FIRST HALF
  // ---------------------------------------------------------------------------
  ctx.beginPath();
  ctx.moveTo(x + radius, y);                      // Start Just after TR corner
  ctx.lineTo(mid, y);                             // Top Line A

  ctx.lineTo(mid, y + height);                    // Mid line

  ctx.lineTo(x + radius, y + height);             // Bottom Line A

  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);  // BL Corner
  ctx.lineTo(x, y + radius);                                    // Left Line

  ctx.quadraticCurveTo(x, y, x + radius, y);                    // TL Corner
  ctx.closePath();

  // Fill it in with paint
  ctx.lineWidth = stroke_size;
  ctx.strokeStyle = stroke_col;
  ctx.fillStyle = fill_a;
  ctx.fill();
  ctx.stroke();

  // ---------------------------------------------------------------------------
  //                                                            DRAW SECOND HALF
  // ---------------------------------------------------------------------------
  end = x + width_a + width_b

  ctx.beginPath();
  ctx.moveTo(mid, y);                             // Start at mid
  ctx.lineTo(end - radius, y);                    // Top Line B

  ctx.quadraticCurveTo(end, y, end, y + radius);  // TR corner
  ctx.lineTo(end, y + height - radius);           // Right Line

  ctx.quadraticCurveTo(end, y + height, end - radius, y + height);  // BR Corner
  ctx.lineTo(mid, y + height);                    // Bottom Line B

  ctx.moveTo(mid, y);                             // Go back to mid top
  ctx.closePath();

  // Fill it in with paint
  ctx.lineWidth = stroke_size;
  ctx.strokeStyle = stroke_col;
  ctx.fillStyle = fill_b;
  ctx.fill();
  ctx.stroke();

}


// #############################################################################
//                                                                   NODE OBJECT
// #############################################################################
function Node(x,y, dims=dims1, theme=theme1, n_in=1, n_out=1){
    this.x = x;
    this.y = y;
    this.dims = dims;
    this.theme = theme;

    // Outer Points of interest
    this.mid_x = this.x + this.dims.width_a;
    this.end_x = this.mid_x + this.dims.width_b;
    this.mid_y = this.y + (this.dims.height / 2.0);
    this.end_y = this.y + this.dims.height;

    // Connection Points of interest
    this.in_wx = this.x + this.dims.radius;
    this.in_wy = y_connection_offsets(n_in, this.dims.height, y=this.y);
    this.out_wx = this.end_x - this.dims.radius;
    this.out_wy = y_connection_offsets(n_out, this.dims.height, y=this.y);



    //Method
    this.draw = function (ctx) {
        nnet_node(ctx, this.x, this.y, this.dims.width_a, this.dims.width_b, this.dims.height, this.theme.a, this.theme.b, this.theme.border, this.dims.border, this.dims.radius);
    }


}







// #############################################################################
//                                                          Y CONNECTION OFFSETS
// #############################################################################
// calculate the y offset positions realtive to the top corner for n number of
// connections evenly spaced
//
// Completely inneficient way of doing it since all nodes in a layer
// will be the same offset from the Top corner, so could just recycle the
// calculation instead.
function y_connection_offsets(n, height, y=0){
    var wy = new Array(n);
    if (n <= 1){
        wy[0] = y + (height/2.0);
    } else {
        var spacing = height / (n-1);
        for (i = 0; i < n; i++) {
            wy[i] = y + (i * spacing);
        };
    };
    return wy;
}

// #############################################################################
//                                                        NODE DIMENSIONS OBJECT
// #############################################################################
function NodeDims(width_a=65, width_b=100, height=50, radius=10, border=3){
    this.width_a = width_a;
    this.width_b = width_b;
    this.height = height;
    this.radius = radius;
    this.border= border;
}


// #############################################################################
//                                                             NODE THEME OBJECT
// #############################################################################
function NodeTheme(a="#6699FF",b="#ff9900", border="#333333"){
    this.a = a; //  Color of the pre-activation area.
    this.b = b; //  Color of the post-activation area.
    this.border= border;
}


// #############################################################################
//                                                                       GLOBALS
// #############################################################################
// Useful Dimensions
var dims1 = new NodeDims();

// Useful theme (Default theme colors)
var theme1 = new NodeTheme();