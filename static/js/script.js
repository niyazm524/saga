String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}
$("#soundstoggle").bootstrapToggle();
$("#soundstoggle").change(function soundtoggled() {
    vol_slider.bootstrapSlider('setValue', $(this).prop("checked") ? prev_volume : 0);
    sendAjax("/btn_click", "volume", $(this).prop("checked") ? prev_volume : 0);
});
$("#soundstoggle-bg").bootstrapToggle();
$("#soundstoggle-bg").change(function soundtoggled() {
    vol_slider_bg.bootstrapSlider('setValue', $(this).prop("checked") ? prev_volume_bg : 0);
    sendAjax("/btn_click", "volume_bg", $(this).prop("checked") ? prev_volume_bg : 0);
});

var vol_slider = $('#volume-slider').bootstrapSlider({
	formatter: function(value) {
		return value.toString() + "%";
	}
});
var vol_slider_bg = $('#volume-slider-bg').bootstrapSlider({
	formatter: function(value) {
		return value.toString() + "%";
	}
});
var vol_slider_bg_nav = $('#volume-slider-bg-nav').bootstrapSlider({
	formatter: function(value) {
		return value.toString() + "%";
	}
});

var time_progress = $("#time-progress");
var ftime_progress = $("#ftime-progress");
var in_process = $("#btn-start").hasClass("active");
var pb_time = $("#pb-time-progress");
var last_id = 0;
var altars = $(".btn-altar");
var prev_volume = vol_slider.bootstrapSlider('getValue');
var prev_volume_bg = vol_slider_bg.bootstrapSlider('getValue');
var ftime = parseInt(ftime_progress.text(), 10);
var time = parseInt(time_progress.text(), 10);
$("#aroprogress").css("width", (parseInt($("#arotext").text(), 10)/50*100).toString()+"%");



function onSlideStop(val)   {
    prev_volume = val.value;

    sendAjax("/btn_click", "volume", val.value.toString());
}
vol_slider.on("slideStop", onSlideStop);
function onSlideStop_bg(val)   {
    prev_volume_bg = val.value;
    sendAjax("/btn_click", "volume_bg", val.value.toString());
}
vol_slider_bg.on("slideStop", onSlideStop_bg);
vol_slider_bg_nav.on("slideStop", onSlideStop_bg);
function updateTimeProgress()   {
    ftime_progress.text((ftime).toString().toHHMMSS());
    time_progress.text(time.toString().toHHMMSS());
    pb_time.css('width', (time/ftime*100).toString()+'%');
    $("#time-progress-nav").text(time.toString().toHHMMSS());
    $("#pb-time-progress-nav").css('width', (time/ftime*100).toString()+'%');
}
updateTimeProgress();

function time_handle()  {
    if(in_process) {
        time += 1;
        updateTimeProgress();
    }
}


setInterval(time_handle, 1000);

var con_issues = $("#con-issues");

function handleResponse(ajax)   {
    if(!con_issues.hasClass("hidden")){
        con_issues.addClass("hidden");
    }
}

$(":button").click(function(event){
    this.blur();
    sendAjax("/btn_click", this.id.replace(/(^btn-)|(-nav$)/g, ''), null);
});

altars.click(function(){

    for(var i = 0; i < altars.length; i++)  {
        if(altars.eq(i).hasClass("active"))    {
            if(altars[i] == this)   {
                sendAjax("/btn_click", "altars", "0");
                return;
            }
            else {
                sendAjax("/btn_click", "altars", ($(this).index()+1).toString());
                return;
            }
        }
    }
    sendAjax("/btn_click", "altars", ($(this).index()+1).toString());
});

$(".door").click(function() {
    var regex = this.id.match(/([^-]+)-(.+)/);
    sendAjax("/btn-door", regex[1], regex[2]);
});
$(".hint").click(function() {
    sendAjax("/btn-hint", this.id.slice(5), null);
});
$(".actlink").click(function() {
    sendAjax("/btn-actlink", this.id, null);
});

//$(".navbar-toggle").click(function() {
//    if(!$(this).hasClass("collapsed"))
//        $("body").css("padding-top", "70px");
//    else {
//        $("body").css("padding-top", "320px");
//    }
//});

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
    timeout: 65000,
    success: function(data) {
        if(!con_issues.hasClass("hidden")){
            con_issues.addClass("hidden");
        }


        var jdata = JSON.parse(data);
        //console.log(jdata);
        last_id = jdata.last_id;
        if('time' in jdata) {
            time = jdata.time;
            updateTimeProgress();
        }
        if('in_process' in jdata) {
            in_process = jdata.in_process;
            updateTimeProgress();
        }
        if('events' in jdata)   {
            for(var i = 0; i < jdata.events.length; i++)    {
                var event = jdata.events[i];
                if(event.event_type == 3)  {
                    in_process = true;
                    if(!$("#btn-start").hasClass("active")){
                        $("#btn-start").addClass("active");
                    }
                }
                else if(event.event_type == 4) {
                    in_process = false;
                    if($("#btn-start").hasClass("active")){
                        $("#btn-start").removeClass("active");
                    }

                }
                else if(event.event_type == 5) {
                    in_process = false;
                    if(!$("#btn-reload").hasClass("active")){
                        $("#btn-reload").addClass("active");
                    }
                    if($("#btn-start").hasClass("active")){
                        $("#btn-start").removeClass("active");
                    }
                }
                else if(event.event_type == 10) {
                    ftime = event.event_data*60;
                    updateTimeProgress();
                }
                else if(event.event_type == 11) {
                    vol_slider.bootstrapSlider('setValue', event.event_data);
                    if(event.event_data == 0)
                        $("#soundstoggle").prop('checked', false);
                    else if(!$("#soundstoggle").prop('checked'))
                        $("#soundstoggle").prop('checked', true);
                }
                else if(event.event_type == 12) {
                    $(".btn-altar").removeClass("active");
                    if(event.event_data != 0)
                        $(".btn-altar").eq(event.event_data-1).addClass("active");
                }
                else if(event.event_type == 13) {
                    $("#arotext").text(event.event_data);
                    $("#aroprogress").css("width", (event.event_data/50*100).toString()+"%");
                    $("#arotext-nav").text(event.event_data);
                }
                else if(event.event_type == 16) {
                    if($("#btn-reload").hasClass("active")){
                        $("#btn-reload").removeClass("active");
                    }
                }
                else if(event.event_type == 17) {
                    vol_slider_bg.bootstrapSlider('setValue', event.event_data);
                    vol_slider_bg_nav.bootstrapSlider('setValue', event.event_data);
                    if(event.event_data == 0)
                        $("#soundstoggle-bg").prop('checked', false);
                    else if(!$("#soundstoggle-bg").prop('checked'))
                        $("#soundstoggle-bg").prop('checked', true);
                }
            }
        }

        poll();
    },
    error: function(jqXHR, textStatus, errorThrown) {
        if(textStatus !== "timeout")    {
            if(con_issues.hasClass("hidden")){
                con_issues.removeClass("hidden");
            }

            setTimeout(poll, 3000);
        } else poll();
    }
});

}

poll();