$( document ).ready(function() {

   $("[aria-labelledby='files']").children('.Box-row').each(function () {

      //alert($(this).find(".Link--primary").text());
      $(this).append("<div role='gridcell' class='repo-explainer-grid' >  \
         <span class='repo-explainer-link'> Detail </span> \
         <span class='repo-explainer-hover-text'>" + "Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem" +"</span> </div>");

   });

   var url_ext = document.location.href.slice(19) ;

  $.ajax({
      type: 'GET',
      url: 'https://raw.githubusercontent.com/pandas-dev/pandas/main/scripts/check_test_naming.py',
      processData: false,
      data: $.param({'url_ext' : url_ext }),
      success: function(resp){

 
      }
   });




});

// var chat_data = JSON.stringify({
//    "model": "gpt-3.5-turbo",
//    "messages": [{"role": "system","content": "If given code, you will return an explanation of what the code does, what each function does and what it returns in the following JSON format: {['functionX' : [ Write explanation of functionX here as string, Write a shorter summary explanation of functionX here as string]] }"},
//       {"role": "user","content": resp}]
// })

// $.ajax({
//    url: "https://api.openai.com/v1/chat/completions",
//    method: "POST",
//    headers: {
//    "Content-Type": "application/json",
//    "Authorization": "Bearer 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"
//    },
//    data: chat_data
// }).done(function(response) {
//    // Handle the response from the API
//    console.log(response);
//    alert(response["choices"][0]["message"]["content"]);
// }).fail(function(jqXHR, textStatus, errorThrown) {
//    // Handle any errors that occur during the AJAX request
//    console.error("Error making AJAX request: " + textStatus + " - " + errorThrown);
// });