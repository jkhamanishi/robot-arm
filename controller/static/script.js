const buttons = {
    "grippers": ["open", "close"],
    "wrist": ["up", "down"],
    "elbow": ["up", "down"],
    "shoulder": ["up", "down"],
    "base": ["ccw", "cw"],
    "stop": ["all"]
};

const layouts = ["portrait", "landscape"];

$(document).ready(() => {
    Object.entries(buttons).forEach(([actuator, directions]) => {
        directions.forEach(direction => layouts.forEach(layout => {
            const buttonID = `${actuator}-${direction}-btn-${layout}`;
            $("#"+buttonID).on("mousedown mouseup touchstart touchend", buttonHandler);
        }));
    });
    layouts.forEach(layout => $(`#led-btn-${layout}`).on("click", switchHandler));
});

function buttonHandler(e){
    e.preventDefault();
    let actuator = "STOP";
    let direction = "MOTORS";
    let toggle = "OFF";
    switch (e.type) {
        case "mousedown":
        case "touchstart":
            toggle = "ON";
        case "touchend":
            const buttonDetails = e.currentTarget.id.split("-");
            actuator = buttonDetails[0].toUpperCase();
            direction = buttonDetails[1].toUpperCase();
            if (actuator == "STOP") {
                setLEDCheckboxes(false);
            }
            break;
        case "mouseup":
            break;
    }
    const message = {
        'actuator': actuator,
        'direction': direction,
        'toggle': toggle
    };
    $.post('/move', message);
};

function switchHandler(e){
    e.preventDefault
    const isChecked = e.currentTarget.checked;
    setLEDCheckboxes(isChecked);
    const message = {
        'actuator': "LED",
        'direction': "ON",
        'toggle': isChecked ? "ON" : "OFF"
    };
    $.post('/move', message);
}

function setLEDCheckboxes(checked){
    layouts.forEach(layout => $(`#led-btn-${layout}`).prop('checked', checked));
}