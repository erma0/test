function encrypt(data, key) {
    var result;
    Java.perform(function () {
        var x = Java.use('com.qq.lib.EncryptUtil');
        result = x.encrypt(data, key);
    });
    return result;
};
function decrypt(data, key) {
    var result;
    Java.perform(function () {
        var x = Java.use('com.qq.lib.EncryptUtil');
        result = x.decrypt(data, key);
    });
    return result;
};
rpc.exports = {
    decrypt: decrypt,
    encrypt: encrypt,
};