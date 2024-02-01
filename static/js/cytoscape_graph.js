const clientForm = document.querySelector('#TraversalForm');

clientForm.addEventListener('submit', async event => {
    event.preventDefault();

    // get values from form by NAMEs of inputs
    const clientFormData = new FormData(clientForm)
    const searchID = document.querySelector('input[name="options-id"]:checked').id;
    clientFormData.append('searchID', searchID);

    const clientData = Object.fromEntries(clientFormData)

    console.log(JSON.stringify(clientData))

    // don't forget the headers for pydantic parser
    let response = await fetch(`${window.origin}/get_graph`, {
        method: 'POST',
        body: JSON.stringify(clientData),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });

    let responseJSON = await response.json()

    // check if user exists in vertices
    if(Object.keys(responseJSON).length === 0){
        console.log("no data found");
        // turn on alert
        document.querySelector("#alertMessage").style.display = 'block';
    } else {
        // turn off alert
        document.querySelector("#alertMessage").style.display = 'none';
    }

    // console.log(responseJSON);

    for (let i = 0, n = responseJSON.nodes.length, node; i < n; ++i) {
        node = responseJSON.nodes[i];
        node.data.id = node.data._id;

        if (node.data._key === clientData.idField) {
            node.classes = ['root']
        }

        if (node.data.block_status === 1){
            node.data.color = "#CB4154"
        } else {
            node.data.color = "#69b3a2";
        }
        node.data.label = node.data._key;
    }

    for (let i = 0, e = responseJSON.edges.length, edge; i < e; ++i) {
        edge = responseJSON.edges[i];
        edge.data.label = edge.data.amount.toString();
		edge.data.lineColor = "#A9A9A9";
    }

    let cy = window.cy = cytoscape({
        container: document.getElementById('graph-container'),
        layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeOverlap: 20,
            refresh: 20,
            fit: true,
            padding: 30,
            randomize: false,
            componentSpacing: 100,
            nodeRepulsion: 400000,
            edgeElasticity: 100,
            nestingFactor: 5,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        },
        elements: responseJSON,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'width': function(n) { return 10 * Math.pow(n.degree(), 0.4); },
                    'height': function(n) { return 10 * Math.pow(n.degree(), 0.4); }
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': function(n) {
                        return Math.min(
                            Math.ceil(0.001 * Math.pow(n.data('amount'), 0.42)),
                            15);
                        },
                    'label': 'data(label)',
                    'line-color': '#A9A9A9',
                    'target-arrow-color': '#A9A9A9',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: 'node.root',
                style: {
                    'border-color': '#0099CC',
                    'border-width': '5px'
                }
            },
            {
                selector: 'node.highlight',
                style: {
                    'border-color': '#FFF',
                    'border-width': '2px'
                }
            },
            {
                selector: 'node.semitransp',
                style: { 'opacity': '0.2' }
            },
            {
                selector: 'edge.highlight',
                style: { 'mid-target-arrow-color': '#FFF' }
            },
            {
                selector: 'edge.semitransp',
                style: { 'opacity': '0.2' }
            }
            ],
    })

    // draw only vertex neighbours on click
    cy.bind('dblclick', 'node', function(evt) {
        let sel = evt.target;
        cy.elements().difference(sel.neighborhood()).not(sel).hide();
    });

    // draw all graph on lhs + rhs mouse buttons
    cy.bind('cxttap', function(evt) {
        cy.elements().show();
    });

    // show vertex neighbours on vertex hover
    cy.on('mouseover', 'node', function(e) {
        let sel = e.target;
        cy.elements().difference(sel.neighborhood()).not(sel).addClass('semitransp');
        sel.addClass('highlight').neighborhood().addClass('highlight');
    });

    // rollback vertex hover
    cy.on('mouseout', 'node', function(e) {
        let sel = e.target;
        cy.elements().removeClass('semitransp');
        sel.removeClass('highlight').neighborhood().removeClass('highlight');
    });

});

