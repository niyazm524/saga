$("[name='soundstoggle']").bootstrapSwitch();
function updateTimeProgress(time)   {
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

