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

    console.log(responseJSON);

});

