"use strict;"

async function displayCupcakes(searchTerm) {

    let $cupcakeList = $("#cupcakeList");
    $cupcakeList.empty();

    let response = await axios.get("/api/cupcakes/");

    for (let cupcake of response.data){
        let $newLi = $("<li>");
        $newLi.html(cupcake);
        $cupcakeList.append($newLi)
    }

}