from __future__ import print_function

from dropbox.client import DropboxOAuth2FlowNoRedirect

import config


def main():
    consumer_key = getattr(config, 'CONSUMER_KEY', '')
    consumer_secret = getattr(config, 'CONSUMER_SECRET', '')
    if not (consumer_key and consumer_secret):
        print('Error! Please provide CONSUMER_KEY and CONSUMER_SECRET in '
              'config.json')
        return
    flow = DropboxOAuth2FlowNoRedirect(config.CONSUMER_KEY,
                                       config.CONSUMER_SECRET)
    url = flow.start()
    print('Follow this link and grant access to ViaWebDAV:')
    print(url, '\n')
    code = raw_input('Enter the code: ').strip()
    accessToken, userId = flow.finish(code)
    print('Your access token: ', accessToken)
    print("""
Put this token into section ACCESS_TOKENS of config.json, e.g.:

    {
        "CONSUMER_KEY": "...",
        "CONSUMER_SECRET": "...",
        "ACCESS_TOKENS": {
            "": "<access-token>",  // map the account to "/"
            "alex": "<another-access-token>"  // map the account to "/alex"
        }
    }
""")


if __name__ == '__main__':
    main()
