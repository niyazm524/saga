function sendAjax(url, id, data)    {
    $.get(
      url,
      {
        "id": id,
        "data": data
      }
    )
    .error(function() {
        console.log("Error")
    })
}

$('#main').change(function() {
  sendAjax("/btn_click", "power-main", $(this).prop('checked'));
  $(this).bootstrapToggle("disable");
  if($("#main").prop('checked') != true && $("#trunks").prop('checked') != true && $("#horns").prop('checked') != true)
    $("#all").bootstrapToggle('off');
})

$('#trunks').change(function() {
  sendAjax("/btn_click", "power-trunks", $(this).prop('checked'));
  $(this).bootstrapToggle("disable");
})

$('#horns').change(function() {
  sendAjax("/btn_click", "power-horns", $(this).prop('checked'));
  $(this).bootstrapToggle("disable");
})

$('#all').change(function() {
    if($("#horns").prop('checked'))  {
        sendAjax("/btn_click", "power-horns", false);
        $("#horns").bootstrapToggle('off');
    }

    if($("#trunks").prop('checked'))  {
        sendAjax("/btn_click", "power-trunks", false);
        $("#trunks").bootstrapToggle('off');
    }
    setTimeout(function() {
        if($("#main").prop('checked'))  {
            sendAjax("/btn_click", "power-main", false);
            $("#main").bootstrapToggle('off');
        }
    }, 2000);

})

