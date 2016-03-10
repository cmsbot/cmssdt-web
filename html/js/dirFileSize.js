
var goTable;

function fnFilterNormal ()
{
var jqInputs = $('#filter_norm input');
var iColumn = 0; // jqInputs[1].value == "" ? null : jqInputs[1].value;
goTable.fnFilter( jqInputs[0].value, iColumn );
}

function fnFilterRegex ()
{
var jqInputs = $('#filter_regex input');
var iColumn = jqInputs[1].value == "" ? null : jqInputs[1].value;
goTable.fnFilter( jqInputs[0].value, iColumn, false );
}

$('#filter_norm input').keyup( fnFilterNormal );
$('#filter_regex input').keyup( fnFilterRegex )

	$(document).ready(function() {
            goTable = $('#dirFileSize').dataTable( {
			    "sPaginationType": "full_numbers",
                            "bProcessing" : true,
                            "bServerSide" : true,
                            "bLengthChange" : true,
                            "bSaveState" : true,
			    "bPaginate" : true,
			    "bSort" : true,
			    "bInfo" : true,
			    "bFilter" : true,
			    "bAutoWidth" : true,
			    "aaSorting" : [[ 1, "asc" ]],
                            "sAjaxSource": "/SDT/cgi-bin/getDirFileSizeInfo.py",
			    "fnServerData": function ( sSource, aoData, fnCallback ) {
			          /* Add some extra data to the sender  */
			          aoData.push( { "name": "release", "value": $('#filter_norm input')[0].value });
				  $.getJSON( sSource, aoData, function (json) { 
				  	/* Do whatever additional processing you want on the callback, then tell DataTables */
				  	fnCallback(json)
				  } );

			     },
			} );
	   $('#filter_norm input').keyup( fnFilterNormal );
	   $('#filter_regex input').keyup( fnFilterRegex );

	} );
