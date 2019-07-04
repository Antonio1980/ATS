var steps = $(".dynamicQuestionsContainer.regulationSteps .stepContainer");

var questions = $(steps[0]).find(".dynamicFieldsList tr");

for (var i = 0; i < questions.length; i++){
    var currQuestion = $(questions[i]), visible = currQuestion.is(":visible");

    if (visible) {
    	var selectEl = currQuestion.find("select");

		if (selectEl.length > 0){
			selectEl.val(selectEl.find('option[value!=""]').attr("value")).trigger('change').trigger("liszt:updated");
			continue;
		}

		var inputEl = currQuestion.find("input");

		if (inputEl.length > 0){
			inputEl.val('Some random value');
			continue;
		}
    }
}