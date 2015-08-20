#Telegrams

Telegrams are simply in the nationstates module. Simply give it the information it needs and It will send the message.

Parameters:

All telegram parameters are optional arguments, however you must include them for a valid request (Other than `auto_send` and `user_agent`). (As they do not have valid default settings)

* `to` - Who to send the message to. It must be an nation 
* `client key` - [Nationstates Guide](https://www.nationstates.net/pages/api.html#telegrams)
* `tgid` - [Nationstates Guide](https://www.nationstates.net/pages/api.html#telegrams)
* `secret_key` - [Nationstates Guide](https://www.nationstates.net/pages/api.html#telegrams)
* `auto_send` - Set `True` to make the module send the request when you create the Telegram object. (Not Recommmend)
* `user_agent` - If set, it will use the supplied string as the user agent for only this request.