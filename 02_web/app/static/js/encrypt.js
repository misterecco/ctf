function encryptAndSend() {
    var pubkey = document.getElementById("dest-pubkey").textContent.trim();
    var origMessage = document.getElementById("origMessage");
    var encMessage = document.getElementById("encMessage");
    var user;
    kbpgp.KeyManager.import_from_armored_pgp({
      armored: pubkey
    }, function(err, user) {
        console
        if (!err) {
            var params = {
                msg: origMessage.value,
                encrypt_for: user
            };
            kbpgp.box(params, function(err, result_string, result_buffer) {
                if(!err) {
                    encMessage.value = result_string;
                    origMessage.value = "";
                    document.getElementById("message-form").submit();
                } else {
                    alert("Error encrypting message, try again later.");
                }
            });
        } else {
            alert("Error using public key, try again later.");
        }
    });
}
