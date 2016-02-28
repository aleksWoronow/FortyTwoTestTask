var helloRequest = (function($){

  function handleRequest(data) {

    var items = [];
    var j_data = $.parseJSON(data[1]);
    var id = data[0];

    $.each(j_data, function(i, val) {
        var req_class = 'old';
        if (parseInt(val.fields.new_request, 10) == 1){
            req_class = 'info';
        }
        items.push('<tr class="' + req_class + '">'
                    + '<td>' + val.fields.path + '</td>'
                    + '<td>' + val.fields.method + '</td>'
                    + '<td>' + val.fields.date + '</td>'
                    + '</tr>'
        );
        
   });
   var title = $('title').text().split(')')[1] || $('title').text();
   var pre_titile = id ? '(' + id + ')' : '';
   $('#request').find('tbody').html(items);
   $('td').attr('align', 'center');
   $('title').text(pre_titile + title);
}

 return {
     loadRequest: function(){
         $.ajax({
            url: '/requests_ajax/',
            dataType : "json",
            success: function(data, textStatus) {
                handleRequest(data);
            },
            error: function(jqXHR) {
                console.log(jqXHR.responseText);
            }
         });
     }
 };
})(jQuery);


$(document).ready(function(){
    helloRequest.loadRequest();
    setInterval(helloRequest.loadRequest, 500);
});
