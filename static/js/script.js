$("[name='soundstoggle']").bootstrapSwitch();
function updateTimeProgress(time)   {
    if(time >= time_progress.attr("aria-valuemin") && time <= time_progress.attr("aria-valuemax"))
        time_progress.css('width', time+'%').attr('aria-valuenow', time);
}
var time_progress = $("#time-progress");
var time = 0;
var last_id = 0;
var time = parseInt(time_progress.attr('aria-valuenow'));
updateTimeProgress();
var con_issues = $("#con-issues");

function handleResponse(ajax)   {

}

$(".btn").click(function(event){
    this.blur();
    $.get(
      "/btn_click",
      {
        id: event.target.id.replace(/^btn-/, '')
      }
    )
    .success(handleResponse)
    .error(function() {
        if(!con_issues.hasClass("hidden")){
            con_issues.addClass("hidden");
        }
    })
});

function poll() {

$.ajax({
    url:"/poll?last_id="+last_id,
    timeout: 60000,
    success: function(data) {
        var jdata = JSON.parse(data);
        console.log(jdata);
        last_id = jdata.last_id;


        poll()
    },
    error: function(jqXHR, textStatus, errorThrown) {

        console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);

        setTimeout(poll, 3000);

    }
});

}

poll();