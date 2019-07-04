script_storage_clear = "localStorage.clear();"
script_signin = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
script_customer_id = "return SO.model.Customer.getCustomerId();"
script_is_signed = "return SO.model.Customer.isLoggedIn();"
script_registration_step = "return SO.model.Customer.currentCustomer.registrationStep"
script_input_val = '''return $("input[name='phonePrefix']").val();'''
script_checklist = '''var mySelect = $('select[id^=countryOfTaxPlatformSelect_]'); mySelect.val(mySelect.find('option:contains("Yes")').attr("value")); mySelect.trigger("liszt:updated");'''
script_checklist2 = '''var mySelect2 = $('select[id^=main_trading_purposePlatformSelect_]'); mySelect2.val(mySelect2.find('option:contains("Intraday")').attr("value")); mySelect2.trigger("liszt:updated");'''

checklist = '''
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
'''
