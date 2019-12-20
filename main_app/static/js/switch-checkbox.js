$(".check-box").on('change', function(e) {
  var this_=$(this);
  var value = this_.is(':checked');
  var id = this_.data("id");
  var url = this_.data("url");

  status=value==true?1:0;
  var data = {
    "id": id,
    "status": status,
  };

  $.ajax({
    url: url,
    data: data,
    dataType:'json',
    type:"POST",
    success: function(ret) {
       if (ret.code == 1001){
         console.log('成功');
       }else{
        console.log('失败');
       }

    },
    error: function(ret) {
        console.log(ret);
        console.log('失败');
    }
  });
});
