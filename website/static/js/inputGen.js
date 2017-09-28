(function () {
    var generateButton = $("#constBtn");
    var computeButton = $("#computeBtn");
    var variables = $("#variables");
    var constraints = $("#constraints");
    var matrixForm = $("#matrix-form");
    var resultPanel = $("#result-panel");
    var matrixOutputData;

    generateButton.click(function(){
        var num_variables = parseInt(variables.val());
        var num_constraints = parseInt(constraints.val());

        /*manual filter does not work*/
        if (num_variables > 11){ num_variables = 10; }
        if (num_variables < 2){ num_variables = 2; }
        if (num_constraints > 11){ num_constraints = 10; }
        if (num_constraints < 2){ num_variables = 2; }
        variables.val(num_variables.toString());
        constraints.val(num_constraints.toString());

        num_variables += 1;
        num_constraints += 1;
        var html_content = "";
        html_content += '<div class="row" style="justify-content: center; width: 100%;">';
        html_content += '<div class="col-md" style="margin-left: 14%;">';
        html_content += '<span style="display: inline-block; width: 85px; margin: 5px; "><i>Constant <strong>C</strong></i></span>';
        for (var i = 0; i < num_variables - 1; i++){
            html_content += '<span style="display: inline-block; width: 56px; margin: 5px;">x<sub>' + (i+1) + '</sub></span>'
        }
        html_content += '</div></div>';

        for (var i = 0; i < num_constraints; i++){
            html_content += '<div class="row" style="justify-content: center; width: 100%;">';
            html_content += '<div class="col-md">';
            if (i == 0) { html_content += "<span class='left-label'>Objective function <i>f</i></span>"; }
            else { html_content += "<span class='left-label'>Constraint <i>c<sub>" + i + "</sub></i></span>"; }
            for (var j = 0; j < num_variables; j++){
                var style = '';
                var inputName = 'name="matrix' + i.toString() + j.toString() + '"';
                if (j == 0) { style = 'style="width: 85px;"'; }
                html_content += '<input type="number" value="0" class="matrix-element"'+ style + inputName + '>';
            }
            html_content += '</div></div>'
        }

        matrixForm.html(html_content);
    });

    computeButton.click(function () {
        var num_variables = parseInt(variables.val()) + 1;
        var num_constraints = parseInt(constraints.val()) + 1;
        var matrix = [];
        console.log("test", num_variables, num_constraints);

        for (var i = 0; i < num_constraints; i++){
            var equation = [];
            var constantValue = "";
            for (var j = 0; j < num_variables; j++){
                var inputName = 'input[name="matrix' + i.toString() + j.toString() + '"]';
                if (j == 0) { constantValue = $(inputName).val(); continue;}
                equation.push($(inputName).val());
            }equation.push(constantValue);
            matrix.push(equation);
        }

        $.ajax({
            type: "GET",
            url: "/process/",
            data: {
                matrix: JSON.stringify(matrix),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (response) {
                alert(response);
                console.log(response);
//                matrixOutputData = response;
                response = response["outputMatrix"];
                var matrix = response["matrix"];
                var solutionSet = response["solutionSet"];
                var solutionValue = response["solutionValue"];
                var resultHtmlContent = "";

                for (var i = 0; i < matrix.length; i++){
                    resultHtmlContent += '<div class="row"><div class="col-md">';
                    for (var j = 0; j < matrix[i].length; j++){
                        resultHtmlContent += '<span style="display: inline-block; margin: 5px;">' + matrix[i][j] +'</span>'
                    }
                    resultHtmlContent += '</div></div>';
                }
                resultHtmlContent += '<div class="row"><div class="col-md">[';
                for (var i = 0; i < solutionSet.length; i++){
                    resultHtmlContent += '<span style="display: inline-block; margin: 5px;">' + solutionSet[i] + '</span>';
                }
                resultHtmlContent += '] = ' + solutionValue + '</div></div>';



                resultPanel.html(resultHtmlContent);
            }
        });
    });

    generateButton.trigger("click");
    computeButton.trigger("click");
})();



