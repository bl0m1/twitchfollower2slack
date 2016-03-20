# twitchfollower2slack
twitchfollower2slack is used to notify a Slack-channel when a Twitch channel got a new follower or followers. Polls Twitch API every 60s.


# Requirements
* Python 3
* External Python 3 modules
  * dateutil
  * requests
  * [twitchchannelquery](https://github.com/bl0m1/twitchquery/)

# Installing
1. Install Python 3 and pip.

1. Install following Python 3 modules (pip install):
   * dateutil
   * requests

1. Make sure twitchchannelquery module is in the same dir as twitchfollower2slack.

1. Run twitchfollower2slack to generate the file 'config.json'.
   Exit script (ctrl + c) and modify this file with your own settings.
