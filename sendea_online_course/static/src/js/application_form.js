odoo.define('sendea_online_course.application_form', function (require) {
    "use strict";
    
    const ajax = require('web.ajax');

    function populateDistricts() {
        let regionId = $('#region').val();
        ajax.jsonRpc('/get_districts', 'call', {region_id: regionId}).then(function (data) {
            $('#district').empty().append('<option value="">Select a District</option>');
            data.forEach(district => {
                $('#district').append(`<option value="${district.id}">${district.name}</option>`);
            });
        });
    }

    window.populateDistricts = populateDistricts;
});
