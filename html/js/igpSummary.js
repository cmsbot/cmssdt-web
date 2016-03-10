
$("#errInfo").ajaxError(function(event, XMLHttpRequest, ajaxOptions, thrownError) {
$(this).text("error from ajax: "+thrownError
);
});

function numFmt(number) {
    var strNum = number+"";
    var len = strNum.length;
    var newNum = "";
    for (k=0; k<len; k++) {
	var i = len-k;
	if ( (k>0) && ((len-i)%3 == 0) ) {
	    newNum = "'"+newNum;
	}
	newNum = strNum.substring(i-1,i) + newNum;
    }
    return newNum;
}

function navsum(data) {      
      if (data.size<1) {
	var notAvail = "not (yet) available";
	var newListItem = "<td> ";
	for (i=0; i<4; i++) {
	   newListItem += "</td><td>"+notAvail
	}
	newListItem += "</td>"
	    $("<tr/>").html(newListItem).addClass(rowType).appendTo(".navSumm");
	return;
      }
      for (i=0; i<data.size; i++) {
            var results  = data.results[i];
	    if ( (i%2) == 0 ) {
	        var rowType="even";
	    }else{
	        var rowType="odd";
	    }
	    var newListItem = "<td>"+results[0]+
                  "</td><td>"+results[1][0]+ "<br/>("+results[1][1]+")"+
		  "</td><td>"+numFmt(results[1][2])+ "<br/>("+numFmt(results[1][3])+")"+
		  "</td><td>"+numFmt(results[1][4])+ "<br/>("+numFmt(results[1][5])+")"+
                  "</td><td>"+numFmt(results[1][6])+ "<br/>("+numFmt(results[1][7])+")"+"</td>";

		  $("<tr/>").html(newListItem).addClass(rowType).appendTo(".navSumm");
      }
}
