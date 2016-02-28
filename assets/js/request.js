var helloRequest = (function($){

  function handleRequest(data) {
    //console.log(data);
    var items = [];
    data = JSON.stringify(data);             
    var j_data = $.parseJSON(data);
    var id = j_data[0];
    $.each(j_data[1], function(i, val) {
        var req_class = '';
        if (parseInt(val.new_req) == 1){
            req_class = 'info';
        }
        items.push('<tr class="'+req_class+'">'
                    + '<td>' + val.path + '</td>'
                    + '<td>' + val.method + '</td>'
                    + '<td>' + val.req_date + '</td>'
                    + '</tr>'
        );
        
   });
   var title = $('title').text().split(')')[1] || $('title').text();
   var pre_titile = id ? '(' + id + ')' : '';
   $('#request').find('tbody').html(items);
   $('title').text(pre_titile + title);
}

 return {
     loadRequest: function(){
         $.ajax({
             url: '/requests_ajax/',
             dataType : "json",
             success: function (data, textStatus) {
                 handleRequest(data);
             }
         });
     }
 };
})(jQuery);


$(document).ready(function(){
    helloRequest.loadRequest();
    setInterval(helloRequest.loadRequest, 5000);
});
