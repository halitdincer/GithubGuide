//TODO: this is a placeholder data, this data will be requested from the server
var sample_raw_data = ["Description for first row item",
   "Description for second row item",
   "Description for third row item",
   "Description for fourth row item"] ;

var intervalId = window.setInterval(function(){
   
   if (!$(".repo-explainer-grid").length){

   // Slice the last part of the current url
   var url_ext = document.location.href.slice(19) ;

   // Make api call to server with url extension
   $.ajax({
      type: 'GET',
      // TODO: this is a placeholder url, replace with actual one
      url: 'https://raw.githubusercontent.com/pandas-dev/pandas/main/scripts/check_test_naming.py',
      data: $.param({'url_ext' : url_ext }),

      // On call success
      success: function(resp){

         // Iterate through each box-row in files
         $("[aria-labelledby='files']").children('.Box-row').each(function (index) {

            if(typeof sample_raw_data[index] === 'undefined') {
               // if it does not exist, do nothing
           }
           else {
               // if it does exist, append 'Detail' element with description
               $(this).append("<div role='gridcell' class='repo-explainer-grid' >  \
               <span class='repo-explainer-link'> [Info] </span> \
               <span class='repo-explainer-hover-text'>" + sample_raw_data[index]  +"</span> </div>");
           }

         });
      },
      // On call error
      error: function(resp){
         console.error(resp);
      }
   });

   }


}, 1000);



// NOTE: sample ajax call to openAI directly, do not remove it till demo since it could be useful later
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