/**
 * Created by shuchengxiang on 2019/2/14.
 */
window.Superlists = {};
window.Superlists.initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide()
    });
};