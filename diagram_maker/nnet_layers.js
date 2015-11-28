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
