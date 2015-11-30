// Modified from code originally by Juan Mendes
// http://stackoverflow.com/a/3368118
/**
 * Draws a Node
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width_a The width of the pre-activation area
 * @param {Number} width_b The width of the post-activation area
 *                 iff you want an input node, use -1 for width_b.
 * @param {Number} height The height of the rectangle

 * @param {Boolean} [fill_a = "#6699FF"] Color of the pre-activation area.
 * @param {Boolean} [fill_b = "#ff9900"] Color of the post-activation area.
 * @param {Boolean} [stroke_col = "#333333"] Color of the border.
 * @param {Boolean} [stroke_size = 3] Width of the line to use for the border.
 * @param {Number} [radius = 10] The radius of the corners;
 */
function draw_node(ctx, x, y, width_a=60, width_b=75, height=50, fill_a, fill_b, stroke_col, stroke_size=5, radius=15) {
  if (typeof stroke_col === 'undefined') {
    stroke_col= "#333333";
  }
  if (typeof fill_a === 'undefined') {
    fill_a = "#6699FF";
  }
  if (typeof fill_b === 'undefined') {
    fill_b = "#ff9900";
  }

  // Handle nodes without a split
  var homogenous = false;
  if (width_b < 0){
        homogenous = true;
        width_a = width_a / 2.0;
        width_b = width_a;
  };

  // Middle of the node along x axis.
  var mid = x + width_a
  var end = x + width_a + width_b

  // ---------------------------------------------------------------------------
  //                                                                 HOMOGENOUS
  // ---------------------------------------------------------------------------
  if (homogenous){
      ctx.beginPath();
      ctx.moveTo(x + radius, y);                      // Start Just after TR corner
      ctx.lineTo(end - radius, y);                    // Top Line

      ctx.quadraticCurveTo(end, y, end, y + radius);  // TR corner
      ctx.lineTo(end, y + height - radius);           // Right Line

      ctx.quadraticCurveTo(end, y + height, end - radius, y + height);  // BR Corner

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

  } else {
      // -----------------------------------------------------------------------
      //                                                         DRAW FIRST HALF
      // -----------------------------------------------------------------------
      ctx.beginPath();
      ctx.moveTo(x + radius, y);                      // Start Just after TR corner
      ctx.lineTo(mid, y);                             // Top Line A

      // Go down middle section
      ctx.lineTo(mid, y + height);                // Mid line

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
    };
}


// #############################################################################
//                                                                   NODE OBJECT
// #############################################################################
// bias = {boolean} is this node a bias node?
function Node(x,y, dims=dims1, theme=THEME_DEFAULT, n_in=1, n_out=1, bias=false){
    this.x = x;
    this.y = y;
    this.dims = dims;
    this.theme = theme;
    this.is_bias = bias;

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
        draw_node(ctx, this.x, this.y, this.dims.width_a, this.dims.width_b, this.dims.height, this.theme.a, this.theme.b, this.theme.border, this.dims.border, this.dims.radius);
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
function NodeTheme(a="#6699FF",b="#ff9900", border="#333333", fg_a="#FFFFFF", fg_b="#000000"){
    this.a = a; //  Color of the pre-activation area.
    this.b = b; //  Color of the post-activation area.
    this.border= border;
    this.fg_a = fg_a; // Foreground Color for pre-activation area.
    this.fg_b = fg_b; // Foreground COlor for post-activation area

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

//var THEME_GREEN = new NodeTheme(a="#1BDA32",b="#C1F9C8", border="#36A944", fg_a="#FFFFFF", fg_b="#115019");
var THEME_GREEN = new NodeTheme(a="#28AE38",b="#C1F9C8", border="#009412", fg_a="#FFFFFF", fg_b="#176220");
var THEME_ORANGE = new NodeTheme(a="#FFA41F",b="#FFE8C6", border="#DD8B16", fg_a="#FFFFFF", fg_b="#813805");
var THEME_PURPLE = new NodeTheme(a="#552DCC",b="#D2C5F6", border="#30118C", fg_a="#FFFFFF", fg_b="#1E0469");
var THEME_BLUE = new NodeTheme(a="#5888ED",b="#AFC8FF", border="#2F6AE9", fg_a="#FFFFFF", fg_b="#021D54");
var THEME_TANGERINE = new NodeTheme(a="#FF4C00",b="#FF9A6F", border="#E24300", fg_a="#FFFFFF", fg_b="#3D1200");
var THEME_FUSCIA = new NodeTheme(a="#CF45D9",b="#F7B3FB", border="#CA22D5", fg_a="#FFFFFF", fg_b="#690B70");



var THEME_GREY_DARK = new NodeTheme(a="#424242",b="#848484", border="#333333", fg_a="#FFFFFF", fg_b="#222222");
var THEME_GREY_MED = new NodeTheme(a="#7E7E7E",b="#D4D4D4", border="#505050", fg_a="#FFFFFF", fg_b="#333333");
var THEME_GREY_LIGHT = new NodeTheme(a="#C6C6C6",b="#ECECEC", border="#7F7F7F", fg_a="#FFFFFF", fg_b="#333333");

var THEME_INPUT_GREY = new NodeTheme(a="#D4D4D4",b="#D4D4D4", border="#505050", fg_a="#333333", fg_b="#333333");





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


// color = in hexadecimal notation
function latexOnCanvas(context, latex, x, y, color="000000", size=10){
    var url = "http://latex.codecogs.com/png.latex?"
    var sizes= [];
    sizes[5] = "tiny"
    sizes[9] = "small"
    sizes[10] = ""
    sizes[12] = "large"
    sizes[18] = "LARGE"
    sizes[20] = "huge"

    color = color.replace("#", "");
    var colorCode = "\\fg_COLOR&space;".replace("COLOR", color);
    var sizeCode = "\\SIZE&space;".replace("SIZE", sizes[size]);

    // Put the pieces of the URL together.
    url += colorCode + sizeCode + latex;

    // render the result of the url on the canvas
    imageFromUrl(context, url, x, y);
}


function SciWeavers_latexOnCanvas(context, latex, x, y, color="Black", size=10){
    // Note it renders ugly and choppy.
    var url = "http://www.sciweavers.org/tex2img.php?eq="
    var more_settings = "&bc=Transparent&im=png&ff=fourier&edit=0"

    var colorCode = "&fc=" + color;
    //        "&fc=Orange"
    //          White
    var sizeCode = "&fs=" + size.toString();

    // Put the pieces of the URL together.
    url += latex + more_settings + colorCode + sizeCode;

    // render the result of the url on the canvas
    imageFromUrl(context, url, x, y);
}







