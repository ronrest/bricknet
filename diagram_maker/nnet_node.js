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
function Node(x,y, dims=dims1, theme=THEME_DEFAULT, n_in=1, n_out=1){
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

    // =========================================================================
    //                                                                    DRAW()
    // =========================================================================
    this.draw = function (ctx) {
        nnet_node(ctx, this.x, this.y, this.dims.width_a, this.dims.width_b, this.dims.height, this.theme.a, this.theme.b, this.theme.border, this.dims.border, this.dims.radius);
    }

    // =========================================================================
    //                                                              CONNECT_TO()
    // =========================================================================
    // wa = index of the weight connection from this node
    //      value of -1 means we will just connect to the center of the node.
    // wb = index of the weight connection on the node we are connecting to.
    //      value of -1 means we will just connect to the center of the node
    // d = How far the bezier control point should stick out relative to the
    //     starting position.
    // d2 = as per d, but relative to the end point.
    // alpha = alpha of the connection line
    // =========================================================================
    this.connect_to = function(ctx, next_node, wa=-1, wb=-1, color="#FF0000" ,size=3, d=50, d2=50, alpha=0.3){
        // ---------------------------------------------------------------------
        //                                           Calculate the y coordinates
        // ---------------------------------------------------------------------
        // Calculate the y coordinate of the starting point
        if (wa == -1){
            var from_y = this.mid_y;
        } else {
            var from_y = this.out_wy[wa];
        }
        // Calculate the y coordinate of the end point
        if (wb == -1){
            var to_y = next_node.mid_y;
        } else {
            var to_y = next_node.in_wy[wb];
        }

        // ---------------------------------------------------------------------
        //                                                Draw Bezier Connection
        // ---------------------------------------------------------------------
        bez(ctx, this.out_wx, from_y, next_node.in_wx, to_y, size, color, d, d2, alpha)
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
        for (var i = 0; i < n; i++) {
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
//                                                    EXTRACT_COLORS_FROM_THEMES
// #############################################################################
// Extracts the preactivation colors from a list of node themes
// Returns an array of colors
function extract_colors_from_themes(themes){
    var cols = [0];
    for (var i = 0; i < themes.length; i++){
        cols[i] = themes[i].a;
    };
    return cols;
};


// #############################################################################
//                                                                       GLOBALS
// #############################################################################
// Useful Dimensions
var dims1 = new NodeDims();

// Useful theme (Default theme colors)
var THEME_DEFAULT = new NodeTheme();
var THEME_BLUE_ORANGE = new NodeTheme(a="#6699FF",b="#ff9900", border="#333333");

var THEME_GREEN = new NodeTheme(a="#1BDA32",b="#C1F9C8", border="#36A944");
var THEME_ORANGE = new NodeTheme(a="#FFA41F",b="#FFE8C6", border="#DD8B16");
var THEME_PURPLE = new NodeTheme(a="#552DCC",b="#D2C5F6", border="#30118C");
var THEME_BLUE = new NodeTheme(a="#5888ED",b="#AFC8FF", border="#2F6AE9");
var THEME_TANGERINE = new NodeTheme(a="#FF4C00",b="#FF9A6F", border="#E24300");
var THEME_FUSCIA = new NodeTheme(a="#CF45D9",b="#F7B3FB", border="#CA22D5");



var THEME_GREY_DARK = new NodeTheme(a="#424242",b="#848484", border="#333333");
var THEME_GREY_MED = new NodeTheme(a="#7E7E7E",b="#D4D4D4", border="#505050");
var THEME_GREY_LIGHT = new NodeTheme(a="#C6C6C6",b="#ECECEC", border="#7F7F7F");





// #############################################################################
//                                                                IMAGE FROM URL
// #############################################################################
// This code is taken from:
// http://www.html5canvastutorials.com/advanced/html5-canvas-load-image-data-url
//
// url = where the image resides
// x = x position to place the image on the canvas
// y = y position to place the image on the canvas
// =============================================================================
function imageFromUrl(context, url, x, y) {
        // load image from data url
        var imageObj = new Image();
        imageObj.src = url;

        imageObj.onload = function() {
          context.drawImage(this, x, y);
        };
}


//blue
//green = "orange"
function latexOnCanvas(context, latex, x, y, color="black", size=10){
    var url = "http://latex.codecogs.com/png.latex?"
    var sizes= [];
    sizes[5] = "tiny"
    sizes[9] = "small"
    sizes[10] = ""
    sizes[12] = "large"
    sizes[18] = "LARGE"
    sizes[20] = "huge"

    var colorCode = "\\fg_COLOR&space;".replace("COLOR", color);
    var sizeCode = "\\SIZE&space;".replace("SIZE", sizes[size]);

    // Put the pieces of the URL together.
    url += colorCode + sizeCode + latex;

    // render the result of the url on the canvas
    imageFromUrl(context, url, x, y);
}
