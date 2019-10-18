function saveMenu() {
    let changes = null;
    $.post(window.location.pathname, changes).done(function(data) {
        location.reload();
    });
}

function deleteMenu(menuId) {
    if (confirm('Are you sure you want to delete this menu?')) {
        if (confirm('It will be permanently erased. This action is irreversible.')) {
            $("#deleteMenuForm").submit();
        }
    }
    return false;
}

function addItem(categoryId) {
    $("#categoryIdForNewItem").val(categoryId);
    $("#categoryNameForNewItem").html('in ' + $("#categoryLabel_"+categoryId).val());
    $('#newItemModal').modal('show');
}


function addNewItemOption() {
    $.post('/account/getObjectId').done(function(object_id) {
        $("#newItemOptions").append(`
            <div id="newItemOptionWrapper_${object_id}" class="newItemOptionWrapper">
                <div class="card col-md-10" style="margin:20px 0px 20px 0px;padding:30px;float:left;">
                    <div class="col-md-12">
                        <div class='form-group'>
                            <input class='form-control form-control-sm' id='newItemOptionLabel_${object_id}' type='text' id='newItemOptionLabel_${object_id}' autocomplete="off" placeholder="Option name" />
                        </div>
                        <small>
                            <div class="custom-control custom-radio" style="float:left;">
                                <input type="radio" id="newItemOptionSingle_${object_id}" name="newItemOptionType_${object_id}" class="custom-control-input newItemOptionType" value="single" onclick="newItemOptionTypeSingle('${object_id}')">
                                <label class="custom-control-label" style="padding-top:2px;" for="newItemOptionSingle_${object_id}">Select One</label>
                            </div>
                            <div class="custom-control custom-radio" style="float:right;">
                                <input type="radio" id="newItemOptionMultiple_${object_id}" name="newItemOptionType_${object_id}" class="custom-control-input newItemOptionType" value="multiple" onclick="newItemOptionTypeMultiple('${object_id}')">
                                <label class="custom-control-label" style="padding-top:2px;" for="newItemOptionMultiple_${object_id}">Select Multiple</label>
                            </div>
                        </small>
                    </div>
                    <hr style="display:none;" id="newItemOptionDivider_${object_id}">
                    <div class="col-md-12" id="newItemOptionBody_${object_id}">

                    </div>
                </div>
                <a style="float:right;margin-top:50px;" class="text-danger col-md-1" href="javascript:removeNewItemOption('${object_id}')"><span class="fa fa-minus-circle"></span></a>
            </div>
        `)
    });
}

function removeNewItemOption(option_id) {
    $("#newItemOptionWrapper_"+option_id).remove();
}

//ADD SINGLE SELECT VALUE TO NEW ITEM OPTION
function addNewItemOptionSingleValue(option_id) {
    $.post('/account/getObjectId').done(function(value_id) {
        $("#newItemOptionBody_"+option_id).append(`
            <div class="row" id="newItemOptionValueWrapper_${value_id}">
                <div class="col-md-1">
                    <input type="radio" id="newItemOptionSingleValue_${value_id}" name="newItemOptionSingleValue_${option_id}" />
                </div>
                <div class="form-group col-md-6" style="float:left;">
                    <input class='form-control form-control-sm' id='' type='text' name='' placeholder="Value name" autocomplete="off" />
                </div>
                <div class='form-group col-md-4' style="float:right;">
                  <div class="form-group">
                    <div class="input-group input-group-sm mb-2">
                      <div class="input-group-prepend">
                        <span class="input-group-text">$</span>
                      </div>
                      <input placeholder="0.00" class="form-control form-control-sm dollarAmount" value="0.00" />
                    </div>
                  </div>
                </div>
                <div class="col-md-1" style="float:left;padding-right:0px;">
                    <a style="float:right;" class="text-danger" href="javascript:removeNewItemOptionValue('${value_id}')"><span class="fa fa-minus-circle"></a>
                </div>
            </div>
        `);
    });
}

//ADD MULTI SELECT VALUE TO NEW ITEM OPTION
function addNewItemOptionMultipleValue(option_id) {
    $.post('/account/getObjectId').done(function(value_id) {
        $("#newItemOptionBody_"+option_id).append(`
            <div class="row" id="newItemOptionValueWrapper_${value_id}">
                <div class="col-md-1">
                    <input type="checkbox" id="newItemOptionMultipleValue_${value_id}" name="newItemOptionMultipleValue_${value_id}" />
                </div>
                <div class="form-group col-md-6" style="float:left;">
                    <input class='form-control form-control-sm' id='' type='text' name='' placeholder="Value name" autocomplete="off" />
                </div>
                <div class='form-group col-md-4' style="float:right;">
                  <div class="form-group">
                    <div class="input-group input-group-sm mb-2">
                      <div class="input-group-prepend">
                        <span class="input-group-text">$</span>
                      </div>
                      <input placeholder="0.00" class="form-control form-control-sm dollarAmount" value="0.00" />
                    </div>
                  </div>
                </div>
                <div class="col-md-1" style="float:left;padding-right:0px;">
                    <a style="float:right;" class="text-danger" href="javascript:removeNewItemOptionValue('${value_id}')"><span class="fa fa-minus-circle"></a>
                </div>
            </div>
        `);
    });
}


function removeNewItemOptionValue(valueId) {
    $("#newItemOptionValueWrapper_"+valueId).remove();
}

function newItemOptionTypeSingle(option_id) {
    $("#newItemOptionDivider_"+option_id).show();
    $("#newItemOptionSingle_"+option_id).attr('disabled', '')
    $("#newItemOptionMultiple_"+option_id).removeAttr('disabled')
    $("#newItemOptionBody_"+option_id).html('');
    $("#newItemOptionBody_"+option_id).append(`
        <p class="lead" style="font-size:14px;">Select One <a href="javascript:addNewItemOptionSingleValue('${option_id}')" style="float:right;"><span class="fa fa-plus"></span></a></p>
        <hr>
    `)
}

function newItemOptionTypeMultiple(option_id) {
    $("#newItemOptionDivider_"+option_id).show();
    $("#newItemOptionSingle_"+option_id).removeAttr('disabled')
    $("#newItemOptionMultiple_"+option_id).attr('disabled', '')
    $("#newItemOptionBody_"+option_id).html('');
    $("#newItemOptionBody_"+option_id).append(`
        <p class="lead" style="font-size:14px;">Select Multiple <a href="javascript:addNewItemOptionMultipleValue('${option_id}')" style="float:right;"><span class="fa fa-plus"></span></a></p>
        <hr>
    `)
}


$(function() {
    addItem('5da95a5d0748a9b3f563d06d') //TEST
    addNewItemOption();
    //
    // $("#multiPricingSwitch").change(function() {
    //     if(this.checked) {
    //
    //     } else {
    //
    //     }
    // });

    $( ".dollarAmount" ).focusout(function() {
        $(this).val(accounting.formatMoney($(this).val()).replace('$', ''));
    });


});
