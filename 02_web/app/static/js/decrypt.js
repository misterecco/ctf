function sanitize(s) {
	return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function prettify(s) {
	return String(s).replace(/\n/g, "<br>");
}

function decryptMessage() {
	var privkey = document.getElementById("privkey");
	var user_pass = document.getElementById("pgp-pass");
	var encMessage = document.getElementById("enc-msg").textContent.trim();
	var decDiv = document.getElementById("dec-msg");
	var user;

	kbpgp.KeyManager.import_from_armored_pgp({
	  armored: privkey.value.trim()
	}, function(err, user) {
		if (!err) {
			if (user.is_pgp_locked()) {
				user.unlock_pgp({
				    passphrase: user_pass.value
			    }, function(err) {
                    if (!err) {
                        console.log("Loaded private key with passphrase");
                        var ring = new kbpgp.keyring.KeyRing;
                        var php_msg = encMessage;
                        var kms = [user];
                        var asp;
                        for (var i in kms) {
                          ring.add_key_manager(kms[i]);
                        }
                        kbpgp.unbox({keyfetch: ring, armored: php_msg, asp }, function(err, literals) {
                            if (err != null) {
                                return alert("Problem: " + err);
                            } else {
                                decDiv.innerHTML = "";
                                var clean = sanitize(literals[0].toString());
                                clean = prettify(clean);
                                decDiv.innerHTML = clean;
                            }
                        });
                    } else {
                        alert("passphrase failed: " + err);
                    }
	            });
	        } else {
	          console.log("Loaded private key w/o passphrase");
	        }
		} else {
			alert("Key load failed: " + err);
		}
	});
}
