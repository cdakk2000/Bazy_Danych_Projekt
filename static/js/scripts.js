// $(document).ready(function() {
//     $("#phone1_brand").change(function() {
//         var mark_id = $(this).val();
//         $.ajax({
//             url: '/models_brand_view/',
//             data: {
//                 'mark_id': mark_id
//             },
//             success: function(data) {
//                 $("#phone1_model").html(data);
//             }
//         });
//     });
// });

// document.getElementById("phone1_brand").addEventListener("change", function(){
//     document.getElementById("phone1_model").innerHTML = "";
//     $.ajax({
//         type: 'GET',
//         url: "get-models/",
//         data: {
//             phone1_brand: $("#d_phone1_brand").val(),
//         },
//         dataType: 'json',
//         success:function(response){
//             var select = document.getElementById("phone1_model");
//             for (var i=0; i<response.json_models.length; i++)
//             {
//                 var option = document.createElement("option");
//                 option.value = response.json_models[i]["Models_Name"];
//                 option.innerHTML = response.json_models[i]["Models_Name"];
//                 select.appendChild(option);
//             }
//         }
//     })
// })

$(document).ready(function(){
    console.log("jestem w funkcji")
    $("#phone1_brand-selector").change(function(){
        var brandId = $(this).val();
        console.log(brandId)
        $.post("/porownywarka/", {brand_id: brandId}, function(data){
            var modelSelect = $("#phone1_model");
            modelSelect.empty();
            data.models.forEach(function(model){
                modelSelect.append($("<option>").val(model.id).text(model.name));
            });
        });
    });
});

console.log("jestem poza funckja")