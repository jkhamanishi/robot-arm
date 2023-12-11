const buttons = {
    "grippers": ["open", "close"],
    "wrist": ["up", "down"],
    "elbow": ["up", "down"],
    "shoulder": ["up", "down"],
    "base": ["ccw", "cw"],
    "stop": ["all"]
};

$(document).ready(() => {
    Object.entries(buttons).forEach(([actuator, directions]) => {
        directions.forEach(direction => {
            const buttonID = `${actuator}-${direction}-btn`;
            $("#"+buttonID).on("mousedown mouseup touchstart touchend", buttonHandler);
        });
    });
    $("#led-btn").on("click", switchHandler);
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
                $("#led-btn").prop('checked', false)
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
    const message = {
        'actuator': "LED",
        'direction': "ON",
        'toggle': isChecked ? "ON" : "OFF"
    };
    $.post('/move', message);
}
