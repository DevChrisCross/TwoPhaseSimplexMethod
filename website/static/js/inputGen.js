$("#constBtn").click(function(){
    var num_variables = parseInt($("#variables").val());
    var num_constraints = parseInt($("#constraints").val());

    /*manual filter does not work*/
    if (num_variables > 11){ num_variables = 10; }
    if (num_variables < 2){ num_variables = 2; }
    if (num_constraints > 11){ num_constraints = 10; }
    if (num_constraints < 2){ num_variables = 2; }
    $("#variables").val(num_variables.toString());
    $("#constraints").val(num_constraints.toString());

    num_variables += 1;
    num_constraints += 1;
    var html_content = "";
    html_content += '<div class="row" style="justify-content: center; width: 100%;">';
    html_content += '<div class="col-md" style="margin-left: 14%;">';
    html_content += '<span style="display: inline-block; width: 85px; margin: 5px; "><i>Constant <strong>C</strong></i></span>';
    for (i = 0; i < num_variables - 1; i++){
        html_content += '<span style="display: inline-block; width: 56px; margin: 5px;">x<sub>' + (i+1) + '</sub></span>'
    }
    html_content += '</div></div>';

    for (i = 0; i < num_constraints; i++){
        html_content += '<div class="row" style="justify-content: center; width: 100%;">';
        html_content += '<div class="col-md">';
        if (i == 0) { html_content += "<span class='left-label'>Objective function <i>f</i></span>"; }
        else { html_content += "<span class='left-label'>Constraint <i>c<sub>" + i + "</sub></i></span>"; }
        for (j = 0; j < num_variables; j++){
            var style = '';
            var inputName = 'name="matrix' + i.toString() + j.toString() + '"';
            if (j == 0) { style = 'style="width: 85px;"'; }
            html_content += '<input type="number" value="0" class="matrix-element"'+ style + inputName + '>';
        }
        html_content += '</div></div>'
    }

    $("#matrix-form").html(html_content);
});

$("#computeBtn").click(function () {
   //code goes here
});

$("#constBtn").trigger("click");

