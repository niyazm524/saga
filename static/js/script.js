$("[name='soundstoggle']").bootstrapSwitch();
function updateTimeProgress(time)   {
    if(time )
    time_progress.css('width', time+'%').attr('aria-valuenow', time);
}
var time_progress = $("#time-progress");
var time = 0;
time = parseInt(time_progress.attr('aria-valuenow'));
updateTimeProgress();
$("#time-reduce").click(function(){
    time -= 5;
    updateTimeProgress(time);
});
$("#time-add").click(function(){
    time += 5;
    updateTimeProgress(time);
});
$(".btn").click(function(event){
    this.blur();
    $.get(
      "/btn_click",
      {
        id: event.target.id.replace(/^button-/, '')
      }
    )
    .success(function(res) {
        if(res != "ok" && !$(event.target).hasClass("btn-warning")){
            $(event.target).addClass("btn-warning");
        }
    })
    .error(function() {
        if(!$(event.target).hasClass("btn-warning")){
            $(event.target).addClass("btn-warning");
        }
    })
});