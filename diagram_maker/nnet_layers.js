// #############################################################################
//                                                         LAYER OF NODES OBJECT
// #############################################################################
// n = number of nodes for this layer
// n_in = number of input connections for each node
// n_out = number of output connections for each node
// dims = a dimension object
// themes = an array of themes, one for each node in the layer.
// space = vertical space between nodes.
// =============================================================================
function LayerOfNodes(x,y, n, dims=dims1, themes=theme1, n_in=1, n_out=1, space=10){
    this.x = x;
    this.y = y;
    this.n = n;
    this.dims = dims;
    this.themes = themes;
    this.space = space;  // Vertical Space between nodes.

    // If the themes passed in is not an array of themes, then it creates
    // an array populating it with the same theme.
    if (!Array.isArray(themes)){
        this.themes = new Array(n);
        this.themes.fill(themes);
    }
    // CALCULATE Y POSITION OF NODES
    var layer_ys = layer_nodes_y(this.n, this.dims.height, this.space, this.y);

    // CREATE NODES
    this.nodes = new Array(n);
    for (i = 0; i < this.n; i++) {
        this.nodes[i] = new Node(x, layer_ys[i], dims=this.dims, theme=this.themes[i], n_in, n_out);
    }

    // DRAW METHOD
    this.draw = function (ctx) {
        for (i = 0; i < this.n; i++) {
            this.nodes[i].draw(ctx);
        }
    }

    // =========================================================================
    //                                                     FORWARD_CONNECTIONS()
    // =========================================================================
    // colors = If a string is used. All connections will be same color.
    //          If an array is used, it should be same size as the number of
    //          elements in target layer, representing colors for each cluster
    //          of lines connecting to each target node.
    //
    // size = thickness of the connection lines
    // d = How far the control point should stick out relative to the starting
    //     position.
    // d2 = as per d, but relative to the end point.
    //
    // use_wa = Use evenly distributed weight connections along the side face of
    //          the starting node?
    // use_wb = Use evenly distributed weight connections along the side face of
    //          the target node?
    // alpha = alpha of the connection lines
    // =========================================================================
    this.forward_connections = function (ctx, next_layer, colors="#AAAAAA", size=3, d=100, d2=100, use_wa=false, use_wb=false, alpha=0.3){
        // TODO: give option to skip connecting to the first node in the target (Bias Node)

        if (!Array.isArray(colors)){
            var cols = new Array(next_layer.n);
            cols.fill(colors);
            colors = cols;
        }

        // handle position of nodes along side face of each node
        var wa = -1;
        var wb = -1;

        for (var i = 0; i < next_layer.n; i++){
            to_node = next_layer.nodes[i];
            for (var j = 0; j < this.n; j++){
                from_node = this.nodes[j]

                // handle psoition along side edges the nodes
                if (use_wa){wa = i}; // Index of connection on edge of from_node
                if (use_wb){wb = j}; // Index of connection on edge of to_node

                from_node.connect_to(ctx, to_node, wa=wa, wb=wb, color=colors[i] ,size, d, d2, alpha);
            }
        }

    }



}



// #############################################################################
//                                                         LAYER NODES Y OFFSETS
// #############################################################################
// y = y offset for this layer
function layer_nodes_y(n, height, space, y=0){
    var ys = new Array(n);
    for (i = 0; i < n; i++) {
        if (i == 0){
            ys[i] = y;
        } else {
            ys[i] = y + i* (height + space);
        };
    };
    return ys;
}





// Get the starting y values for two subsequent layers
// y position for the whole thing
// na = number of nodes in layer a
// nb = number of nodes in layer b
//function get_start_ys(y, na, nb, spacing){
//    if (na > nb){
//        start_y =
//    }
//}
