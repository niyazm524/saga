$("#soundstoggle").bootstrapSwitch();
function soundtoggled() {
    console.log("change");
    sendAjax("btn_click", "soundstoggle", $(this).prop("checked") ? "true" : "false");
}

function updateTimeProgress(time)   {
    if(time >= time_progress.attr("aria-valuemin") && time <= time_progress.attr("aria-valuemax"))
        time_progress.css('width', time+'%').attr('aria-valuenow', time);
}
var time_progress = $("#time-progress");
var time = 0;
var last_id = 0;
var ftime = $("#ftime");
var time = parseInt(time_progress.attr('aria-valuenow'));
updateTimeProgress();
var con_issues = $("#con-issues");

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10) * 60; // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}

function handleResponse(ajax)   {

}

function updateFTime(new_time)  {
    ftime.text(new_time.toString().toHHMMSS());
}

$(":button").click(function(event){
    this.blur();
    sendAjax("/btn_click", this.id.replace(/^btn-/, ''), null);
});

function sendAjax(url, id, data)    {
    $.get(
      url,
      {
        "id": id,
        "data": data
      }
    )
    .success(handleResponse)
    .error(function() {
        if(con_issues.hasClass("hidden")){
            con_issues.removeClass("hidden");
        }
    })
}

function poll() {

$.ajax({
    url:"/poll?last_id="+last_id,
    timeout: 60000,
    success: function(data) {
        if(!con_issues.hasClass("hidden")){
            con_issues.addClass("hidden");
        }


        var jdata = JSON.parse(data);
        console.log(jdata);
        last_id = jdata.last_id;
        if('events' in jdata)   {
            for(var i = 0; i < jdata.events.length; i++)    {
                var event = jdata.events[i];
                if(event.event_type == 10)
                    updateFTime(event.event_data)
            }
        }

        poll()
    },
    error: function(jqXHR, textStatus, errorThrown) {
        if(textStatus !== "timeout")    {
            if(con_issues.hasClass("hidden")){
                con_issues.removeClass("hidden");
            }

            setTimeout(poll, 3000);
        } else poll(l)
    }
});

}

poll();